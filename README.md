# Unshred Paper
I got the inspiration for this project will actually shredding paper.

#### make_shreds.py
The program make_shreds.py is used to digitally make shreds of images. Run

```python3 make_shreds.py file_location_1 number_shreds_1 file_location_2 number_shreds_2 ...```.

The program can take any number of files (at least one), with 2 arguments per file (location and number of shreds). It will output a directory will all the shreds. For each image, the shreds will be scrambled and may be of different sizes.

Example: ```python3 make_shreds.py file1.jpg 10 ../file2.jpg 20```.


#### unshred.py
The program unshred.py is used to digitally reconstruct an image from shreds. Run

```python3 unshred.py directory_path```.

The directory passed in can be created using make_shreds.py, but any directory with shreds (in image form) will work. The program will output all the images reconstructed (the directory can contain the shreds of more than one image), and will also display the images in your device's default image viewer.
