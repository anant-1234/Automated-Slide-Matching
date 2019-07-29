import matplotlib.image as mpimg
import glob
import numpy as np
import math
from scipy import ndimage

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

framespath = glob.glob("./Test/frames/*.jpg")
slidespath = glob.glob("./Test/slides/*.jpg")
framespath.sort()
slidespath.sort()

slides = []

# Converting to rgb, applying sobel and then normalizing
for i in slidespath:
	im = mpimg.imread(i)
	gray = rgb2gray(im)

	dx = ndimage.sobel(gray, 1)
	dy = ndimage.sobel(gray, 0)
	gray = np.hypot(dx, dy)
	gray *= 255.0/np.max(gray)

	slides.append((gray-np.mean(gray))/math.sqrt(np.var(gray)))

correct = 0
incorrect = 0

for i in range(len(framespath)):
	im = mpimg.imread(framespath[i])
	gray = rgb2gray(im)

	dx = ndimage.sobel(gray, 1)
	dy = ndimage.sobel(gray, 0)
	gray = np.hypot(dx, dy)
	gray *= 255.0/np.max(gray)

	gray = (gray-np.mean(gray))/math.sqrt(np.var(gray))

	curmax = -1e15
	ans = -1
	for j in range(len(slides)):
		try:
			temp = np.sum(np.multiply(gray, slides[j]))
			if temp >= curmax:
				curmax = temp
				ans = j
		except:
			pass

	
	print(framespath[i].split('/')[3], slidespath[ans].split('/')[3])
	if (framespath[i].split('/')[3].split('_')[0] + '_' + framespath[i].split('/')[3].split('_')[1]) == slidespath[ans].split('/')[3].split('.')[0]:
		correct += 1
	else:
		incorrect += 1

print('=================================================')
print('Correct: ', correct, 'Incorrect: ', incorrect)
print('Accuracy: ', 100*correct/(correct+incorrect))
print('=================================================')