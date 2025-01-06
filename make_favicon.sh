#!/usr/bin/env bash
# Resize source image
convert img/PXL_20220603_180735988.MP_cropped.jpg -alpha off -resize 256x256 favicon_tmp.png
# Make a mask with a white circle on a black background
convert -size 256x256 xc:black -fill white -draw "circle 128,128 128,256" favicon_mask.png
# Apply the mask
convert favicon_tmp.png favicon_mask.png \
    -alpha Off -compose CopyOpacity -composite favicon_tmp.png
# Create favicon with multiple size images
convert favicon_tmp.png -resize 256x256 \
    -define icon:auto-resize="256,128,96,64,48,32,16" favicon.ico
# Remove temporary files
rm favicon_tmp.png
rm favicon_mask.png
