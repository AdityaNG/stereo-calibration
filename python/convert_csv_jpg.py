import numpy as np
import cv2
import os
import argparse
import csv

global args

parser = argparse.ArgumentParser(description='Convert CSV images to JPG')
parser.add_argument("--path", help="Path to the folder with the CSV images", default=os.path.abspath(os.path.curdir))
args = parser.parse_args()
print(args)

def main():
    path = args.path
    files_list = filter(lambda x: x.endswith(".csv"), os.listdir(path))

    if files_list == []:
        print("No CSV files found")
        exit(1)

    for f in files_list:
        f_path = os.path.join(path, f)
        save_path = os.path.join(path, f.replace(".csv", ".jpg")) 
        print(f_path)
        
        image = np.zeros((240,320,1), np.uint8) 

        with open(f_path, newline="") as csvfile:
            # reader = csv.DictReader(csvfile)
            reader = csvfile
            line = reader.readline()
            row_counter = 0
            cols_counter = 0
            while line!='':
                # print(len(line))
                if len(line) == 4161:
                    row_vals = list(map(float, line.split(",")))
                    for x, pix in enumerate(row_vals):
                        image[row_counter, x] = pix
                    cols_counter = len(row_vals)
                    row_counter += 1
                    # print(row_vals)
                line = reader.readline()

            # print(row_counter, cols_counter)
        cv2.imshow('Image',image)
        cv2.waitKey(0)
        cv2.imwrite(save_path, image)

    pass

if __name__ == '__main__':
    main()

