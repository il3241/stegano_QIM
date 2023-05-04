
from PIL import Image, ImageFilter
from cprint import *
from functions import *
from filters import *
from histograms import *

def START():
	bprint("Введите название входного файла (файл должен быть сохранен в папке /in_img)")
	name = input()
	path_to_inp_image = "in_img/" + name

	try:
		input_img = Image.open(path_to_inp_image)
		start_img = input_img
		bprint("Что необходимо сделать с входным файлом: \
			\n1 - встраивание; \
			\n2 - извлечение.")
	
		TODO = int(input())
		while TODO != "exit":
			if TODO == 1:
		
				bprint("Введи сообщение которое необходимо встроить в файл, оно должно быть сохрангено в папке /message")

				mes_name = input()
				mes_path = "message/" + mes_name
				file = open(mes_path, "r")
				message = file.readline()
				file.close()

				bprint("Введите шаг квантования:")
				q = int(input())
	
				output_image = EMBEDDING(input_img, message, q)
				bprint("=====================")
				bprint("MSE")
				MSE = obscurity_MSE(start_img, output_image)
				gprint(MSE)

				bprint("---------------------")

				bprint("PSNR")
				PSNR = obscurity_PSNR(MSE)
				gprint(PSNR)

				bprint("---------------------")

				bprint("RMSE")
				RMSE = obscurity_RMSE(MSE)
				gprint(RMSE)

				bprint("---------------------")

				bprint("SSIM")
				SSIM = obscurity_SSIM(start_img, output_image)
				gprint(SSIM)

				bprint("---------------------")

				bprint("EC")
				input_message_binary = []
				input_message_binary = string_to_binary(message)
				EC = capacity(input_img, input_message_binary)
				gprint(EC)
				bprint("---------------------")
				bprint("=====================")

				bprint("Оценить устойчивость встраивания к деструктивным воздействиям?")
				bprint("Да  - 1")
				bprint("Нет - 2")
				TODO_destr = int(input())

				while TODO_destr != "exit":	
					if (TODO_destr == 1):
						bprint("---------------------")
						
						# Размытие
						bprint("BER_blur")
						BER_blur = blur_and_check(q, input_message_binary, output_image)
						gprint(BER_blur)

						bprint("---------------------")

						# Резкость
						bprint("BER_sharpen")
						BER_sharpen = sharpen_and_check(q, input_message_binary, output_image)
						gprint(BER_sharpen)

						bprint("---------------------")
						
						# Сглаживание
						bprint("BER_smooth")
						BER_smooth = smooth_and_check(q, input_message_binary, output_image)
						gprint(BER_smooth)

						bprint("---------------------")
						
						# Выделение контура
						bprint("BER_contour") 
						BER_contour = contour_and_check(q, input_message_binary, output_image)
						gprint(BER_contour)

						bprint("---------------------")

						# Выделение Деталей
						bprint("BER_detail") 
						BER_detail = detail_and_check(q, input_message_binary, output_image)
						gprint(BER_detail)

						bprint("---------------------")

						# Выпуклость
						bprint("BER_emboss") 
						BER_emboss = emboss_and_check(q, input_message_binary, output_image)
						gprint(BER_emboss)
						bprint("---------------------")
						# Черное белое
						bprint("BER_grayscale") 
						BER_grayscale = grayscale_and_check(q, input_message_binary, output_image)
						gprint(BER_grayscale)
						bprint("---------------------")
						bprint("=====================")
						bprint("---------------------")
						# Черное белое
						bprint("BER_0") 
						BER_0 = zero_and_check(q, input_message_binary, output_image)
						gprint(BER_0)
						bprint("---------------------")
						bprint("=====================")
						TODO_destr = "exit"
					elif TODO_destr == 2:
						TODO_destr = "exit"
					else:
						rprint("Введите либо 1 (Да), либо 2 (Нет).")
						TODO_destr = int(input())
				bprint("Показать гистограммы?")
				bprint("Да  - 1")
				bprint("Нет - 2")
				TODO_hist = int(input())
				while TODO_hist != "exit":
					if TODO_hist == 1:
						show_histograms(start_img, output_image)
						TODO_hist = "exit"
					elif TODO_hist == 2:
						TODO_hist = "exit"
					else: 
						rprint("Введите либо 1 (Да), либо 2 (Нет).")
						TODO_hist = int(input())
				TODO = "exit"
				show_img(output_image, "main")
			elif TODO == 2:
				bprint("Введите шаг квантования:")
				q = int(input())
				message = "" 
				message = EXTRACTION(input_img, q) 
				bprint(message)
				TODO = "exit"
			else:
				rprint("Введите либо 1 (встраивание), либо 2 (извлечение)")
				TODO = int(input())
	except FileNotFoundError:  
		rprint("Файл не найден. Обратите внимание, что входной файл должен находиться в папке /in_img")


def EMBEDDING(
		input_img 	  : Image, 
		input_message : str, 
		q             : int ) -> Image:
	input_img = input_img.convert('RGB')             	  # Конвертируем входное изображение в формат RGB
	size_of_input_img = ( input_img.size ) 		 		  # Кортеж с парой значений w, h
	can_insert = check_size(size_of_input_img, input_message) # Проверяем влезает ли сообщение в фото
	if can_insert: # Если влезает, то начинаем встраивание

		# Переводим символы сообщения в битовый формат
		input_message_binary = []
		input_message_binary = string_to_binary(input_message)

		index_message = 0
		# Начинаем встраивание
		for y in range(size_of_input_img[1]):
			for x in range(size_of_input_img[0]):
				
				pos = (x,y)
				# Получваем значения RGB пикселя
				r,g,b = input_img.getpixel(pos)

				# Проверяем, не кончилось ли сообщение
				if index_message != len(input_message_binary):
					
					# Встраиваем бит сообщения в r
					r_modified = q * (r//q) + (q//2) * input_message_binary[index_message]

					# Добавляем измененное значение обратно
					input_img.putpixel(pos, (r_modified, g, b))

					index_message += 1 # Итерируем по битам сообщения

	else:
		rprint("Данное сообщение слишком большое и не может быть встроено. \
	 			\nСоответственно, сообщение не было изменено.")
	
	return input_img



def EXTRACTION(
		stego_img : Image,
		q         : int) -> str:
	
	stego_img = stego_img.convert('RGB')             	  # Конвертируем входное изображение в формат RGB
	size_of_input_img = ( stego_img.size ) 		 		  # Кортеж с парой значений w, h

	ext_message_binary = []							      # Извлекаем сообщение в бинарном формате

	for y in range(size_of_input_img[1]):
			for x in range(size_of_input_img[0]):
				
				pos = (x,y)
				# Получваем значения RGB пикселя
				r_modified, g, b = stego_img.getpixel(pos)

				
				# Встраиваем в пиксель нулевой P_0 и единичный P_1 бит
				P_0 = q * (r_modified // q)
				P_1 = q * (r_modified // q) + (q // 2)

				m_i = min( abs(r_modified - P_0), abs(r_modified - P_1) )
				if ( abs(r_modified - P_0) < abs(r_modified - P_1)):
					ext_message_binary.append(0)
				else:
					ext_message_binary.append(1)

	ext_message_str = ""

	ext_message_str = binary_to_string(ext_message_binary)

	return ext_message_str


if __name__ == "__main__":
	START()
	


