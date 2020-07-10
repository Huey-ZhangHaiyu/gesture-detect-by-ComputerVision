"""
415 final project
Haiyu Zhang
last date:12/03/2019
"""
"""
This code contains image processing and keyboard detect
"""

from cv2 import cv2
import numpy as np
import math
import copy
import game

cap_region_x_begin = 0.5  # start point/total width
cap_region_y_end = 0.8  # start point/total width
threshold = 50  # threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50
learningRate = 0
bgCaptured = 0  # bool variety


def removeBG(bgModel,frame):
    fgmask = bgModel.apply(frame, learningRate=learningRate)  # Build a background subtractor model
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)  # process the outline
    removed = cv2.bitwise_and(frame, frame, mask=fgmask)  # Apply the model to a frame
    return removed


def calculateFingers(res, drawing):  # count fingers and draw
    hull = cv2.convexHull(res, returnPoints=False)  # find the convex hull, and get the angular point
    if len(hull) > 3:
        defects = cv2.convexityDefects(res, hull)  # convexity defect
        if type(defects) != type(None):  # avoid crashing
            cnt = 0
            for i in range(defects.shape[0]):  # calculate the angle
                s, e, f, d = defects[i][0]
                start = tuple(res[s][0])
                end = tuple(res[e][0])
                far = tuple(res[f][0])
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))  # compute the angle of each hull side
                if angle <= math.pi / 2:  # if angle less than 90 degree, treat as fingers and draw
                    cnt += 1
                    cv2.circle(drawing, far, 8, [211, 84, 0], -1)
            return True, cnt
    return False, 0


def opencamera():
    camera = cv2.VideoCapture(0)  # creating camera object
    camera.set(10, 200)  # set camera
    bgModel = None
    bgCaptured = 0
    while camera.isOpened():
        ret, frame = camera.read()  # reading the frames
        frame = cv2.bilateralFilter(frame, 5, 50, 100)  # smoothing filter
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),  # draw the ROI rectangle
                      (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
        cv2.imshow('input', frame)  # show the frame

        if bgCaptured == 1:
            removed = removeBG(bgModel, frame)
            ROI = removed[0:int(cap_region_y_end * frame.shape[0]),
                  int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
            cv2.imshow('ROI', ROI)  # show the ROI

            gray = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)  # convert the image into binary image
            blur = cv2.GaussianBlur(gray, (blurValue, blurValue), 0)  # cancel the noise and smooth the whole image
            cv2.imshow('blur', blur)  # show the blur result
            ret, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)  # get the black and white image
            cv2.imshow('threshold', thresh)  # show the threshold result

            # get the contours
            thresh1 = copy.deepcopy(thresh)  # copy father and son class
            contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find the contour
            length = len(contours)
            maxArea = -1
            if length > 0:
                for i in range(length):  # find the biggest contour (according to area)
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i
                res = contours[ci]
                hull = cv2.convexHull(res)  # find the contour's convex hull
                drawing = np.zeros(ROI.shape, np.uint8)
                cv2.drawContours(drawing, [res], 0, (0, 255, 0), 2)
                cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 3)
                isFinishCal, cnt = calculateFingers(res, drawing)
            cv2.imshow('output', drawing)

        # keyboard
        k = cv2.waitKey(10)
        if k == 27:  # esc
            camera.release()
            cv2.destroyAllWindows()
            break
        elif k == ord('b'):  # press 'b' to capture the background
            bgModel = cv2.createBackgroundSubtractorMOG2(0, bgSubThreshold)  # Creates MOG2 Background Subtractor
            bgCaptured = 1
            print('!!!Background Captured!!!')
        elif k == ord('p'):  # play a game
            print('eigenvalue of gesture is ', cnt)
            move = ""
            if cnt == 0:
                move = "Rock"
            if cnt == 1:
                move = "Scissors"
            if cnt == 4:
                move = "Paper"
            game.play(move)
            game.score()

