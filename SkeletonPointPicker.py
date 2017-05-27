import cv2
import numpy as np
import json
import sys
import os


isDrawing = False
skeletonPointList = []
COLORSTEP = np.array([0, 40, -40])


def ClickAndPickSkeleton(event, x, y, flags, param):
    global isDrawing
    global sourceImage, sourceClone
    global lastPoint
    global color, COLORSTEP
    global skeletonPointList

    # The starting point of part root
    if event == cv2.EVENT_RBUTTONDOWN:
        isDrawing = True
        color = np.array([0, 0, 255])
        cv2.circle(sourceClone, (x, y), 1, color, 2)
        cv2.imshow("sourceImage", sourceClone)
        lastPoint = (x, y)
        skeletonPointList.append((x, y))

    # Child bones of part root
    if event == cv2.EVENT_LBUTTONDOWN:
        if isDrawing:
            color = color + COLORSTEP
            cv2.circle(sourceClone, (x, y), 1, color, 2)
            cv2.line(sourceClone, lastPoint, (x, y), color, 2)
            cv2.imshow("sourceImage", sourceClone)
            lastPoint = (x, y)
            skeletonPointList.append((x, y))

    # Bone preview
    elif event == cv2.EVENT_MOUSEMOVE:
        if isDrawing:
            tempImage = sourceClone.copy()
            overlay = sourceClone.copy()
            alpha = 0.3

            cv2.line(overlay, lastPoint, (x, y), color, 2)

            cv2.addWeighted(overlay, alpha, tempImage, 1 - alpha, 0, tempImage)
            cv2.imshow("sourceImage", tempImage)


def GetFileName(path):
    fileName = os.path.splitext(path)[0]
    return fileName


def main():
    global isDrawing
    global sourceImage, sourceClone
    global skeletonPointList
    global lastPoint
    global color, COLORSTEP
    global fileName

    fileName = GetFileName(sys.argv[1])

    sourceImage = cv2.imread("Pictures/" + sys.argv[1])
    sourceClone = sourceImage.copy()

    cv2.namedWindow("sourceImage")
    cv2.imshow("sourceImage", sourceImage)
    cv2.setMouseCallback("sourceImage", ClickAndPickSkeleton)

    while True:
        key = cv2.waitKey(0)

        if key == 27:  # ESC
            isDrawing = False
            skeletonPointList = []
            sourceClone = sourceImage.copy()
            cv2.imshow("sourceImage", sourceClone)

        if key == 32:  # Spacebar
            with open('Skeleton/' + fileName + '.json', 'w') as outfile:
                json.dump(skeletonPointList, outfile)

            # Save the notation image to /Results folder
            cv2.imwrite("Results/" + fileName + ".result.png", sourceClone)
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    main()
