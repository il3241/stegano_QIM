from PIL import Image, ImageFilter
from cprint import *
from math import log10
import numpy as np
from skimage.metrics import structural_similarity as ssim


def check_size(
        size_of_img   : tuple, 
        input_message : str ) -> bool:
    
    if size_of_img[0] * size_of_img[1] >= len(input_message) * 8:
        return True
    else:
        return False
    
def string_to_binary(
        input_message_str : str ) -> list:
    
    input_message_bin = []
    for ch in input_message_str:
        input_message_bin.extend([int(bit) for bit in bin(ord(ch))[2:].zfill(8)])
    return input_message_bin

def show_img(
        image : Image,
		name : str):
	image.save("out_img/" + name+".PNG", "PNG")
	image.show()

def save_img(
		image : Image,
		name : str):
	image.save("out_img/" + name+".PNG", "PNG")


def binary_to_string(input_message_bin : list) -> str:
	input_message_str = ""
	for i in range(0, len(input_message_bin), 8):
		ch = chr(int("".join(map(str, input_message_bin[i : i + 8])), 2))
		input_message_str += ch
	return input_message_str


def obscurity_MSE(
        old_img : Image, 
        new_img : Image) -> float:
	size_of_img = (old_img.size)
	size = size_of_img[0] * size_of_img[1]
	delta_sum = 0

	for y in range(size_of_img[1]):
		for x in range(size_of_img[0]):
			pos = (x,y)
			r_old, g_old, b_old = old_img.getpixel(pos)
			r_new, g_new, b_new = new_img.getpixel(pos)

			delta = r_old - r_new

			delta_sum += pow(delta,2)

	MSE = delta_sum / (size)

	return MSE

def obscurity_PSNR(
		MSE : float) -> float: 
	PSNR = 10 * log10((255*255)/MSE)

	return PSNR

def obscurity_RMSE(
		MSE : float) -> float: 
	RMSE = pow(MSE, 0.5)

	return RMSE

"""
def obscurity_SSIM(
		old_img : Image, 
        new_img : Image) -> float: 
	average_r_old = 0.0 # Среднее значение пикселей старого контейнера
	average_r_new = 0.0 # Среднее значение пикселей нового контейнера

	k_1 = 0.01 # Первая константа
	k_2 = 0.03 # Вторая константа
	L = pow(2, 8) -1
	c_1 = pow((k_1 * L), 2)
	c_2 = pow((k_2 * L), 2)
	size_of__img = ( old_img.size )

	variance_r_old = 0.0 # Дисперсия старого контейнера
	variance_r_new = 0.0 # Дисперсия нового контейнера

	math_expectation_old = 0.0 # Математическое ожидание старое
	math_expectation_new = 0.0 # Математическое ожидание новое
	# Вычисляем математическое ожидание
	for y in range(size_of__img[1]):
			for x in range(size_of__img[0]):
				pos = (x,y)
				r_old,g_old,b_old = old_img.getpixel(pos)
				r_new,g_new,b_new = new_img.getpixel(pos)
				math_expectation_old += r_old
				math_expectation_new += r_new
	
	math_expectation_old /= (size_of__img[1] * size_of__img[0])
	math_expectation_new /= (size_of__img[1] * size_of__img[0])
	# Вычисляем средние значения
	for y in range(size_of__img[1]):
			for x in range(size_of__img[0]):
				pos = (x,y)
				# Получваем значения RGB пикселя
				r_old,g_old,b_old = old_img.getpixel(pos)
				r_new,g_new,b_new = new_img.getpixel(pos)

				average_r_old += r_old
				average_r_new += r_new

				# Дисперсия старого
				variance_r_old += pow((r_old - math_expectation_old), 2)
				# Дисперсия нового
				variance_r_new += pow((r_new - math_expectation_new), 2)
				
	variance_r_old /= 256
	variance_r_new /= 256

	average_r_old /= (size_of__img[1] * size_of__img[0])
	average_r_new /= (size_of__img[1] * size_of__img[0])

	сovariance = 0.0

	for y in range(size_of__img[1]):
			for x in range(size_of__img[0]):
				r_old,g_old,b_old = old_img.getpixel(pos)
				r_new,g_new,b_new = new_img.getpixel(pos)
				сovariance += (r_old - average_r_old) * (r_new - average_r_new)

	сovariance /= (size_of__img[1] * size_of__img[0])
	numerator = (2 * average_r_old * average_r_new + c_1) * (2 * сovariance + c_2)
	denominator = (pow(average_r_old, 2) + pow(average_r_new, 2) + k_1) * (variance_r_old + variance_r_new + k_2)
	SSIM  = numerator / denominator

	return SSIM 
"""

def obscurity_SSIM(
		old_img : Image, 
        new_img : Image): 
	
	old_arr = np.array(old_img)
	new_arr = np.array(new_img)

	r_old = old_arr[:, :, 0]
	r_new = new_arr[:, :, 0]

	SSIM = ssim(r_old, r_new)

	return SSIM

def capacity(
		img 	: Image,
		bin_mes : list) -> float: 
	size_of_img = (img.size)
	EC = len(bin_mes) / (size_of_img[0] * size_of_img[1])

	return EC 



