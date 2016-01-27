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
from pokerOCR import cardsOCR, getAndConvertImage

#problems: results are not accurate enough
#number of ties in result seems very high

def getSeed():
##        endpoint = 'https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint16'
##
##        req = request.Request(endpoint)
##        response = request.urlopen(req)
##
##        #print(response.read().decode('utf-8'))
##        return json.loads(response.read().decode('utf-8'))['data'][0]

        return random.randint(10,100)
    




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





title = getWindowTitle('No Limit Hold\'em')

card_samples = {}
for file in os.listdir('card samples'):
    card_samples.update({file.rstrip('.png'): np.array(Image.open('card samples/'+ file).convert('L'))})

    
hand_card_samples = card_samples.copy()
for x in range(1,6):
    hand_card_samples.pop('EmptyPos' + str(x))

for x in range(1,3):
    card_samples.pop('noHandCard' + str(x))



table_cards_previous = []
hand_cards_previous = []
players_previous = []#to prevent repetitive printing
time_next_seed = datetime.datetime.now()
seed_value = getSeed()

while(True):


    
    if datetime.datetime.now() > time_next_seed:
        seed_value = getSeed()
        time_next_seed = datetime.datetime.now() + datetime.timedelta(minutes=10)
    

    window_image = getScreenshot(title) #resizes to 1493x1057 and moves to (0,0) coordinate (for dual monitor)

    (image_width, image_height) = window_image.size


    my_hand_bbox = [ (645, 628, 728, 689), #crop coordinates (left, top, right, bottom)                  
                     (734, 628, 817, 689) ]

    table_cards_bbox = [ (515, 339, 598, 400),
                         (606, 339, 689, 400),
                         (697, 339, 780, 400),
                         (788, 339, 871, 400),
                         (879, 339, 962, 400) ]
                        



    hand_cards_image = [getAndConvertImage(window_image, x) for x in my_hand_bbox]
    table_cards_image = [getAndConvertImage(window_image, x) for x in table_cards_bbox]
    #Image.fromarray(hand_cards_image[1], 'L').show()
    
    #Image.fromarray(table_cards_image[3], 'L').show()
    #break
    
    player1_bbox = (99, 165, 275, 203)

    player2_bbox = (98, 485, 272, 525)  

    player3_bbox = (653, 41, 829, 80)  

    player4_bbox = (1210, 165, 1385, 205)  

    player5_bbox = (1209, 486, 1385, 526)
        
    player_images = [getAndConvertImage(window_image, player1_bbox, 'RGB'),\
                     getAndConvertImage(window_image, player2_bbox, 'RGB'),\
                     getAndConvertImage(window_image, player3_bbox, 'RGB'),\
                     getAndConvertImage(window_image, player4_bbox, 'RGB'),\
                     getAndConvertImage(window_image, player5_bbox, 'RGB')]


    #Image.fromarray(player_images[0], 'RGB').show()

    
    
    
    




    table_cards = [cardsOCR(x, card_samples) for x in table_cards_image]
    hand_cards = [cardsOCR(x, hand_card_samples) for x in hand_cards_image]

    players_in_game = 0
    
    for x in range(5):#scan cropped image of opponent cards and  sum red pixel values (back of card color) to determine number of players in round
        if player_images[x][:,:,0].sum() > 800000:#arbitrary value
            players_in_game += 1#if there are many red pixels then there is player
    
    

    if(table_cards_previous != table_cards or hand_cards_previous != hand_cards or players_previous != players_in_game):
        
        empty_positions = ['EmptyPos1', 'EmptyPos2', 'EmptyPos3', 'EmptyPos4', 'EmptyPos5', 'noHandCard1', 'noHandCard2']

        table_cards_input = []
        for card in table_cards:
            if card not in empty_positions:
                table_cards_input.append(card)


        hand_cards_input=[]
        for card in hand_cards:
            if card not in empty_positions:
                hand_cards_input.append(card)

        


        if(len(hand_cards_input) == 2 and players_in_game > 0):
 
            try:
                results = monteCarloSim(hand_cards_input, table_cards_input, players_in_game, seed_value)

                odds_of_winning = results['wins']/results['rounds']
                odds_of_tie = [x/results['rounds'] for x in results['ties']]
                odds_of_losing = results['losses']/results['rounds']
                print('\n'*5)
                print('Table cards: \n', table_cards_input)
                print('Hand Cards:', hand_cards_input)
                print('Opponents:',players_in_game, '\n\n')
                print('\n'*(25 - players_in_game))

                print('Win: ', round(odds_of_winning, 4), '\n')
                print('Tie ', 1, 'player: ', round(odds_of_tie[0], 4), '\n')
                for x in range(1, len(odds_of_tie)):
                    print('Tie ', x+1, 'players: ', round(odds_of_tie[x], 4), '\n')
                print('Lose: ', round(odds_of_losing, 4), '\n')

                expected_equity = odds_of_winning*players_in_game
                for x in range(len(odds_of_tie)):
                    expected_equity += (odds_of_tie[x]*(players_in_game+1)/(x+2) - odds_of_tie[x])
                expected_equity -= odds_of_losing
                
                print('Expected equity: ', round(expected_equity, 4))
                
                
            except Exception as e:
                print(e, '\n\n')
            #print("--- %s seconds ---" % (time.time() - start_time))
            #Image.fromarray(hand_cards_image, 'L').show()
            #Image.fromarray(table_cards_image, 'L').show()

    table_cards_previous = table_cards
    hand_cards_previous = hand_cards
    players_previous = players_in_game

    time.sleep(1)


    





