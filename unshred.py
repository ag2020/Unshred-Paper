# Read in directory path from command line
import sys
dir_path = sys.argv[1]

import os
from PIL import Image
import numpy as np

# Convert all images in directory into array format and save in data array
data = []
for file_name in os.listdir(dir_path):
    file_path = os.path.join(dir_path, file_name)
    image = Image.open(file_path)
    data.append(np.asarray(image))

# Calculates the squared correlation between the two images, with the image corresponding to data1 on the left and the image corresponding to data2 on the right
def calc_corr(data1, data2):
    return np.sum(np.square(data1[:, -1] - data2[:, 0]))


# Finds all the unique shred heights and separates them
images_data = {}
for elem in data:
    if elem.shape[0] not in images_data:
        images_data[elem.shape[0]] = [elem]
    else:
        images_data[elem.shape[0]].append(elem)


files = []  # will store the names of all the output files

# Goes through all the shreds grouped by height
for image_data in images_data.values():
    num_slices = len(image_data)
    order = {}  # will store which image comes after which image

    # will store which images do not come after any other images (so they are the leftmost image in the picture)
    start = set(range(num_slices))

    # Calculates the correlations between all the images and determines the ordering of the images
    # Images with a low correlation are likely adjacent in the picture
    for i in range(num_slices):
        corrs = []
        for j in range(num_slices):
            # uses calc_corr function to calculate correlation
            corr = calc_corr(image_data[i], image_data[j])
            corrs.append(corr)

        # Makes sure that a shred is not found to be adjacent to itself
        max_val = max(corrs)
        corrs[i] = max_val

        # The shred with the least correlation (if any) is adjacent to the current shred
        arg_min = np.argmin(corrs)
        if corrs[arg_min] < 0.65 * max_val:
            order[i] = arg_min
            start.discard(arg_min)

    # Uses each starting shred to construct an image
    for num in start:
        final_image = image_data[num]
        element = num
        # Makes sure that we don't enter an infinite loop
        already_seen = {element}

        # Keeps adding shreds one at a time to the final image until there are no more adjacent shreds
        while element in order:
            element = order[element]
            if element in already_seen:
                break  # Avoids infinite loop
            already_seen.add(element)
            # Augments the final image
            final_image = np.hstack((final_image, image_data[element]))

        # Converts image from array format to visual format
        image = Image.fromarray(final_image)
        image.show()

        # Constructs file name and saves the image
        if dir_path[-1] == '/':
            dir_path = dir_path[:-1]
        file_name = dir_path[(dir_path.rfind('/') + 1):] + \
            '_' + str(len(files) + 1) + '.jpg'
        image.save(file_name)
        files.append(file_name)

print("Images successfully reconstructed. Saved in files", str(files) + '.') # Prints out the names of the files containing the output images
