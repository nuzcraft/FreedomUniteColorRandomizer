sed 's/"//g' $1 | while IFS=, read id file directory paletteSize subId subDirectory; 
do
echo "moving and renaming $id to $file" 
mkdir -p $(dirname "$file") && cp "$id" "$file"; 
done