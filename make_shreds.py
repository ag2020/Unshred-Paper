# Read in and validate command-line arguments
import sys
if len(sys.argv) % 2 == 0 or len(sys.argv) < 3:
    raise Exception("Incorrect number of arguments")

for i in range(2, len(sys.argv), 2):
    try:
        int(sys.argv[i])
    except:
        raise Exception("Every alternate argument must be an integer")

# Make new directory to contain shreds
import os
dir_name = ''
for i in range((len(sys.argv) - 1) // 2):
    image_path = sys.argv[2 * i + 1]
    num_slices = int(sys.argv[2 * i + 2])
    name_start = image_path.rfind('/')
    name_end = image_path.rfind('.')
    if i > 0:
        dir_name += '_'
    if name_end == -1:
        dir_name += image_path[(name_start + 1):] + '_' + str(num_slices)
    else:
        dir_name += image_path[(name_start + 1):name_end] + '_' + str(num_slices)
os.makedirs(dir_name)

from PIL import Image
from numpy import asarray
import random

# Make shreds of images
for j in range((len(sys.argv) - 1) // 2):
    image_path = sys.argv[2 * j + 1]
    num_slices = int(sys.argv[2 * j + 2])

    # Read in image using Pillow
    image = Image.open(image_path)

    # Convert image into 3D array
    data = asarray(image)

    # Make array which contains endpoints of slices
    slice_ends = random.sample(range(1, data.shape[1]), num_slices - 1)
    slice_ends.sort()

    # Make slices of image (in data format)
    slices = []
    for i in range(num_slices - 1):
        if i == 0:
            start = 0
        else:
            start = slice_ends[i - 1]
        slices.append(data[:, start:slice_ends[i]])
    slices.append(data[:, slice_ends[num_slices - 2]:])

    # Convert slice data into actual image shreds, and shuffle
    shreds = []
    for i in range(num_slices):
        shreds.append(Image.fromarray(slices[i]))
    random.shuffle(shreds)

    # Save shreds as image files in directory
    for i in range(num_slices):
        shreds[i].save(dir_name + '/shred_' + str(j + 1) + '_' + str(i + 1) + '.jpg')

print("Shreds successfully saved in directory " + dir_name + '.')
