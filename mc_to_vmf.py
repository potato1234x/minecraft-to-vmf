import anvil
import os

world_directory_input = input("World Directory: ")
world_directory = f"{world_directory_input}" + r"\region"

# Input chunk coordinates
chunk_x1, chunk_z1 = map(int, input("Enter the first chunk coordinates (x1 z1): ").split())
chunk_x2, chunk_z2 = map(int, input("Enter the second chunk coordinates (x2 z2): ").split())

nonsolid_blocks = ["air", "cave_air", "water", "lava", "grass", "seagrass", "tall_seagrass", "short_grass", "tall_grass", "peony", "oak_leaves", "birch_leaves", "spruce_leaves", "jungle_leaves", "dark_oak_leaves", "acacia_leaves", "mangrove_leaves"]

# VMF header
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
    if block_id == "grass_block":
        top_material = "minecraft/grass_block_top"
        side_material = "minecraft/grass_block_side"
        bottom_material = "minecraft/dirt"
    else:
        if block_id == "birch_log":
            top_material = bottom_material = "minecraft/birch_log_top"
            side_material = "minecraft/birch_log"
        else:
            top_material = side_material = bottom_material = "MINECRAFT/" + block_id.upper()
            print("Writing block " + block_id + " with material MINECRAFT/" + block_id.upper())

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

# VMF footer
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

# VMF footer
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

# check if a block is adjacent to a nonsolid block
def is_adjacent_to_nonsolid(region, chunk_x, chunk_z, chunk, x, y, z, nonsolid_blocks, world_directory, region_cache, chunk_cache):
    for dx, dy, dz in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        adjacent_x, adjacent_y, adjacent_z = x + dx, y + dy, z + dz

        # determine the neighboring chunk's coordinates
        neighbor_chunk_x = chunk_x
        neighbor_chunk_z = chunk_z
        
        # handle neighboring chunks
        if adjacent_x < 0:
            adjacent_x += 16
            neighbor_chunk_x -= 1
        elif adjacent_x >= 16:
            adjacent_x -= 16
            neighbor_chunk_x += 1

        if adjacent_z < 0:
            adjacent_z += 16
            neighbor_chunk_z -= 1
        elif adjacent_z >= 16:
            adjacent_z -= 16
            neighbor_chunk_z += 1

        try:
            # check if we're crossing region boundaries
            region_x = neighbor_chunk_x // 32
            region_z = neighbor_chunk_z // 32
            current_region_x = chunk_x // 32
            current_region_z = chunk_z // 32

            # check if the neighboring region is already cached
            if (region_x, region_z) not in region_cache:
                if region_x != current_region_x or region_z != current_region_z:
                    # load the neighboring region file only if necessary
                    region_file = os.path.join(world_directory, f"r.{region_x}.{region_z}.mca")
                    try:
                        neighboring_region = anvil.Region.from_file(region_file)
                        region_cache[(region_x, region_z)] = neighboring_region
                    except Exception:
                        continue  # treat missing region as non-target
                else:
                    # if in the same region, use the current region
                    region_cache[(region_x, region_z)] = region
            
            neighboring_region = region_cache[(region_x, region_z)]

            # check if the neighboring chunk is already cached
            if (neighbor_chunk_x, neighbor_chunk_z) not in chunk_cache:
                try:
                    neighboring_chunk = neighboring_region.get_chunk(neighbor_chunk_x % 32, neighbor_chunk_z % 32)
                    chunk_cache[(neighbor_chunk_x, neighbor_chunk_z)] = neighboring_chunk
                except Exception:
                    continue  # treat missing chunk as non-target
            else:
                neighboring_chunk = chunk_cache[(neighbor_chunk_x, neighbor_chunk_z)]

            adjacent_block = neighboring_chunk.get_block(adjacent_x % 16, adjacent_y, adjacent_z % 16)

            if adjacent_block.id in nonsolid_blocks:
                return True

        except Exception:
            continue  # treat missing chunk/block as non-target

    return False


# main function to convert chunks to VMF
def minecraft_chunk_to_vmf(chunk_x1, chunk_z1, chunk_x2, chunk_z2, world_directory, output_file, convert_if_adjacent_to_air=True):
    region_cache = {}  # Cache for region files
    chunk_cache = {}   # Cache for chunks

    with open(output_file, 'w') as vmf:
        # write header
        vmf.write(generate_vmf_header())
        
        id_counter = 2  # assuming id 1 is for worldspawn
        entity_data = ""

        # iterate over the range of chunks from (chunk_x1, chunk_z1) to (chunk_x2, chunk_z2)
        for chunk_x in range(chunk_x1, chunk_x2 + 1):
            for chunk_z in range(chunk_z1, chunk_z2 + 1):
            
                # determine which region file this chunk belongs to
                region_x = chunk_x // 32
                region_z = chunk_z // 32
                
                region_file = os.path.join(world_directory, f"r.{region_x}.{region_z}.mca")

                # loader
                try:
                    region = anvil.Region.from_file(region_file)
                    region_cache[(region_x, region_z)] = region  # Cache the region
                except Exception as e:
                    print(f"Error loading region file: {region_file}. Exception: {e}")
                    continue  # Skip to the next chunk if there's an error
                
                # try to get the chunk for the current coordinates
                try:
                    chunk = region.get_chunk(chunk_x % 32, chunk_z % 32)
                    chunk_cache[(chunk_x, chunk_z)] = chunk  # Cache the chunk
                except KeyError as e:
                    print(f"Error loading chunk at ({chunk_x}, {chunk_z}) in {region_file}: {e}")
                    continue  # Skip to the next chunk if there's an error

                # loop through all blocks in the chunk and write them as vmf brushes or entities
                for x in range(16):  # chunks are 16x16 blocks
                    for z in range(16):
                        for y in range(50, 80):  # adjusted the height range from -63 to 319
                            block = chunk.get_block(x, y, z)
                            if block.id != "air" and block.id != "cave_air" and block.id != "water":  # Skip air blocks
                                if convert_if_adjacent_to_air:
                                    if not is_adjacent_to_nonsolid(region, chunk_x, chunk_z, chunk, x, y, z, nonsolid_blocks, world_directory, region_cache, chunk_cache):
                                        continue  # Skip blocks not adjacent to air
                                
                                if block.id in ["grass", "short_grass", "tall_grass"]:  # Grass becomes prop
                                    entity_data += convert_grass_to_entity(id_counter, (x * 32) + (chunk_x * 512), (z * -32) + (chunk_z * -512), y * 32)
                                else:
                                    # blockpos to offset
                                    vmf.write(convert_block_to_vmf(block.id, id_counter, (x * 32) + (chunk_x * 512), (z * -32) + (chunk_z * -512), y * 32))
                                id_counter += 1

        # write the brush footer
        vmf.write(generate_brush_footer())
        
        # write all the collected entities after solids
        vmf.write(entity_data)

        # write the VMF footer
        vmf.write(generate_vmf_footer())
    
    print("Completed with " + str(id_counter - 1) + " total solids and entities written.")

minecraft_chunk_to_vmf(chunk_x1, chunk_z1, chunk_x2, chunk_z2, world_directory, 'output.vmf', True)
