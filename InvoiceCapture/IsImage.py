# -*- coding: utf-8 -*-



    
#    ------
    
    
import imghdr

print(imghdr.what('geeksforgeeks.png'))

# ---------

import filetype

filename = "geeksforgeeks.png"

if filetype.is_image(filename):
    print(f"{filename} is a valid image...")
    
elif filetype.is_video(filename):
    print(f"{filename} is a valid video...")
    
    
    
filetype.is_image("gmail.py")
filetype.is_video(filename)
