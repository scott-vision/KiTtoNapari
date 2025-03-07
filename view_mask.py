import napari
import tifffile
import numpy as np

# File paths
image_path = "2024-11-07_MC256_slide6_Capture_8_cropped.tif"  # Replace with your image file path
mask_path = "2024-11-07_MC256_slide6_Capture_8_cropped_segmented.tif"   # Replace with your mask file path
spot_path = "spot_masks/spotmask_every_10th_threshold99.7_sigma_2_spotradius3.tif"
scale = [1,0.271, 0.104, 0.104]
# Load the 5D image and mask
image = tifffile.imread(image_path)  # Shape: (time, z, channel, y, x)
mask = tifffile.imread(mask_path)    # Shape: (time, z, y, x)
spot_mask = tifffile.imread(spot_path)    # Shape: (time, z, y, x)

# Extract channel 1 (index 0) from the image
channel_1_image = image[..., 0, :, :]  # Shape: (time, z, y, x)
channel_2_image = image[..., 1, :, :]  # Shape: (time, z, y, x)

# Ensure the mask shape matches the channel shape
if mask.shape != channel_1_image.shape:
    raise ValueError("Mask shape does not match the selected channel's shape.")

# Create a masked image
masked_image_ch1 = np.where(mask > 0, channel_1_image, 0)  # Mask the channel
masked_image_ch2 = np.where(mask > 0, channel_2_image, 0)  # Mask the channel

filtered_spot_mask = spot_mask * mask

# Start Napari viewer
with napari.gui_qt():
    viewer = napari.Viewer(ndisplay=3)  # Initialize in 3D mode
    
    # Add the original channel 1 image
    viewer.add_image(
        channel_1_image, 
        name="Channel 1 Image (TZCYX)",
        colormap="cyan",
        scale=scale,  # Adjust scale to match physical dimensions
        rendering="mip"  # Maximum intensity projection for 3D rendering
    )
    # Add the original channel 2 image
    viewer.add_image(
        channel_2_image, 
        name="Channel 2 Image (TZCYX)",
        colormap="magenta",
        scale=scale,  # Adjust scale to match physical dimensions
        opacity=0.5,  # Make it semi-transparent for better visualization
        rendering="mip"  # Maximum intensity projection for 3D rendering
    )
    
    # Add the mask
    viewer.add_labels(
        mask,
        name="Mask",
        scale=scale,
        opacity=0.5  # Make it semi-transparent for better visualization
    )

    # Add the mask
    viewer.add_labels(
        filtered_spot_mask,
        name="Spots",
        scale=scale,
        opacity=0.5  # Make it semi-transparent for better visualization
    )
    
    # Add the masked image
    viewer.add_image(
        masked_image_ch1, 
        name="Masked Image Ch1",
        colormap="cyan",
        scale=scale,  # Adjust scale if needed
        opacity=0.5, 
        rendering="attenuated_mip"  # Attenuated maximum intensity projection
    )

    # Add the masked image
    viewer.add_image(
        masked_image_ch2, 
        name="Masked Image Ch2",
        colormap="magenta",
        scale=scale,  # Adjust scale if needed
        opacity=0.5, 
        rendering="attenuated_mip"  # Attenuated maximum intensity projection
    )