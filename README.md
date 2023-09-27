<div align="center">

[![LATEST](https://img.shields.io/github/v/release/nuzcraft/FreedomUniteColorRandomizer?label=latest)](https://github.com/nuzcraft/FreedomUniteColorRandomizer/releases/latest)[![DOWNLOADS](https://img.shields.io/github/downloads/nuzcraft/FreedomUniteColorRandomizer/total)](https://github.com/nuzcraft/FreedomUniteColorRandomizer/releases)

</div>

---

# Freedom Unite Color Randomizer Patch

This is a mod/patch for Monster Hunter Portable 2nd G that will allow you to randomize the colors of the monsters. I've included files and instructions for how to colorize and patch your copy of the game which guarantees that you'll be fighting 100% unique monsters!

<div align="center">

<img src="https://github.com/nuzcraft/FreedomUniteColorRandomizer/assets/20135847/d41079ac-d094-4c78-8602-805389d74d69">

</div>

## How does the patch work?

The patch works by updating the texture file for each of the monsters with recolored ones. It tries to group similar colors together and update them so the monsters maintain some of their original shading.

## Applying the Patch

Make sure you use either a UMD dump or PSN version of `Monster Hunter Portable 2nd G`

All my development and testing was done with a version pre-patched with [FU Complete](https://github.com/FUComplete/Patch). The color randomization patch _should_ work on an unpatched version of MHP2G; I have not tested it.

### Option 1 - Use FUComplete File Replacer

---

For this option, we'll use IncognitoMan's [FU Complete](https://github.com/FUComplete/Patch). After downloading and running FU Complete on your copy of MHP2G, follow the directions [here](https://github.com/FUComplete/FUCTool#file-replacer) to start using the File Replacer.

1. Download the files from the most [recent release](https://github.com/nuzcraft/FreedomUniteColorRandomizer/releases/latest)
   - here, you should see at least one (if not multiple) .zip files labeled 'pacs'. These folders contain .pac mod files
2. Choose .zip file and unzip it. Each represents a different randomization; you don't need to use them all
3. Drop the .pac files you want to use into the mods folder for the File Replacer and press the `Generate nativePSP folder` button
4. Continue following the directions [here](https://github.com/FUComplete/FUCTool#file-replacer)

Feel free to mix and match or exclude .pac files. The `fileMapping_FUCR_2g.csv` file can help you identify which files correspond with which monsters. There are resources in FU Complete that can help with that too.

### Option 2 - Apply a pre-built xdelta patch to your image

---

For this option, you'll need [xdelta](https://github.com/jmacd/xdelta).

1. Download the files from the most [recent release](https://github.com/nuzcraft/FreedomUniteColorRandomizer/releases/latest)
   - here, you should see at least one (if not multiple) .xdelta files. These are pre-compiled patches.
2. Choose a single xdelta file if there are multiple available. Each represents a different randomization; you don't need to apply them all.
3. Copy your original image file (.iso) and the xdelta file into the same directory as the xdelta executable.
4. Run xdelta to apply the patch to the original iso
   - The format is -d -v -s original_file patch_file new_file
   - `./xdelta3.exe -d -v -s MHP2G_FUC.iso MHP2G_FUCR_v1.0_01.xdelta MHP2G_FUCR_v1.0_xdelta_01.iso`

Alternatively, you can use IncognitoMan's [FU Complete patcher](https://github.com/FUComplete/Patch/releases/latest). Just copy the xdelta file into the directory with the other xdelta files use for patching FU Complete.

### Option 3 - Create your own unique patch

---

We're going to open up the game file, find the texture files for the monsters, then use a python script to edit the colors (mostly by shifting hues). Then we'll use some pre-existing tools to pack everything back up into an iso image.

My preferred command line is bash, so all my example commands use bash.

### Additional files (outside this repo) that you'll need to create this patch.

- `Monster Hunter Portable 2nd G` UMD dump or PSN Version
  - Preferably patched with [FU Complete](https://github.com/FUComplete)
- [mhff](https://github.com/IncognitoMan/mhff)
  - we'll specifically use the data.py file for psp
  - mhff unpacks the DATA.BIN into a flat file format, which allows us to easily use a bash script to create a more intuitive file structure.
  - mhff also allows us to inject files back into DATA.BIN relatively easily.
- [mhtools](https://github.com/codestation/mhtools)
  - the mhtools.jar file included in the release is what we'll use
  - mhtools unpacks the individual files into a structure I could understand better than mhff. Presumably the tools are close to interchangable.
- [UMDGen](https://www.romhacking.net/utilities/1218/)
  - not needed if using [File Replacer](https://github.com/FUComplete/FUCTool#file-replacer)
  - I'm not sure if UMDGen has a real website?
  - We'll use this tool to put everything back together into a game we can play

### Steps

1. Create a new folder, you'll use this as your working directory
2. Download the code from this repo and place it in the directory
3. Copy `data.py` from `mhff` and `mhtools.jar` from `mhtools` to the working directory.
4. Extract the files from your MHP2G iso into your working directory.
   - I use 7-Zip, but you can use whatever you want.
   - It doesn't really matter what depth these files are at, so housing them in a subfolder is fine.
5. Copy `PSP_GAME/USRDIR/DATA.BIN` out into your working directory
6. Create a new folder in your working directory called `DATABIN`
7. Use the `data.py` file from `mhff` to extract the files from `DATA.BIN` into the folder called `DATABIN`
   - `python data.py a DATA.BIN DATABIN`
   - The DATABIN folder will now contain a bunch of files numbered 0000 to 6601
8. Copy your `fileMapping_FUCR_2g.csv` and `organize_FUCR.sh` files into `DATABIN`. We'll be using these two files to make the files a bit more readable.
9. Navigate into `DATABIN` and run the `organize_FUCR.sh` script, passing in the fileMapping document as a parameter
   - `./organize_FUCR.sh fileMapping_FUCR_2g.csv`
   - this will create subfolders within your DATABIN that help organize the files
   - The main files this patch will be editing are in the emmodel folder
     - These are monster files. We'll specifically be altering the texture files within these files.
10. Use the unpack bash script (located in your working directory) to call mhtools.jar to unpack all the .pac files in the emmodel folder by running the emmodel_unpack_FUCR.sh script
    - `./emmodel_unpack_FUCR.sh`
    - This will create additional subfolders in the emmodel folder - these are the unpacked versions of the monster files. You can go in and look at the image folders to see what the existing textures are going to look like. These are what we're going to change.
11. Okay, now we're going to take a little trip...
    - **EITHER** Copy all the folders in `emmodel` out to a new folder, then grab `colorPackInject.sh`, `colorize.py`, `DATA.BIN`, `mhtools.jar`, `data.py`, and `fileMapping_FUCR_2g.csv` and copy them there...
    - **OR** Grab `colorPackInject.sh`, `colorize.py`, `DATA.BIN`, `mhtools.jar`, `data.py`, and `fileMapping_FUCR_2g.csv` and copy them into your emmodel folder
12. create an empty folder called `colorized_pacs`
13. Navigate to the folder, then run `colorPackInject.sh`, passing in the fileMapping csv
    - `./colorPackInject.sh fileMapping_FUCR_2g.csv`
    - this script will run through the .csv file, pick up the emmodel folders, colorize the texture, pack them back up into .pac files, then inject them into DATA.BIN
    - .pac files will be copied into the `colorized_pacs` folder, ready to be used by the [File Replacer](https://github.com/FUComplete/FUCTool#file-replacer)
    - At this point (provided the command line didn't spit out too many errors) - you should be able to open up the image folders and see that the textures have been recolored. These have been injected into the DATA.BIN, so all that's left is to rebuild the image.
14. If you're rebuilding the .iso, use UMDGen and copy all the files from your original unpacking of the iso into it. Then, replace the DATA.BIN with the one we just injected (in the emmodel folder). Save as .iso and you're all ready to go!
15. If you're using the [File Replacer](https://github.com/FUComplete/FUCTool#file-replacer), then copy the .pac files and drop them in your mods folder, then use the FU Complete tool to create the nativePSP directory based on the mods.

### Creating Patches

You can use xdelta to create a patch if you happen to find a great set of randomized colors that you want to share.

- `./xdelta3.exe -e -v -s old_file new_file patch_file`
- `./xdelta3.exe -e -v -s MHP2G_FUC.iso MHP2G_FUCR_v1.0_01.iso MHP2G_FUCR_v1.0_01.xdelta`

## Notes

The file mapping csv contains 6 columns/values for each record.

- id - identifying number of the file - after we edit a file, we use this to make sure we inject it back into the right place
- file - this is where mhff's data.bin moves the file to. Filenames can be edited here as you wish, but note that they generally need to match off against the directory.
- directory - trimmed version of the file - this entry is used to flag which folders have textures to be colorized
- palleteSize - ~~can be set to change the spread of randomization; default is 6. Increasing creates more bands of color that will be changed independent of the other bands~~ No longer used.
- subId - id of a secondary file that should be colored with the same values as the primary. For example, colorizing velociprey so they have a similar colorization to velocidrome.
- subDirectory - trimmed version of the secondary filename; used to find the folder to be colored alongside the primary directory

## Special Thanks

- IncognitoMan for being available when I had questions as well as for their organization script and csv [here](https://gist.github.com/IncognitoMan/5606104bd3f4ab79c0e4e2f791acbda5)
- Codestation for [mhtools](https://github.com/codestation/mhtools)
- Svanheulen and IncognitoMan for [mhff](https://github.com/IncognitoMan/mhff)
- Capcom for creating Monster Hunter

## Credits

Nuzcraft - Development, Programming
