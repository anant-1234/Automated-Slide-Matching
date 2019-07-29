import matplotlib.image as mpimg
import glob
import numpy as np
import math
from scipy import ndimage

n = 400

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


for i in range(1):
	im = mpimg.imread(framespath[i])
	gray = rgb2gray(im)

	dx = ndimage.sobel(gray, 1)
	dy = ndimage.sobel(gray, 0)
	gray = np.hypot(dx, dy)
	gray *= 255.0/np.max(gray)

	gray = (gray-np.mean(gray))/math.sqrt(np.var(gray))

	# curmax = -1e15
	# ans = -1
	# for j in range(len(slides)):
	# 	try:
	# 		cnt = {}
	# 		curmax = -1e15
	# 		for u in range(len(slides[j]) - n + 1):
	# 			for v in range(len(slides[j][0]) - n + 1):
	# 				t_slide = np.array(slides[j])
	# 				temp = np.sum(np.multiply(gray, t_slide[u:u+n-1,v:v+n-1]))
	# 				if temp >= curmax:
	# 					curmax = temp
	# 					ans = j
	# 					cnt{j} = ans;
	# 	except:
	# 		pass
	
	cur = {}
	for u in range(0, np.size(gray,0) - n + 1):
		for v in range(0, np.size(gray,1) - n + 1):
			cur_max = -1e15
			ans = -1
			for j in range(len(slides)):
				try:
					t_slide = np.array(slides[j])
					temp = np.sum(np.multiply(gray[u:u+n-1,v:v+n-1], t_slide[u:u+n-1,v:v+n-1]))
					if temp >= cur_max:
						cur_max = temp
						ans = j
				except:
					pass
			if ans in cur:
				cur[ans] += 1
			else:
				cur[ans] = 1
	maxi = 0
	ans = -1
	for keys in cur:
		if cur[keys] >= maxi:
			maxi = cur[keys]
			ans = keys
	
	print(framespath[i].split('/')[3], slidespath[ans].split('/')[3])
	if (framespath[i].split('/')[3].split('_')[0] + '_' + framespath[i].split('/')[3].split('_')[1]) == slidespath[ans].split('/')[3].split('.')[0]:
		correct += 1
	else:
		incorrect += 1

print('=================================================')
print('Correct: ', correct, 'Incorrect: ', incorrect)
print('Accuracy: ', 100*correct/(correct+incorrect))
print('=================================================')