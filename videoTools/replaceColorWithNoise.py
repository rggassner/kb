#! venv/bin/python3
# Replace pixels in a color range using multiple noise/inpainting strategies
import os
import multiprocessing
import argparse
import cv2
import numpy as np
from PIL import Image

# =========================
# Helpers
# =========================

def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def color_range_mask(image_rgb, target_color, color_range):
    target = np.array(target_color, dtype=np.int16)
    lower = np.clip(target - color_range, 0, 255).astype(np.uint8)
    upper = np.clip(target + color_range, 0, 255).astype(np.uint8)
    return cv2.inRange(image_rgb, lower, upper)


def save_mask_if_needed(mask, output_path, filename, save_mask):
    if save_mask:
        Image.fromarray(mask).save(
            os.path.join(output_path, f"mask_{filename}")
        )


# =========================
# Gaussian (fixed)
# =========================

def gaussian_replace(image, mask, noise_level):
    noise = np.random.normal(
        0, noise_level, image.shape
    ).astype(np.int16)

    img = image.astype(np.int16)
    img[mask > 0] += noise[mask > 0]
    return np.clip(img, 0, 255).astype(np.uint8)


# =========================
# Gaussian (adaptive)
# =========================

def gaussian_adaptive_replace(image_rgb, image_bgr, mask, target_color, noise_level):
    target = np.array(target_color, dtype=np.float32)

    # Distance from target color
    diff = image_rgb.astype(np.float32) - target
    dist = np.linalg.norm(diff, axis=2)

    if not mask.any():
        return image_bgr

    max_dist = dist[mask > 0].max()
    if max_dist == 0:
        max_dist = 1.0

    # Strength: closer to target → stronger noise
    strength = 1.0 - (dist / max_dist)
    strength = np.clip(strength, 0.0, 1.0)

    # Gaussian noise
    noise = np.random.normal(
        0, noise_level, image_bgr.shape
    ).astype(np.float32)

    # Work fully in float
    img = image_bgr.astype(np.float32)

    for c in range(3):
        img[:, :, c][mask > 0] += (
            noise[:, :, c][mask > 0] * strength[mask > 0]
        )

    return np.clip(img, 0, 255).astype(np.uint8)


# =========================
# Poisson noise
# =========================

def poisson_replace(image, mask, noise_level):
    """
    Apply Poisson noise with controllable strength.
    Lower noise_level -> stronger noise
    Higher noise_level -> weaker noise
    """
    img = image.astype(np.float32)

    # Normalize noise_level into a safe lambda scale
    # Prevent division by zero
    scale = max(noise_level, 1)

    # Scale image to Poisson domain
    lam = np.clip(img / scale, 0, None)

    noisy = np.random.poisson(lam).astype(np.float32) * scale

    result = image.copy()
    result[mask > 0] = np.clip(noisy[mask > 0], 0, 255).astype(np.uint8)

    return result


def inpaint_replace(image_rgb, mask, radius):
    """
    Replace masked regions in an image using OpenCV inpainting.

    This function fills the regions specified by the mask using the
    Telea inpainting algorithm. The masked pixels are reconstructed
    based on surrounding pixel information, producing a smooth and
    visually consistent result. It is typically used to remove or
    conceal areas matching a target color or artifact.

    Parameters
    ----------
    image_rgb : numpy.ndarray
        Input image in RGB color space with shape (H, W, 3).
    mask : numpy.ndarray
        Single-channel 8-bit mask where non-zero values indicate
        regions to be inpainted.
    radius : int
        Radius of the circular neighborhood used during inpainting.
        Larger values increase smoothing but may reduce local detail.

    Returns
    -------
    numpy.ndarray
        The inpainted image in RGB color space.
    """
    return cv2.inpaint( # pylint: disable=no-member
        image_rgb,
        mask,
        inpaintRadius=radius,
        flags=cv2.INPAINT_TELEA # pylint: disable=no-member
    )


