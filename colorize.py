from PIL import Image
import numpy as np
import colorsys
import random
import argparse
import os

rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)

class Hue:
    def __init__(self, name: str, pure_value: int, min_value: int, max_value: int) -> None:
        self.name = name
        self.pure_value = pure_value
        self.min_value = min_value
        self.max_value = max_value
        self.f_pure_value: float = float(pure_value / 360)
        self.f_min_value: float = float(min_value / 360)
        self.f_max_value: float = float(max_value / 360)
        self.f_value: float = random.uniform(self.f_min_value, self.f_max_value)

        self.saturation_shift: float = 0.0
        sat_rand = random.random()
        if sat_rand < 0.1:
            self.saturation_shift = 0.1
        elif sat_rand < 0.2:
            self.saturation_shift = -0.1
        self.value_shift: float = 0
        val_rand = random.random()
        if val_rand < 0.05:
            self.value_shift = -90


class Rainbow:
    def __init__(self) -> None:
        self.hue_array: [Hue] = []

    def add_hue(self, hue: Hue):
        self.hue_array.append(hue)

    def get_random_hue(self) -> Hue:
        if self.hue_array:
            return random.choice(self.hue_array)

def shift_hue(arr, new_hues: [Hue], new_hue_white: Hue, rainbow: Rainbow, alter_white: bool = True):
    r,g,b,a = np.rollaxis(arr, axis=-1)
    h,s,v = rgb_to_hsv(r,g,b)
    # colorize here
    ## change hue
    for i in range(len(h)):
        for j in range(len(h[i])):
            for idx, hue in enumerate(rainbow.hue_array):
                if h[i][j] < hue.f_max_value:
                    h[i][j] = new_hues[idx].f_value
                    s[i][j] += new_hues[idx].saturation_shift
                    if s[i][j] > 1.0:
                        s[i][j] = 1.0
                    elif s[i][j] < 0.0:
                        s[i][j] = 0.0
                    v[i][j] += new_hues[idx].value_shift
                    if v[i][j] > 360:
                        v[i][j] = 360
                    elif v[i][j] < 0.0:
                        v[i][j] = 0.0
                    break
    ## alter whites
    if alter_white:
        for i in range(len(s)):
            for j in range(len(s[i])):
                if s[i][j] < 0.15:
                    h[i][j] = new_hue_white.f_pure_value
                    s[i][j] += new_hue_white.saturation_shift
                    if s[i][j] > 1.0:
                        s[i][j] = 1.0
                    elif s[i][j] < 0.0:
                        s[i][j] = 0.0
                    v[i][j] += new_hue_white.value_shift
                    if v[i][j] > 360:
                        v[i][j] = 360
                    elif v[i][j] < 0.0:
                        v[i][j] = 0.0
    # colorize over
    r,g,b = hsv_to_rgb(h,s,v)
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
    forceWhiteShift = argument.forceWhiteShift
    ls_directories = directories.split(',')
    ls_subdirectories = subdirectories.split(',')
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

    red_low = Hue("red", 0, 0, 6)
    orange = Hue("orange", 30, 6, 41)
    yellow = Hue("yellow", 60, 41, 76)
    yellow_green = Hue("yellow_green", 90, 76, 101)
    green = Hue("green", 120, 101, 140)
    teal = Hue("teal", 150, 140, 161)
    cyan = Hue("cyan", 180, 161, 200)
    blue = Hue("blue", 240, 200, 251)
    purple = Hue("purple", 270, 251, 276)
    magenta = Hue("magenta", 300, 276, 345)
    red_high = Hue("red", 360, 345, 360)

    rainbow =  Rainbow()
    rainbow.add_hue(red_low)
    rainbow.add_hue(orange)
    rainbow.add_hue(yellow)
    rainbow.add_hue(yellow_green)
    rainbow.add_hue(green)
    rainbow.add_hue(teal)
    rainbow.add_hue(cyan)
    rainbow.add_hue(blue)
    rainbow.add_hue(purple)
    rainbow.add_hue(magenta)
    rainbow.add_hue(red_high)

    new_hues: [Hue] = []
    for x in range(0, len(rainbow.hue_array) - 1):
        new_hues.append(rainbow.get_random_hue())
    new_hues.append(new_hues[0])

    new_hue_white: [Hue] = rainbow.get_random_hue()
    new_hue_white.saturation_shift = 0.4
    new_hue_white.value_shift = -45

    for idx, hue in enumerate(new_hues):
        print(rainbow.hue_array[idx].name, "to", hue.name)
    print("whites to", new_hue_white.name)
    alter_white = False
    if random.random() >= 0.5 or forceWhiteShift == "True":
        alter_white = True
    print("alter white?", alter_white)

    for idx, texture in enumerate(imgs):
        tex = texture.convert('RGBA')
        arr = np.array(np.asarray(tex).astype('float'))
        new_img = Image.fromarray(shift_hue(arr, new_hues, new_hue_white, rainbow, alter_white).astype('uint8'), 'RGBA')
        # new_name = files[idx].replace("palette", "new_palette")
        new_img.save(files[idx])
        # new_img.save(new_name)
