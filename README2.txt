# Freedom Unite Color Randomizer Patch

This is a mod/patch for Monster Hunter Portable 2nd G that will allow you to randomize the colors of the monsters. I've included files and instructions for how to colorize and patch your copy of the game which guarantees that you'll be fighting 100% unique monsters!

<div align="center">

<img src="https://github.com/nuzcraft/FreedomUniteColorRandomizer/assets/20135847/d41079ac-d094-4c78-8602-805389d74d69">

</div>

## How does the patch work?

The patch works by updating the texture file for each of the monsters with recolored ones. It tries to group similar colors together and update them so the monsters maintain some of their original shading. Colorization does not happen at runtime. I've provided batches of colorized monsters in patches and mod files that can be applied to your game.

## Applying the Patch

Make sure you use either a UMD dump or PSN version of `Monster Hunter Portable 2nd G`

All my development and testing was done with a version pre-patched with [FU Complete](https://github.com/FUComplete/Patch). The color randomization patch _should_ work on an unpatched version of MHP2G; I have not tested it.

### Option 1 - Use FUComplete File Replacer

---

For this option, we'll use IncognitoMan's [FU Complete](https://github.com/FUComplete/Patch). After downloading and running FU Complete on your copy of MHP2G, follow the directions [here](https://github.com/FUComplete/FUCTool#file-replacer) to start using the File Replacer.

1. Download the files from the most [recent release](https://github.com/nuzcraft/FreedomUniteColorRandomizer/releases/latest)
   - here, you should see at least one (if not multiple) .zip files labeled 'pacs'. These folders contain .pac mod files
2. Choose a .zip file and unzip it. Each represents a different randomization; you don't need to use them all
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
5. The new .iso is now patched and ready to play!

Alternatively, you can use IncognitoMan's [FU Complete patcher](https://github.com/FUComplete/Patch/releases/latest). Just copy the xdelta file into the directory with the other xdelta files use for patching FU Complete.

## Special Thanks

- IncognitoMan for being available when I had questions as well as for their organization script and csv [here](https://gist.github.com/IncognitoMan/5606104bd3f4ab79c0e4e2f791acbda5)
- Codestation for [mhtools](https://github.com/codestation/mhtools)
- Svanheulen and IncognitoMan for [mhff](https://github.com/IncognitoMan/mhff)
- Capcom for creating Monster Hunter

## Credits

Nuzcraft - Development, Programming

All code and instructions for creating your own custom colorizations are available in [the github repo](https://github.com/nuzcraft/FreedomUniteColorRandomizer/) for this project.
