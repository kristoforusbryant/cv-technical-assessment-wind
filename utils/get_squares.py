#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-o", "--output", required = True, help = "Path to the image output")
args = vars(ap.parse_args())

def place_circle(img):
    img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    img_orig = img.copy()

    scale = 16
    dim = (int(img.shape[1] // scale), int(img.shape[0] // scale))
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    # The image is sliced into 31 x 31 grids
    # For all images, the squares are located at the following grids:
    #   (1, 1), (2, 1), (3, 1), (4, 1), (1, 6), (2, 6), (3, 6), (4, 6)
    gs = 31 # grid size

    # Use Green Channel for the grid (2, 1)
    i, j = 2, 1
    _, g, _ = cv.split(img)
    subset = g[i*gs:(i+1)*gs, j*gs + 10:(j+1)*gs].copy()
    subset = cv.medianBlur(subset, 3)
    _, thresh = cv.threshold(subset, np.mean(subset.flatten()), 255, cv.THRESH_BINARY_INV)
    padded = np.zeros((thresh.shape[0] + 2, thresh.shape[1] + 2), dtype='uint8')
    padded[1:-1, 1:-1] = thresh

    contours, _ = cv.findContours(padded, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    areas = [cv.contourArea(cnt) for cnt in contours]
    largest = np.argsort(areas)[-1]

    x,y,w,h = cv.boundingRect(contours[largest])
    x, y = x - 1, y - 1 # Taking into account padding
    x, y, w, h = x + 1, y + 1, w - 1, h - 1 # More conservative by using smaller bounding box

    # Drawing rectangles
    cv.rectangle(img_orig, ((gs * j + x + 10) * scale, (gs * i + y) * scale),
                        ((gs * j + x + 10 + w) * scale, (gs * i + y + h) * scale), (0, 255, 0), 20)


    # Use saturation channel for the following grids
    idxes = [(3, 1), (4, 1), (1, 6), (2, 6), (3, 6), (4, 6)]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    _, s, _ = cv.split(hsv)

    for i, j in idxes:
        subset = s[i*gs:(i+1)*gs, j*gs:(j+1)*gs].copy()
        subset = cv.GaussianBlur(subset, (3, 3), 0)
        _, thresh = cv.threshold(subset, np.mean(subset.flatten()), 255, cv.THRESH_BINARY_INV)
        padded = np.zeros((thresh.shape[1] + 2, thresh.shape[1] + 2), dtype='uint8') + 255
        padded[1:-1, 1:-1] = thresh

        contours, _ = cv.findContours(padded, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        areas = [cv.contourArea(cnt) for cnt in contours]
        snd_largest = np.argsort(areas)[-2]

        x,y,w,h = cv.boundingRect(contours[snd_largest])
        x, y = x - 1, y - 1 # Taking into account padding
        x, y, w, h = x + 1, y + 1, w - 1, h - 1 # More conservative by using smaller bounding box

        # Drawing rectangles
        cv.rectangle(img_orig, ((gs * j + x) * scale, (gs * i + y) * scale),
                            ((gs * j + x + w) * scale, (gs * i + y + h) * scale), (0, 255, 0), 20)

    return img_orig

if __name__ == "__main__":
    img = cv.imread(args["image"])
    img = place_circle(img)
    cv.imwrite(args["output"], img)
