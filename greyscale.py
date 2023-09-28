from PIL import Image, ImageOps
import numpy as np
import colorsys
import random
import argparse
import os
        
def greyscale(arr):
    r,g,b,a = np.rollaxis(arr, axis=-1)
    for i in range(len(r)):
        for j in range(len(r[i])):
            grey = 0.299*r[i][j] + 0.587*g[i][j] + 0.144*b[i][j]
            r[i][j] = grey
            g[i][j] = grey
            b[i][j] = grey
    arr = np.dstack((r,g,b,a))
    return arr

if __name__=='__main__':
    # TODO remove subdirectory since no longer trying to create palette. Will need to retool csv
    parser = argparse.ArgumentParser(description = "Colorize a batch of .pngs with new hues")
    parser.add_argument("-d", "--directory", help = "Example: em01_rathian_002_006/002_image. Main directory to colorize. Comma separate for multiple directories.", required = True, default = "")
    parser.add_argument("-s", "--subDirectory", help = "Example: em01_rathian_002_006/002_image. Secondary directory to colorize. Comma separate for multiple directories.", required = False, default = "")
    
    argument = parser.parse_args()

    directories = argument.directory
    subdirectories = argument.subDirectory
    ls_directories = directories.split(',')
    ls_subdirectories = subdirectories.split(',')
    imgs = []
    files = []

    for directory in ls_directories:
        for file in os.listdir(directory):
            if file.endswith('.png'):
                filename = directory + '/' + file
                new_filename = directory + '/orig_' + file
                os.rename(filename, new_filename)
                imgs.append(Image.open(new_filename))
                files.append(new_filename)
    
    if argument.subDirectory:
        for subdirectory in ls_subdirectories:
            for file in os.listdir(subdirectory):
                if file.endswith('.png'):
                    filename = subdirectory + '/' + file
                    new_filename = directory + '/orig_' + file
                    imgs.append(Image.open(new_filename))
                    files.append(new_filename)

    for idx, texture in enumerate(imgs):
        tex = texture.convert('RGBA')
        arr = np.array(np.asarray(tex).astype('float'))
        new_img = Image.fromarray(greyscale(arr).astype('uint8'), 'RGBA')
        new_name = files[idx].replace("orig_", "")
        new_img.save(new_name)
