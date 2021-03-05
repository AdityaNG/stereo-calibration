import numpy as np
import cv2
import os
import argparse
import csv

global args

parser = argparse.ArgumentParser(description='Find checkerboard in JPG images')
parser.add_argument("--path", help="Path to the folder with the images to rename", default=os.path.abspath(os.path.curdir))
parser.add_argument("--width", help="Pattern width", default=8)
parser.add_argument("--height", help="Pattern height", default=8)
parser.add_argument("-i", help="File name", default="left")
parser.add_argument("-o", help="Output file", default="cam_left.yml")
args = parser.parse_args()
print(args)

def increase_contrast(img):
    #-----Reading the image-----------------------------------------------------
    # img = cv2.imread('Dog.jpg', 1)
    # cv2.imshow("img",img) 

    #-----Converting image to LAB Color model----------------------------------- 
    lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    # cv2.imshow("lab",lab)

    #-----Splitting the LAB image to different channels-------------------------
    l, a, b = cv2.split(lab)
    # cv2.imshow('l_channel', l)
    # cv2.imshow('a_channel', a)
    # cv2.imshow('b_channel', b)

    #-----Applying CLAHE to L-channel-------------------------------------------
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(3,3))
    cl = clahe.apply(l)
    # cv2.imshow('CLAHE output', cl)

    #-----Merge the CLAHE enhanced L-channel with the a and b channel-----------
    limg = cv2.merge((cl,a,b))
    # cv2.imshow('limg', limg)

    #-----Converting image from LAB Color model to RGB model--------------------
    final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    # cv2.imshow('final', final)

    #_____END_____#
    return final

def main(path, w, h, i, o):
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*7,3), np.float32)
    objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
    # Arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.<Paste>
    files_list = filter(lambda x: x.endswith(".jpg") or x.endswith("png"), os.listdir(path))

    if files_list == []:
        print("No jpg files found")
        exit(1)

    for f in files_list:
        f_path = os.path.join(path, f)
        img_orig = cv2.imread(f_path, cv2.IMREAD_GRAYSCALE)
        img_color = cv2.imread(f_path)
        # img_color = increase_contrast(img_color)
        img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
        # img = cv2.imread(f_path, cv2.IMREAD_GRAYSCALE)
        
        # img = cv2.equalizeHist(img)
        # img = cv2.Canny(img, 100, 200)
        
        kernel = np.ones((5, 5), np.uint8)
        # img = cv2.dilate(img, kernel, iterations = 1)

        kernel = np.ones((5, 5), np.uint8)
        # img = cv2.erode(img, kernel, iterations = 1)

        # img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        # img = cv2.medianBlur(img, 3)

        gray = img
        ret, corners = cv2.findChessboardCorners(gray, (w, h), None)
        if ret == True:
            print("Checkerboard FOUND", f, sep='\t')
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (7,6), corners2, ret)
        else:
            print("Checkerboard not found", f, sep='\t')
        cv2.imshow('img_color', img_color)
        cv2.imshow('img', img)
        cv2.waitKey(500)
	
    pass

if __name__ == '__main__':
    main(args.path, int(args.width), int(args.height), args.i, args.o)

