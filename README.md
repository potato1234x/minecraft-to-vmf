# Minecraft to VMF
A python script to convert minecraft chunks into VMF files.

## Usage
This is a python script, find a tutorial on how to install python and run the .bat file to start.

- Paste in your world directory. This will be in C:/Users/(username)/AppData/Roaming/.minecraft/saves/(save name)
- Find the coordinates of the chunk to export, these will be in the F3 menu below the regular coordinates and copy them in. (the first and last numbers)
- Currently there is no brush optimisation, but it's coming. Hopefully.

## Future Features
These arent guaranteed but i'll hopefully get around to it, you could also make a PR if you know what you're doing.

- Brush optimisation (merging brushes/only converting blocks adjacent to air)
- Custom scale parameter
- Bulk chunk converting
- Automatic detection for multi texture blocks
- Persistent options
- Auto converting textures to vtfs
- Auto converting json models to mdls
- Auto generating skybox brushes
- Spawnpoints

## How to convert textures/models in the meantime

### Textures
- Extract the .jar of the version of your choice
- Go to assets/minecraft/textures/blocks/ and open a texture with the vtf editor of your choice.
- Export as uncompressed vtf with point sampling and no mipmap flags checked.
- Save in example_assets/materials/minecraft (unless its for a model in which case it goes in materials/models/minecraft)
- Make sure the vmt points to the right texture and right surface property.

### Models
- Extract the .jar of the version of your choice
- Go to assets/minecraft/models/blocks/ and open a json with blockbench.
- Export as obj.
- Open in blender and using source tools export and follow a blender to source model tutorial but in the qc file set the scale to 32 (or if you're reading this in the future, whatever size you want the blocks to be in HU)
- Save in example_assets/models/minecraft
