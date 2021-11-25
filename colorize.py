
from PIL import Image
import numpy as np
import colorsys
from colorthief import ColorThief
import random
import sys
import os
import argparse

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    h = hout
    r, g, b = hsv_to_rgb(h, s, v)
    arr = np.dstack((r, g, b, a))
    return arr

def shift_hue2(arr, new_hues, sat_diff, val_diff, hue_diff_array, invert):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    h, s, v = rgb_to_hsv(r, g, b)
    for idx1,hue_array in enumerate(h):
        for idx2, hue in enumerate(hue_array):
            for idx3, new_hue in enumerate(new_hues):
                if hue >= hue_diff_arr[idx3] and hue <= hue_diff_arr[idx3+1]:
                    h[idx1][idx2] = new_hue
                    new_s = s[idx1][idx2] + sat_diff[idx3]
                    if new_s < 0:
                        new_s = 0
                    elif new_s > 1:
                        new_s = 1
                    s[idx1][idx2] = new_s
                    new_v = v[idx1][idx2] + val_diff[idx3]
                    if new_v < 0:
                        new_v = 0
                    elif new_v > 255:
                        new_v = 255
                    v[idx1][idx2] = new_v
    r, g, b = hsv_to_rgb(h, s, v)
    if invert:
        r,g,b = 255-r,255-g,255-b
    arr = np.dstack((r, g, b, a))
    return arr

# def invert_hsv(h, s, v):
#     r, g, b = hsv_to_rgb(h, s, v)
#     if (v <= .2 or (v>.8 and s <= .2)):
#         r, g, b = 255-r,255-g,255-b
#     return rgb_to_hsv(r, g, b)

def colorize(image, hues, sats, vals, hue_diff_array, invert):
    # colorize an image to a new hue
    # hue (0-360)
    img = image.convert('RGBA')
    arr = np.array(np.asarray(img).astype('float'))
    new_img = Image.fromarray(shift_hue2(arr, hues, sats, vals, hue_diff_array, invert).astype('uint8'), 'RGBA')
    return new_img

if __name__=='__main__':
    parser = argparse.ArgumentParser(description = "Colorize a batch of .pngs with new hues")
    parser.add_argument("-p", "--paletteSize", help = "Example: 4. Higher number means more variations.", required = False, default = "6")
    parser.add_argument("-d", "--directory", help = "Example: em01_rathian_002_006/002_image. Main directory to colorize. Used to create the palette. Comma separate for multiple directories.", required = True, default = "")
    parser.add_argument("-s", "--subDirectory", help = "Example: em01_rathian_002_006/002_image. Secondary directory to colorize. Not used to create the palette. Comma separate for multiple directories.", required = False, default = "")
    
    argument = parser.parse_args()

    colorCount = int(argument.paletteSize)
    directories = argument.directory
    subdirectories = argument.subDirectory
    ls_directories = directories.split(',')
    ls_subdirectories = subdirectories.split(',')
    imgs_for_palette = []
    imgs = []
    files = []
    for directory in ls_directories:
        for file in os.listdir(directory):
            if file.endswith('.png'):
                filename = directory + '/' + file
                imgs_for_palette.append(Image.open(filename))
                imgs.append(Image.open(filename))
                files.append(filename)
    
    if argument.subDirectory:
        for subdirectory in ls_subdirectories:
            for file in os.listdir(subdirectory):
                if file.endswith('.png'):
                    filename = subdirectory + '/' + file
                    imgs.append(Image.open(filename))
                    files.append(filename)

    img_size = imgs_for_palette[0].size
    merged_image = Image.new('RGBA', (len(imgs)*img_size[0], img_size[1]))
    for idx, png in enumerate(imgs_for_palette):
        resized_img = imgs_for_palette[idx].resize(img_size)
        merged_image.paste(resized_img, (idx*img_size[0], 0))
    merged_filename = ls_directories[0] + '/merged.png'
    merged_image.save(merged_filename)

    color_thief = ColorThief(merged_filename)
    palette = color_thief.get_palette(color_count=colorCount) #8 maybe too busy?

    os.remove(merged_filename)

    hue_arr = []
    for idx, val in enumerate(palette):
        r, g, b = val
        h, s, v = rgb_to_hsv(r, g, b)
        # print(int(h*360))
        hue_arr.append(h)
    hue_arr.sort()

    hue_diff_arr = [0]
    for idx, val in enumerate(hue_arr):
        if idx + 1 < len(hue_arr):
            hue_diff_arr.append((hue_arr[idx] + hue_arr[idx+1]) / 2)
        else:
            hue_diff_arr.append((hue_arr[idx] + 1.0) / 2)
    hue_diff_arr.append(1.0)

    hues = []
    for x in range(1, len(hue_diff_arr)):
        hues.append(random.random())

    sats = []
    for x in range(1, len(hue_diff_arr)):
        sats.append(random.random() * .4 - .2)

    vals = []
    for x in range(1, len(hue_diff_arr)):
        vals.append((random.random()*255*.2) - (.1*255))

    invert = False
    if random.random() <= .1:
        invert = True

    for idx, texture in enumerate(imgs):
        new_img = colorize(texture, hues, sats, vals, hue_diff_arr, invert)
        new_img.save(files[idx])