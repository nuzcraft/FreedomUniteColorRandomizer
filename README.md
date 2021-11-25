Good Day!

What you'll need to create this patch:

- MHP2G iso
  This has been developed and tested using MHP2G with an english patch applied. I've not tested it on my unpatched file yet. This is the patch I'm using: FU Complete (https://github.com/FUComplete)
- mhff(https://github.com/IncognitoMan/mhff) data.py file for psp
- mhtools(https://github.com/codestation/mhtools) mhtools.jar file

## Steps

1. Create a new folder, you'll use this as your working directory
2. Extract the files from your MHP2G iso into your working directory. I use 7-Zip, but you can use whatever you want. It doesn't really matter what depth these files are at, so housing them in a subfolder is fine.
3. Copy PSP_GAME/USRDIR/DATA.BIN out into your working directory
4. Create a new folder in your working directory called DATABIN
5. Use the data.py file from mhff to extract the files from DATA.BIN into a folder called DATABIN
   - python data.py a DATA.BIN DATABIN
   - The DATABIN folder will now contain a bunch of files numbered 0000 to 6601
6. Copy your fileMapping_FUCR_2g.csv and organize_FUCR.sh files into DATABIN. We'll be using these two files to make the files a bit more readable.
7. Navigate into DATABIN and run the organize_FUCR.sh script, passing in the fileMapping document as a parameter
   - ./organize_FUCR.sh fileMapping_FUCR_2g.csv
   - this will create subfolders within your DATABIN that help organize the files
   - The main files this patch will be editing are in the 'emmodel' folder; these are monster files. We'll specifically be altering the texture files
8. Use mhtools.jar (located in your working directory) to unpack all the .pac files in the 'emmodel' folder by running the emmodel_unpack_FUCR.sh script
   - ./emmodel_unpack_FUCR.sh
   - This will create additional subfolders in the emmodel folder - these are the unpacked versions of the monster files. You can go in and look at the image folders to see what the existing textures are going to look like. This is what we're going to change.
9. Okay, now we're going to take a little trip.
   - EITHER Copy all the folders in emmodel out to a new folder, then grab cpi.sh, colorize.py, DATA.BIN, mhtools.jar, data.py, and fileMapping_FUCR_2g.csv and copy them there...
   - OR Grab cpi.sh, colorize.py, DATA.BIN, mhtools.jar, data.py, and fileMapping_FUCR_2g.csv and copy them into your emmodel folder
10. Navigate to the folder, then run cpi.sh, passing in the fileMapping csv
    - ./cpi.sh fileMapping_FUCR_2g.csv
    - At this point (provided the command line didn't spit out too many errors) - you should be able to open up the image folders and see that the textures have been recolored. These have been injected into the DATA.BIN, so all that's left is to rebuild the image.
11. Use UMDGen and copy all the files from your original unpacking of the iso into it. Then, replace the DATA.BIN with the one we just injected (in the emmodel folder). Save as .iso and you're all ready to go!

## Special Thanks

- the organize.sh script from here: https://gist.github.com/IncognitoMan/5606104bd3f4ab79c0e4e2f791acbda5 (also included in this codebase)
