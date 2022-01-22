from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2

INPUT_IMAGE = 'captchaG3.gif'
INPUT_IMAGE = 'Golestan-Captchas/56867.gif'


def sharp_img(img):
	gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	blur_image = cv2.blur(gray_img, (4, 4))
	gblur_img = cv2.GaussianBlur(blur_image, (0, 0), 6)
	sharp_img = cv2.addWeighted(gray_img, 1.80, gblur_img, -0.60, 0)
	sharp_not_img = cv2.bitwise_not(sharp_img);
	retval, img_zeroone = cv2.threshold(sharp_not_img, 20, 255, cv2.THRESH_BINARY)
	return img_zeroone


def clear_img(img):
	im  = cv2.imread('mask.png')
	mask = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	retval, t_mask = cv2.threshold(mask, 70, 255, cv2.THRESH_BINARY)
	masker = cv2.bitwise_not(t_mask)
	img = cv2.bitwise_and(img, masker)
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(2,2))
	opening_img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	# opening_img = cv2.bitwise_not(opening_img)

	return opening_img

def show_image(image):
	cv2.imshow('image',image)
	c = cv2.waitKey()
	if c >= 0 : return -1
	return 0

def isContain(c, contours):
	for item in contours:
		xC, yC, wC, hC = cv2.boundingRect(c)
		xItem, yItem, wItem, hItem = cv2.boundingRect(item)
		if (xC - xItem) in range(6) and (yC - yItem) in range(6) and wC < wItem and hC < hItem:
			print(xC, yC, wC, hC)
			print(xItem, yItem, wItem, hItem, end="\n\n")
			return True
		if wC < 5 or hC < 5:
			return True
	return False

def bestContours(contours):

	contoursDict = {}
	for index, item in enumerate(contours):
		if not isContain(item, contours):
			contoursDict[index] = len(item)
	sortedItems = sorted(contoursDict.items(), key=lambda x: x[1], reverse = True)[:5]
	keys = [item[0] for item in sortedItems]
	values = [item[1] for item in sortedItems]

	print(sortedItems)

	returnedTuple = []
	for index, item in enumerate(contours):
		if index in keys:
			returnedTuple.append(item)
	return tuple(returnedTuple)

im = cv2.imread(INPUT_IMAGE)
sim = sharp_img(im)

cl_img = clear_img(sim)

contours, hierarchy  = cv2.findContours(cl_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

contours = bestContours(contours)

for c in contours:
	x, y, w, h = cv2.boundingRect(c)
	ROI = cl_img[y:y+h, x:x+w]
	cv2.imwrite(f'captcha{x+y}.png', cv2.bitwise_not(ROI))
	cv2.rectangle(cl_img, (x-3, y-3), (x+w+1, y+h+1), (255, 255, 255), 1)

show_image(cl_img)

# cv2.imshow("ClearedImage", cl_img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite('captcha.png', cl_img)