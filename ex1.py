import math
import cv2 as cv
from cv2 import exp
from scipy.signal import gaussian, convolve2d
from matplotlib import pyplot as plt
import numpy as np
from scipy.fft import fft2, ifft2 
from skimage.util import random_noise
#####################  Degrading the image and adding noise:
# Question 1
path = r'C:\Users\youss\OneDrive\Documents\IVP\project 2\geese.jpg'
img = cv.imread(path)
def rescaleImage(Image, scaler_factor):
    height = int(Image.shape[0] * scaler_factor)
    width = int(Image.shape[1] * scaler_factor)
    dimension = (width,height)

    return cv.resize(Image, dimension, interpolation=cv.INTER_AREA)
# rescaling the image since its too big for my screen(personal option)
img= rescaleImage(img,0.1)
cv.imshow("Original Image",img)

# Method that will blur the image with a motion effect
def MotionBlur(image):
    # Seting the coefficient of for the blurring
    a = 0.25
    b = 0.15
    #taking the size of the image
    n2, n1, n0 = image.shape
    # Creating a grid in order to make the motion effect
    [u, v] = np.mgrid[-n2 / 2:n2 / 2, -n1 / 2:n1 / 2]
    u = 2 * u / n2
    v = 2 * v / n1
    # Applying the fourier transform 
    F = np.fft.fft2(image)
    # The  diagonal motion blurring degradation function
    H = np.sinc((u * a + v * b)) * np.exp(-1j * np.pi * (u * a + v * b))
    G = F
    G[:, :, 0] = np.multiply(F[:, :, 0], H)
    G[:, :, 1] = np.multiply(F[:, :, 1], H)
    G[:, :, 2] = np.multiply(F[:, :, 2], H)
    # Applying the inverse fourier transform
    g = np.fft.ifft2(G)
    return g

V =abs(MotionBlur(img)) / 255 
T =MotionBlur(img)

# # Question 2
# def add_gaussian_noise(img):
# 	gauss = np.random.normal(0, 0.2, np.shape(img))
# 	noisy_img = img + gauss
# 	noisy_img[noisy_img < 0] = 0
# 	noisy_img[noisy_img > 255] = 255
# 	return noisy_img
# cv.imshow("Motion Blur Degradation Plus Gaussian Noise Image ",add_gaussian_noise(V))

noise_img = random_noise(V, mode='s&p',amount=0.1)
noise_img = np.array(255*noise_img, dtype = 'uint8')

# Question 3
cv.imshow("Motion Blur Degradation Image ",V)
cv.imshow('Motion Blur Degradation Plus Gaussian Noise Image',noise_img)

#############     Removing noise: 

# Question 1
def wienner_filter(image):
    a = 0.25
    b = 0.15
    #taking the size of the image
    n2, n1, n0 = image.shape
    # Creating a grid in order to make the motion effect
    [u, v] = np.mgrid[-n2 / 2:n2 / 2, -n1 / 2:n1 / 2]
    u = 2 * u / n2
    v = 2 * v / n1
    # Applying the fourier transform 
    F = np.fft.fft2(image)
    # The  diagonal motion blurring degradation function
    H = np.sinc((u * a + v * b)) * np.exp(-1j * np.pi * (u * a + v * b))
    # We have to get the fourier transfrom of the image in Order to get G 
    image = np.fft.fft2(image)
    G = image 
    R1 = G
    R1[:, :, 0] = np.divide(G[:,:,0], H)
    R1[:, :, 1] = np.divide(G[:,:,1], H)
    R1[:, :, 2] = np.divide(G[:,:,2], H)
    return np.abs(np.fft.ifft2(R1))/255
rx1 = wienner_filter(abs(T))
cv.imshow("Wienner Filter of Only Blur Image",rx1)

# Question 2 
rx2 = wienner_filter(abs(noise_img))
cv.imshow("Wienner Filter Of Blur and Guassian Noise Image",rx2)
cv.waitKey(0)
 