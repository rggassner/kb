#!/bin/bash
#
# init_mount.sh
# ---------------------------
# This script mounts specific drives in a defined order using their
# /dev/disk/by-id/ symlinks, then optionally enables a swapfile
# and provides hints for unmounting Veracrypt volumes.
#
# Why /dev/disk/by-id?
# --------------------
# Device names like /dev/sda and /dev/sdb can change between reboots.
# The /dev/disk/by-id symlinks are stable and tied to the disk’s serial number
# (and enclosure slot if using a multi-bay USB case).
#
# Notes:
# - The order of drives is important (outer → inner) and is preserved
#   using a simple indexed array.
# - Uses Veracrypt CLI in text mode (-t) for non-interactive mounting.
# - Swapfile management is optional and commented out for safety.
#
# Requirements:
# - veracrypt installed and available in $PATH
# - sudo privileges for swapon/swapoff commands
# - Drives should be identified via /dev/disk/by-id/ (stable across reboots)

# ------------------------------------------------------------------------------
# Ordered list of "device|mount_point"
# Modify this array to add or remove drives.
# ------------------------------------------------------------------------------
drives=(
    "/dev/disk/by-id/usb-External_USB3.0_DISK00_20170331000C3-0:0|/mnt/nas"
    "/dev/disk/by-id/usb-External_USB3.0_DISK01_20170331000C3-0:1|/mnt/nas/localhost/docs"
    "/dev/disk/by-id/usb-ST8000DM_004-2U9188_00000000000000000000-0:0|/mnt/backup"
)

missing=()

# ------------------------------------------------------------------------------
# Mount drives in order
# ------------------------------------------------------------------------------
for entry in "${drives[@]}"; do
    device="${entry%%|*}"       # left side of '|'
    mount_point="${entry##*|}"  # right side of '|'

    if [[ ! -e "$device" ]]; then
        echo "Drive not found: $device"
        missing+=("$device")
        continue
    fi

    mkdir -p "$mount_point"
    echo "Mounting $device at $mount_point"
    veracrypt -t "$device" "$mount_point"
done

# ------------------------------------------------------------------------------
# Error handling for missing drives
# ------------------------------------------------------------------------------
if (( ${#missing[@]} > 0 )); then
    echo
    echo "Some drives were not found:"
    printf '   - %s\n' "${missing[@]}"
    echo
    echo "Listing devices under /dev/disk/by-id/:"
    ls -l /dev/disk/by-id/
    exit 1
fi

# ------------------------------------------------------------------------------
# Optional: Create and enable a swapfile on the NAS
# Uncomment these lines if you need a swapfile
# ------------------------------------------------------------------------------
# dd if=/dev/zero of=/mnt/nas/swapfile bs=1M count=2048   # Create 2GB swapfile
# chmod 600 /mnt/nas/swapfile                             # Secure permissions
# mkswap /mnt/nas/swapfile                                # Format swap

# Enable NAS swapfile
sudo swapon /mnt/nas/swapfile

# Disable default swap (optional)
sudo swapoff /var/swap

# ------------------------------------------------------------------------------
# Optional: Unmount Veracrypt volumes manually
# Uncomment to unmount specific volumes
# ------------------------------------------------------------------------------
# cryptsetup -v remove /dev/mapper/truecrypt1_1