def process_file(argsi): # pylint: disable=too-many-locals
    """
    Process a single image file by replacing a target color range using the
    specified method and parameters.

    This function is designed to be called with a tuple of arguments, making it
    suitable for use with multiprocessing or map-style execution. It loads an
    input image, builds a mask for pixels within a given color range, and applies
    one of several replacement strategies (gaussian, adaptive gaussian, poisson,
    or inpainting). The processed image is then written to the output directory.

    If the output file already exists, the file is skipped. If no pixels match
    the target color range, the original image is copied unchanged.

    Parameters
    ----------
    argsi : tuple
        A tuple containing the following elements, in order:
        - filename (str): Name of the image file to process.
        - method (str): Replacement method to use. One of
          {"gaussian", "gaussian_adaptive", "poisson", "inpaint"}.
        - input_path (str): Directory containing the input images.
        - output_path (str): Directory where processed images are written.
        - target_color (tuple or list): Target color in RGB space.
        - color_range (int or tuple): Tolerance or range used to build the color mask.
        - noise_level (float): Noise or strength parameter used by gaussian/poisson methods.
        - inpaint_radius (int): Radius used for OpenCV inpainting.
        - save_mask (bool): Whether to save the generated mask alongside the output.

    Raises
    ------
    ValueError
        If an unknown replacement method is specified.
    """
    (
        filename,
        method,
        input_path,
        output_path,
        target_color,
        color_range,
        noise_level,
        inpaint_radius,
        save_mask,
    ) = argsi

    in_path = os.path.join(input_path, filename)
    out_path = os.path.join(output_path, filename)

    if os.path.exists(out_path):
        print(f"Skipping {filename}")
        return

    image_bgr = cv2.imread(in_path) # pylint: disable=no-member
    if image_bgr is None:
        return

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB) # pylint: disable=no-member
    mask = color_range_mask(image_rgb, target_color, color_range)

    if not mask.any():
        cv2.imwrite(out_path, image_bgr) # pylint: disable=no-member
        return

    if method == "gaussian":
        result = gaussian_replace(image_bgr, mask, noise_level)

    elif method == "gaussian_adaptive":
        result = gaussian_adaptive_replace(
            image_rgb, image_bgr, mask, target_color, noise_level
        )

    elif method == "poisson":
        result = poisson_replace(image_bgr, mask, noise_level)

    elif method == "inpaint":
        result = inpaint_replace(image_rgb, mask, inpaint_radius)
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR) # pylint: disable=no-member

    else:
        raise ValueError(f"Unknown method: {method}")

    save_mask_if_needed(mask, output_path, filename, save_mask)
    cv2.imwrite(out_path, result) # pylint: disable=no-member


# =========================
# Main
# =========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Replace pixels in a color range using noise or inpainting"
    )

    parser.add_argument("--method", choices=[
        "gaussian", "gaussian_adaptive", "poisson", "inpaint"
    ], default="gaussian")

    parser.add_argument("--input-path", default="input_directory")
    parser.add_argument("--output-path", default="output_directory")

    parser.add_argument("--target-color", nargs=3, type=int, default=[0, 0, 0])
    parser.add_argument("--color-range", type=int, default=30)

    parser.add_argument("--noise-level", type=int, default=50)
    parser.add_argument("--inpaint-radius", type=int, default=30)

    parser.add_argument("--save-mask", action="store_true")

    args = parser.parse_args()

    ensure_output_dir(args.output_path)

    files = [
        f for f in os.listdir(args.input_path)
        if os.path.isfile(os.path.join(args.input_path, f))
    ]

    work = [
        (
            f,
            args.method,
            args.input_path,
            args.output_path,
            tuple(args.target_color),
            args.color_range,
            args.noise_level,
            args.inpaint_radius,
            args.save_mask,
        )
        for f in files
    ]

    with multiprocessing.Pool() as pool:
        pool.map(process_file, work)

