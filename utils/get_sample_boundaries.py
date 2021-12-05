#!/usr/bin/env python3

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
ap.add_argument("-o", "--output", required = True, help = "Path to the image output")
args = vars(ap.parse_args())

def get_boundary(img):
    img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
    img_orig = img.copy()

    scale = 16
    dim = (int(img.shape[1] // scale), int(img.shape[0] // scale))
    img = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    img = cv.GaussianBlur(img, (3, 3), 0)

    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Getting circle
    circs = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, 100, minRadius=43, maxRadius=63)
    circ = [int(round(c)) for c in circs[0][0]]

    blank = np.zeros(img.shape[:2], dtype='uint8')
    mask = cv.circle(blank, (circ[0], circ[1]), circ[2] - 5, 255, -1)

    edge = cv.Canny(gray, 50, 5)
    masked_edge = cv.bitwise_and(edge, mask)

    contours = cv.findContours(masked_edge, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    areas = [cv.contourArea(cnt) for cnt in contours[0]]
    sorted = np.flip(np.argsort(areas))
    contours = [cnt * scale for cnt in contours[0]]

    cnt = np.concatenate([contours[i] for i in sorted])
    chull = cv.convexHull(cnt)
    cv.drawContours(img_orig, [chull], -1, (0, 255, 0), 20)

    # Getting histogram
    blank = np.zeros(img_orig.shape[:2], np.uint8)
    hmask = cv.drawContours(blank, np.array([np.squeeze(chull)]), -1, 255, cv.FILLED)
    idx = hmask == 255

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    ax.hist(img_orig[idx, 0], alpha=.5, color='red', density=True, bins=250)
    ax.hist(img_orig[idx, 1], alpha=.5, color='green', density=True, bins=250)
    ax.hist(img_orig[idx, 2], alpha=.5, color='blue', density=True, bins=250)
    ax.set_xlim(0, 255)

    ax.set_title(f"Color Histogram of Sample in ", fontsize=20)
    ax.set_ylabel("Density", fontsize=18)
    ax.set_xlabel("Channel Values", fontsize=18)

    fig.savefig(args["output"][:-4] +  "_histogram.jpg")

    return img_orig

if __name__ == "__main__":
    img = cv.imread(args["image"])
    img = get_boundary(img)
    cv.imwrite(args["output"], img)
