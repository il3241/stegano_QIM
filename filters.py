from PIL import Image, ImageFilter
from functions import *
from cprint import *
from QIM import show_img

def EXTRACTION_FILTERED(
        q         : int,
        stego_filtred_img : Image) -> list: 
    
	stego_filtred_img = stego_filtred_img.convert('RGB')             	  # Конвертируем входное изображение в формат RGB
	size_of_input_img = ( stego_filtred_img.size ) 		 		  # Кортеж с парой значений w, h

	ext_message_binary = []							      # Извлекаем сообщение в бинарном формате

	for y in range(size_of_input_img[1]):
			for x in range(size_of_input_img[0]):
				
				pos = (x,y)
				# Получваем значения RGB пикселя
				r_modified, g, b = stego_filtred_img.getpixel(pos)

				
				# Встраиваем в пиксель нулевой P_0 и единичный P_1 бит
				P_0 = q * (r_modified // q)
				P_1 = q * (r_modified // q) + (q // 2)

				m_i = min( abs(r_modified - P_0), abs(r_modified - P_1) )
				if ( abs(r_modified - P_0) < abs(r_modified - P_1)):
					ext_message_binary.append(0)
				else:
					ext_message_binary.append(1)
	return ext_message_binary

def CHECK(
		inp_mes : list,
		ext_mes : list) -> float: 
	B_e = 0
	for i in range(len(inp_mes)):
		if inp_mes[i] != ext_mes[i]:
			B_e += 1
	BER = B_e / len(inp_mes)

	return BER
	

def blur_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.BLUR)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    
    save_img(stego_filtred_img, "1")


    return BER

def sharpen_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.SHARPEN)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, "2")
    

    return BER

def smooth_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.SMOOTH)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img , "3")
    
    return BER

def contour_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.CONTOUR)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img , '4')
    
    return BER

def detail_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.DETAIL)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, '5')
    
    return BER


def emboss_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.filter(ImageFilter.EMBOSS)
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, '6')
    
    return BER

def grayscale_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
    stego_filtred_img = stego_img.convert('L')
    ext_mes_bin = EXTRACTION_FILTERED(q, stego_filtred_img)
    BER = CHECK(input_bin, ext_mes_bin)
    save_img(stego_filtred_img, '7')
    
    return BER

def zero_and_check(
        q         : int,
        input_bin : list,
        stego_img : Image) -> float: 
	ext_mes_bin = EXTRACTION_FILTERED(q, stego_img)
	BER = CHECK(input_bin, ext_mes_bin)

	return BER