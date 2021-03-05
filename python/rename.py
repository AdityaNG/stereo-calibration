import numpy as np
import cv2
import os
import argparse
import csv
from shutil import copyfile

global args

parser = argparse.ArgumentParser(description='Convert CSV images to JPG')
parser.add_argument("--path", help="Path to the folder with the images to rename", default=os.path.abspath(os.path.curdir))
args = parser.parse_args()
print(args)

def main():
    path = args.path
    files_list = filter(lambda x: x.endswith(".jpg") or x.endswith(".png"), os.listdir(path))

    if files_list == []:
        print("No jpg files found")
        exit(1)

    for f in files_list:
        f_path = os.path.join(path, f)
        new_name = f

        file_type = ".jpg"
        if f.endswith(".png"):
            file_type = ".png"


        if "_left"+file_type in f:
            num = int(f.replace("_left" + file_type, ""))
            new_name = "left" + str(num) + file_type
        elif "_right"+file_type in f:
            num = int(f.replace("_right" + file_type, ""))
            new_name = "right" + str(num) + file_type
        else:
            print("Name error")
            exit(1)
        save_path = os.path.join(path, new_name) 
        print(f_path, "->", save_path, sep='\t')
        copyfile(f_path, save_path)
        
    pass

if __name__ == '__main__':
    main()

