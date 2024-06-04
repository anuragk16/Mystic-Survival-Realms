import pygame
import os
from maps import MAP
from PIL import Image
from numpy import asarray,empty
import sys

def levels(level:int=1):
    img = Image.open(f'assets\\images\\level{level}.png')
    numpyd = asarray(img)
    a = MAP(numpyd.shape[1],numpyd.shape[0])
    numpydata = numpyd.astype(str)
    
    # Define replacement dictionaries for different pixel values
    replacements = {
        ("34" ,"32" ,"52", "255"): "O",     # obstacals
        ("0" ,"0" ,"0" ,"255"): "B",        # background
        ("91" ,"110" ,"225", "255"): "P",   # player
        ("118" ,"66" ,"138" ,"255"): "C",   # chest
        ("106", "190", "48", "255"): "T",   # trees
        ("203", "219" ,"252", "255"): "E",  # Enemy level 2
        ("255", "255" ,"255","255"): "e",   # enemy level 1
        ("138", "111" ,"48","255"): "D",    # dungeon
        ("69", "40" ,"60","255"): "R",      # rock
        ("172", "50" ,"50","255"): "G"    # boss
    }
    
    # Create a new array to hold the replaced values
    replaced_array = empty(numpydata.shape[0:2], dtype='<U1')
    
    # Iterate over each pixel
    for y in range(numpydata.shape[0]):
        for x in range(numpydata.shape[1]):
            pixel = tuple(numpydata[y][x])
            if pixel in replacements:
                replaced_array[y][x] = replacements[pixel]
            else:
                replaced_array[y][x] = '.'  # Or any default value you want for unmatched pixels
                
    #print(replaced_array)
    numpydata_list = replaced_array.tolist()
    
    # Assuming each 'tile' in your map_array is a 32x32 block
    tile_size = 32
    width, height, map_array = a.get_map_dimensions()
    
    # Update the map array with the new values
    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            tile_y = y // tile_size
            tile_x = x // tile_size
            # Check if the tile coordinates are within the bounds of the numpydata_list
            #if tile_y < len(numpydata_list) and tile_x < len(numpydata_list[0]):
                # Update the map_array with the corresponding value from numpydata_list
            map_array[tile_y*32][tile_x*32] = numpydata_list[tile_y][tile_x]
        
   
    
    return width, height, map_array, a
    
    

