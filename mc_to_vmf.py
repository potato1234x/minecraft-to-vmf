import anvil
import os

world_directory_input = input("World Directory: ")
world_directory = f"{world_directory_input}" + r"\region"

chunk_x = int(input("chunk to export x coord: "))

chunk_z = int(input("chunk to export z coord: "))

# material mapping
block_to_material = {
    "grass_block_top": "minecraft/grass_block_top",
    "grass_block_side": "minecraft/grass_block_side",
    "dirt": "minecraft/dirt",
    "stone": "minecraft/stone",
}

# vmf header
def generate_vmf_header():
    return """versioninfo
{
    "editorversion" "400"
    "editorbuild" "6444"
    "mapversion" "1"
    "formatversion" "100"
    "prefab" "0"
}
viewsettings
{
    "bSnapToGrid" "1"
    "bShowGrid" "1"
    "bShowLogicalGrid" "0"
    "nGridSpacing" "64"
}
world
{
    "id" "1"
    "mapversion" "1"
    "classname" "worldspawn"
    "detailmaterial" "detail/detailsprites"
    "detailvbsp" "detail.vbsp"
    "maxpropscreenwidth" "-1"
    "skyname" "sky_day01_01"
"""

# block to brush
def convert_block_to_vmf(block_id, solid_id, x_offset, y_offset, z_offset):
    # multi texture side blocks
    if block_id == "grass_block":
        top_material = "minecraft/grass_block_top"
        side_material = "minecraft/grass_block_side"
        bottom_material = "minecraft/dirt"
    else:
        if block_id == "birch_log":
            top_material = bottom_material = "minecraft/birch_log_top"
            side_material = "minecraft/birch_log"
        else:
            # Default behavior for all other blocks
            if block_id in block_to_material:
                top_material = side_material = bottom_material = block_to_material[block_id]
            else:
                top_material = side_material = bottom_material = "MINECRAFT/" + block_id.upper()  # default mat
                print(block_id + " is not in material list! Trying MINECRAFT/" + block_id.upper())

    # Return a solid for normal blocks
    return f"""
    solid
    {{
        "id" "{solid_id}"
        side
        {{
            "id" "{solid_id + 1}"
            "plane" "({x_offset - 16} {y_offset - 16} {z_offset + 16}) ({x_offset - 16} {y_offset + 16} {z_offset + 16}) ({x_offset + 16} {y_offset + 16} {z_offset + 16})"
            "material" "{top_material}"
            "uaxis" "[1 0 0 8] -2"
            "vaxis" "[0 -1 0 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        side
        {{
            "id" "{solid_id + 2}"
            "plane" "({x_offset - 16} {y_offset + 16} {z_offset - 16}) ({x_offset - 16} {y_offset - 16} {z_offset - 16}) ({x_offset + 16} {y_offset - 16} {z_offset - 16})"
            "material" "{bottom_material}"
            "uaxis" "[1 0 0 8] 2"
            "vaxis" "[0 -1 0 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        side
        {{
            "id" "{solid_id + 3}"
            "plane" "({x_offset - 16} {y_offset - 16} {z_offset - 16}) ({x_offset - 16} {y_offset + 16} {z_offset - 16}) ({x_offset - 16} {y_offset + 16} {z_offset + 16})"
            "material" "{side_material}"
            "uaxis" "[0 1 0 8] -2"
            "vaxis" "[0 0 -1 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        side
        {{
            "id" "{solid_id + 4}"
            "plane" "({x_offset + 16} {y_offset + 16} {z_offset - 16}) ({x_offset + 16} {y_offset - 16} {z_offset - 16}) ({x_offset + 16} {y_offset - 16} {z_offset + 16})"
            "material" "{side_material}"
            "uaxis" "[0 1 0 8] 2"
            "vaxis" "[0 0 -1 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        side
        {{
            "id" "{solid_id + 5}"
            "plane" "({x_offset - 16} {y_offset + 16} {z_offset - 16}) ({x_offset + 16} {y_offset + 16} {z_offset - 16}) ({x_offset + 16} {y_offset + 16} {z_offset + 16})"
            "material" "{side_material}"
            "uaxis" "[1 0 0 8] -2"
            "vaxis" "[0 0 -1 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        side
        {{
            "id" "{solid_id + 6}"
            "plane" "({x_offset + 16} {y_offset - 16} {z_offset - 16}) ({x_offset - 16} {y_offset - 16} {z_offset - 16}) ({x_offset - 16} {y_offset - 16} {z_offset + 16})"
            "material" "{side_material}"
            "uaxis" "[1 0 0 8] 2"
            "vaxis" "[0 0 -1 8] 2"
            "rotation" "0"
            "lightmapscale" "16"
            "smoothing_groups" "0"
        }}
        editor
        {{
            "color" "0 246 103"
            "visgroupshown" "1"
            "visgroupautoshown" "1"
        }}
    }}
"""

# vmf footer
def generate_brush_footer():
    return """}
"""

# grass to prop_static
def convert_grass_to_entity(entity_id, x_offset, y_offset, z_offset):
    return f"""
entity
{{
    "id" "{entity_id}"
    "classname" "prop_static"
	"disableshadows" "1"
    "origin" "{x_offset} {y_offset} {z_offset}"
    "model" "models/minecraft/grass.mdl"
    "solid" "6"
}}
"""

# vmf footer
def generate_vmf_footer():
    return """
cameras
{
    "activecamera" "-1"
}
cordon
{
    "mins" "(-10240 -10240 -10240)"
    "maxs" "(10240 10240 10240)"
    "active" "0"
}
"""

# main function
def minecraft_chunk_to_vmf(chunk_x, chunk_z, world_directory, output_file):
    # find region file
    region_file = os.path.join(world_directory, f"r.{chunk_x // 32}.{chunk_z // 32}.mca")

    # loader
    try:
        region = anvil.Region.from_file(region_file)
    except Exception as e:
        print(f"Error loading region file: {region_file}. Exception: {e}")
        return
    
    # try get chunk
    try:
        chunk = region.get_chunk(chunk_x % 32, chunk_z % 32)
    except KeyError as e:
        print(f"Error loading chunk at ({chunk_x}, {chunk_z}) in {region_file}: {e}")
        return
    
    with open(output_file, 'w') as vmf:
        # write header
        vmf.write(generate_vmf_header())
        
        id_counter = 2  # assuming id 1 is for worldspawn

        # find entities
        entity_data = ""
        
        # loop through all blocks in the chunk and write them as vmf brushes or entities
        for x in range(16):  # chunks are 16x16 blocks
            for z in range(16):
                for y in range(0, 100):  # height to convert
                    block = chunk.get_block(x, y, z)
                    if block.id != "air":  # skip air blocks
                        if block.id == "grass" or block.id == "tall_grass":  # grass becomes prop
                            entity_data += convert_grass_to_entity(id_counter, x * 32, z * -32, y * 32)
                        else:
                            # blockpos to offset
                            vmf.write(convert_block_to_vmf(block.id, id_counter, x * 32, z * -32, y * 32))
                        id_counter += 1

        # write the brush footer
        vmf.write(generate_brush_footer())
        
        # write all the collected entities after solids
        vmf.write(entity_data)

        # write the VMF footer
        vmf.write(generate_vmf_footer())
    
    print("Completed with " + str(id_counter - 1) + " total solids and entities written.")

# Example usage:
minecraft_chunk_to_vmf(chunk_x, chunk_z, world_directory, 'output.vmf')  # replace with desired chunk coordinates
