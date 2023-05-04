from PIL import Image
from numpy import *
import matplotlib.pyplot as plt

def show_histograms(
        start_img : Image, 
        stego_img : Image): 
    
	start_img_array = array(start_img)
	stego_img_array = array(stego_img)

	start_img_array_red = start_img_array[:, :, 0]
	stego_img_array_red = stego_img_array[:, :, 0]

	plt.figure(figsize=(10, 6))
	plt.hist(start_img_array_red.flatten(), bins=256, color='b', alpha=0.5)
	plt.title("Гистограмма оригинального изображения (RED канал)")
	plt.xlabel("Значение пикселей")
	plt.ylabel("Колличество пикселей")
	plt.show()

	
	plt.figure(figsize=(10, 6))
	plt.hist(stego_img_array_red.flatten(), bins=256, color='r', alpha=0.5)
	plt.title("Гистограмма стегоизображения (RED канал)")
	plt.xlabel("Значение пикселей")
	plt.ylabel("Колличество пикселей")
	plt.show()