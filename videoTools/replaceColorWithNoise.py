#! venv/bin/python3
# Replace pixels in a color range using multiple noise/inpainting strategies

import cv2
import numpy as np
import os
from PIL import Image
import multiprocessing
import argparse

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

# =========================
# Inpainting
# =========================

def inpaint_replace(image_rgb, mask, radius):
    return cv2.inpaint(
        image_rgb,
        mask,
        inpaintRadius=radius,
        flags=cv2.INPAINT_TELEA
    )


# =========================
# Worker
# =========================

def process_file(args):
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
    ) = args

    in_path = os.path.join(input_path, filename)
    out_path = os.path.join(output_path, filename)

    if os.path.exists(out_path):
        print(f"Skipping {filename}")
        return

    image_bgr = cv2.imread(in_path)
    if image_bgr is None:
        return

    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    mask = color_range_mask(image_rgb, target_color, color_range)

    if not mask.any():
        cv2.imwrite(out_path, image_bgr)
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
        result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)

    else:
        raise ValueError(f"Unknown method: {method}")

    save_mask_if_needed(mask, output_path, filename, save_mask)
    cv2.imwrite(out_path, result)


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

