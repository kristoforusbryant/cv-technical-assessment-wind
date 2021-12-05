#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-o", "--output", required = True, help = "Path to the image output")
args = vars(ap.parse_args())

def place_squares(img):
    img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    img_orig = img.copy()

    scale = 16
    dim = (int(img.shape[1] // scale), int(img.shape[0] // scale))
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray_edge = cv.Canny(gray, 20, 5)

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    _, s, _ = cv.split(hsv)
    s_edge = cv.Canny(s, 100, 5)

    # The image is sliced into 31 x 31 grids
    # For all images, the squares are located at the following grids:
    #   (1, 1), (2, 1), (3, 1), (4, 1), (1, 6), (2, 6), (3, 6), (4, 6)
    gs = 31 # grid size

    idxes = [(1, 1), (2, 1), (3, 1), (4, 1), (1, 6), (2, 6), (3, 6), (4, 6)]

    for i, j in idxes:
        if (i, j) in [(1, 1), (2, 1)]:
            edge = gray_edge
        else:
            edge = s_edge
        subset = edge[i*gs:(i+1)*gs, j*gs:(j+1)*gs + 10].copy()

        contours, _ = cv.findContours(subset, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        areas = [cv.contourArea(cnt) for cnt in contours]
        largest = np.argsort(areas)[-1]

        x,y,w,h = cv.boundingRect(contours[largest])

        # Drawing rectangles
        cv.rectangle(img_orig, ((gs * j + x) * scale, (gs * i + y) * scale),
                            ((gs * j + x + w) * scale, (gs * i + y + h) * scale), (0, 255, 0), 20)



    return img_orig

if __name__ == "__main__":
    img = cv.imread(args["image"])
    img = place_squares(img)
    cv.imwrite(args["output"], img)
