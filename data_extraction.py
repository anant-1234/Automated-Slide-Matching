import shutil
import glob 
print(glob.glob("./Dataset/*"))
temp = glob.glob("./Dataset/*")
for i in temp:
	try:
		shutil.copyfile(i+"/ppt.jpg", './Test/slides/'+i[10:] + '.jpg')
	except:
		pass