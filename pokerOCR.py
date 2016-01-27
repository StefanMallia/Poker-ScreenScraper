import numpy as np
from PIL import ImageGrab, Image, ImageChops
import datetime
import time
import random
import os
from getScreenshot import getScreenshot, getWindowTitle
from urllib import request
import json
from montecarlo import monteCarloSim


def cardsOCR(image, card_samples):
    '''
    Function that uses openCV matchtemplate module to scan an image for the template
    '''
    results = {}

    for card in card_samples:
        results.update({card: ((image - card_samples[card])**2).sum()})

     #results with smallest value chosen as these are the best results
    key = min(results, key=results.get)

    return key

def getAndConvertImage(window_image, bbox, colour = 'L'):
    '''
    Crop and convert to greyscale ('L') or RGB ('RGB')
    '''
    image = window_image.copy()#help(window_image.crop) to see why (lazy operation)
    image = image.crop(bbox)
    #window_image.show()
    #hand_cards_image.show()


    image = image.convert(colour)#.convert('RGB')
    image = np.array(image)

    return image



