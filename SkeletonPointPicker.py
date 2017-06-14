import cv2
import numpy as np
import json
import sys
import os


isDrawing = False
bonePointList = []
boneIsTailList = []
COLORSTEP = np.array([0, 40, -40])


def ClickAndPickSkeleton(event, x, y, flags, param):
    global isDrawing
    global sourceImage, sourceClone
    global lastPoint
    global color, COLORSTEP
    global bonePointList, boneIsTailList
    global isRootBone

    # The starting point of part root
    if event == cv2.EVENT_RBUTTONDOWN:
        isDrawing = True
        color = np.array([0, 0, 255])
        cv2.circle(sourceClone, (x, y), 1, color, 2)
        cv2.imshow("sourceImage", sourceClone)
        lastPoint = (x, y)
        bonePointList.append((x, y))
        # If you click rightButton, then last bone is tail.
        isRootBone = True
        if len(boneIsTailList) > 1:
            boneIsTailList[-1] = True

    # Child bones of part root
    if event == cv2.EVENT_LBUTTONDOWN:
        if isDrawing:
            color = color + COLORSTEP
            cv2.circle(sourceClone, (x, y), 1, color, 2)
            cv2.line(sourceClone, lastPoint, (x, y), color, 2)
            cv2.imshow("sourceImage", sourceClone)
            lastPoint = (x, y)
            bonePointList.append((x, y))
            # If you click leftButton, then add a new bone.
            if isRootBone:
                isRootBone = False
            else:
                boneIsTailList[-1] = False

            boneIsTailList.append(True)

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


def UnDo():
    #global bonePointList, boneIsTailList

    #bonePointList = bonePointList[0:-1]
    #boneIsTailList = boneIsTailList[0:-1]
    pass


def main():
    global isDrawing
    global sourceImage, sourceClone
    global bonePointList
    global lastPoint
    global color, COLORSTEP
    global fileName

    fileName = GetFileName(sys.argv[1])

    sourceImage = cv2.imread("Pictures/" + sys.argv[1])
    sourceClone = sourceImage.copy()

    cv2.namedWindow("sourceImage", cv2.WINDOW_NORMAL or cv2.WINDOW_GUI_NORMAL or cv2.WINDOW_KEEPRATIO)
    cv2.imshow("sourceImage", sourceImage)
    cv2.setMouseCallback("sourceImage", ClickAndPickSkeleton)

    while True:
        key = cv2.waitKey(0)

        if key == 27:  # ESC
            isDrawing = False
            bonePointList = []
            sourceClone = sourceImage.copy()
            cv2.imshow("sourceImage", sourceClone)

        if key == 32:  # Spacebar
            with open('Skeleton/' + fileName + '.json', 'w') as outfile:
                json.dump(bonePointList, outfile)

            with open('boneInformation.json', 'w') as outfile:
                json.dump({'isTail': boneIsTailList, 'boneBelongsToPart': []}, outfile,
                          sort_keys=False, indent=4)

            # Save the notation image to /Results folder
            cv2.imwrite("Results/" + fileName + ".result.png", sourceClone)
            break

        # undo
        if key == 8:  # Backspace
            UnDo()

    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == '__main__':
    main()
