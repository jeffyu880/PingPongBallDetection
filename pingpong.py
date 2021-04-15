import numpy as np
import cv2
#template matching
video = cv2.VideoCapture(0)
video.set(3, 640)  # Set horizontal resolution
video.set(4, 480)  # Set vertical resolution

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v
#h value divide by 2, s, and v values divide by 100 and multiply by 255
orange_min_val = (10,150,160)
#(10, .18*255, .35*255)                  #very light orange/pastel
orange_max_val = (23,255,255)
#(10, 255, 255)             python  #very rich/deep orange
white_min_val = (17, 0, 105)                        #Pure white
white_max_val = (44, 87, 255)
yellow_min_val = (25, 56, 79)
yellow_max_val = (25, 255, 255)

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        colorsB = frame[y,x,0]
        colorsG = frame[y,x,1]
        colorsR = frame[y,x,2]
        colors = frame[y,x]
        print("Red: ",colorsR)
        print("Green: ",colorsG)
        print("Blue: ",colorsB)
        print("BGR Format: ",colors)
        print("HSV Format: ", rgb_to_hsv(colorsR, colorsG, colorsB))
        print("Coordinates of pixel: X: ",x,"Y: ",y)

        cv2.imshow('HSV', hsv)

while True:
    check, frame = video.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsv = cv2. cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("Capturing", frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    cv2.GaussianBlur(frame, (5,5), cv2.BORDER_DEFAULT)
    cv2.imshow("HSV", hsv)
    mask_orange = cv2.inRange(hsv, orange_min_val, orange_max_val)
    mask_white = cv2.inRange(hsv, white_min_val, white_max_val)
    #mask_yellow = cv2.inRange(hsv, yellow_min_val, yellow_max_val)
    #cv2.imshow("yellow mask", mask_yellow)
    mask_orange = cv2.erode(mask_orange, kernel, iterations = 2)
    mask_orange = cv2.dilate(mask_orange, kernel, iterations = 2)
    mask_white = cv2.erode(mask_white, kernel, iterations = 2)
    mask_white = cv2.dilate(mask_white, kernel, iterations = 2)
    cv2.imshow("orange mask", mask_orange)
    cv2.imshow("white mask", mask_white)
    mask_combined = cv2.bitwise_or(mask_orange, mask_white)
    cv2.imshow("masked", mask_combined)
    #cv2.imshow("Gray", gray)
    # #adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 1)
    # cv2.imshow("adaptive", adaptive)
    #
    #
    # cv2.imshow("Dilate", dilate)
    # gaussian = cv2.GaussianBlur(dilate, (5,5), 5)
    #
    # cv2.imshow("Gaussian", gaussian)
    #
    # edged = cv2.Canny(dilate, 200, 255)
    # contours, heiarachy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    #
    # cv2.drawContours(frame, contours, -1, (255,0,255), 3)

    cv2.setMouseCallback('HSV', click_event)

    if cv2.waitKey(20) & 0xFF == ord('r'):
        print("there are {} contours" .format(len(contours)))

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
