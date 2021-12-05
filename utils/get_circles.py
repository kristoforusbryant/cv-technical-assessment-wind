#!/usr/bin/env python3

import cv2 as cv
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
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Getting circle
    circs = cv.HoughCircles(img, cv.HOUGH_GRADIENT, 1, 100, minRadius=43, maxRadius=63)
    circ = [int(round(c) * scale) for c in circs[0][0]]

    # Drawing circle
    cv.circle(img_orig, (circ[0], circ[1]), circ[2], (0, 255, 0), 20)
    cv.rectangle(img_orig, (circ[0] - 25, circ[1] - 25), (circ[0] + 25, circ[1] + 25), (0, 0, 255), -1)
    cv.line(img_orig, (circ[0], circ[1]), (circ[0] + circ[2], circ[1]), (0, 0, 255), 6)
    cv.putText(img_orig, f'radius: {circ[2]}', (circ[0] + 100, circ[1] - 50), cv.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 5)

    return img_orig

if __name__ == "__main__":
    img = cv.imread(args["image"])
    img = place_circle(img)
    cv.imwrite(args["output"], img)
