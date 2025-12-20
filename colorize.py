from PIL import Image
import numpy as np
import colorsys
import random
import argparse
import os
import math

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

if __name__=='__main__':
    # TODO remove subdirectory since no longer trying to create palette. Will need to retool csv
    parser = argparse.ArgumentParser(description = "Colorize a batch of .pngs with new hues")
    parser.add_argument("-d", "--directory", help = "Example: em01_rathian_002_006/002_image. Main directory to colorize. Comma separate for multiple directories.", required = True, default = "")
    parser.add_argument("-s", "--subDirectory", help = "Example: em01_rathian_002_006/002_image. Secondary directory to colorize. Comma separate for multiple directories.", required = False, default = "")
    parser.add_argument("-c", "--bwcompress", help= "Example: True. if true it will compress the color spaces so blacks and whites are recolored.", required=False, default=False)

    argument = parser.parse_args()

    directories = argument.directory
    subdirectories = argument.subDirectory
    ls_directories = directories.split(',')
    ls_subdirectories = subdirectories.split(',')
    bwcompress = argument.bwcompress
    print(bwcompress)
    imgs = []
    files = []

    for directory in ls_directories:
        for file in os.listdir(directory):
            if file.endswith('.png'):
                filename = directory + '/' + file
                imgs.append(Image.open(filename))
                files.append(filename)
    
    if argument.subDirectory:
        for subdirectory in ls_subdirectories:
            for file in os.listdir(subdirectory):
                if file.endswith('.png'):
                    filename = subdirectory + '/' + file
                    imgs.append(Image.open(filename))
                    files.append(filename)

    colors_dict = {
        "red":  0,
        "orange": 30,
        "yellow": 60,
        "yellow-green": 90,
        "green": 120,
        "teal": 150,
        "cyan": 180,
        "blue": 240,
        "purple": 270,
        "magenta": 300,
        "red2": 360
    }

    new_hues = []
    for x in range(0, len(colors_dict) - 1):
        hue = random.choice(list(colors_dict.values()))
        if new_hues.count(hue) < 2:
            new_hues.append(random.choice(list(colors_dict.values())))
        else:
            hue = random.choice(list(colors_dict.values()))
            if new_hues.count(hue) < 2:
                new_hues.append(random.choice(list(colors_dict.values())))
            else:
                hue = random.choice(list(colors_dict.values()))
                new_hues.append(random.choice(list(colors_dict.values())))


    new_hues.append(new_hues[0])

    # print(colors_dict)
    # print(new_hues)

    color_values = list(colors_dict.values())
    # print(color_values)


    for idx, hue in enumerate(new_hues):
        print(list(colors_dict.keys())[idx], "to", hue)

    # print("whites to", new_hue_white.name)
    # alter_white = False
    # if random.random() >= 0.5:
    #     alter_white = True
    # print("alter white?", alter_white)

    for idx, texture in enumerate(imgs):
        tex = texture.convert('RGBA')
        arr = np.array(np.asarray(tex).astype('float'))
        # new_img = Image.fromarray(shift_hue(arr, new_hues, new_hue_white, rainbow, alter_white).astype('uint8'), 'RGBA')

        # working on new stuff here
        r,g,b,a = np.rollaxis(arr, axis=-1)
        h,s,v = rgb_to_hsv(r,g,b)
        for i in range(len(h)):
            for j in range(len(h[i])):

                for k in range(len(new_hues) - 1):
                    if h[i][j] >= (color_values[k] / 360.0) and h[i][j] < color_values[k + 1] / 360.0:
                        val = h[i][j] * 360.0
                        per = (val - color_values[k]) / (color_values[k + 1] - color_values[k])
                        per = -(math.cos(math.pi * per) - 1) / 2
                        hues = []
                        hues.append(new_hues[k])
                        hues.append(new_hues[k + 1])
                        # hue1 = new_hues[k]
                        # hue2 = new_hues[k + 1]
                        # if hues[0] == 0 and hues[1] > 180:
                        #     hues[0] = 360
                        # elif hues[0] == 360 and hues[1] <= 180:
                        #     hues[0] = 0

                        if hues[0] < hues[1]:
                            if hues[1] - hues[0] >= 180:
                                hues[1] = hues[1] - 360
                                per = 1.0 - per
                        elif hues[0] > hues[1]:
                            if hues[0] - hues[1] > 180:
                                hues[0] = hues[0] - 360
                            else:
                                per = 1.0 - per

                        # hues.sort()
                        # if hues[1] - hues[0] >= 180:
                        #     hues[1] = hues[1] - 360
                        #     per = 1.0 - per
                        # hues.sort()

                        new_val = per * abs(hues[1] - hues[0]) + min(hues[1], hues[0])
                        if new_val < 0:
                            new_val += 360
                        h[i][j] = new_val / 360.0
                
                # compress blacks and whites for specific files
                if bwcompress:
                    s[i][j] = (s[i][j] * 0.85) + 0.15
                    v[i][j] = (v[i][j] / 255.0) * (255.0 * 0.7) + (255.0 * 0.15)

        r,g,b = hsv_to_rgb(h,s,v)
        arr = np.dstack((r,g,b,a))

        new_img = Image.fromarray(arr.astype('uint8'), 'RGBA')

        # new_name = files[idx].replace(".png", "_2.png")
        new_img.save(files[idx])
        # new_img.save(new_name)
