import pokerEval as pe

import time
import random




    
class Deck:

    def __init__(self, seed_value):
        
        self.deck = {'C2': 1, 'C3': 1, 'C4': 1, 'C5': 1, 'C6': 1, 'C7': 1, 'C8': 1, 'C9': 1, 'C10': 1, 'CJ': 1, 'CQ': 1, 'CK': 1, 'CA': 1, \
                     'D2': 1, 'D3': 1, 'D4': 1, 'D5': 1, 'D6': 1, 'D7': 1, 'D8': 1, 'D9': 1, 'D10': 1, 'DJ': 1, 'DQ': 1, 'DK': 1, 'DA': 1, \
                     'H2': 1, 'H3': 1, 'H4': 1, 'H5': 1, 'H6': 1, 'H7': 1, 'H8': 1, 'H9': 1, 'H10': 1, 'HJ': 1, 'HQ': 1, 'HK': 1, 'HA': 1, \
                     'S2': 1, 'S3': 1, 'S4': 1, 'S5': 1, 'S6': 1, 'S7': 1, 'S8': 1, 'S9': 1, 'S10': 1, 'SJ': 1, 'SQ': 1, 'SK': 1, 'SA': 1}

        self.cards = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'CJ', 'CQ', 'CK', 'CA', \
                     'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'DJ', 'DQ', 'DK', 'DA', \
                     'H2', 'H3', 'H4', 'H5', 'H6', 'H7', 'H8', 'H9', 'H10', 'HJ', 'HQ', 'HK', 'HA', \
                     'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8', 'S9', 'S10', 'SJ', 'SQ', 'SK', 'SA']


        self.not_in_deck = []
        random.seed(seed_value)

    

    def randomCard(self):
        while(True):
            card = random.choice(self.cards)

            if self.deck[card] == 1:
                self.deck[card] = 0
                self.not_in_deck.append(card)
                return card

    def removeCards(self,card_list):
        for card in card_list:
            self.deck[card] = 0
            self.not_in_deck.append(card)
        
    
    def resetCards(self):        
        for card in self.not_in_deck:
            self.deck[card] = 1

        self.not_in_deck = []
            
        


def monteCarloSim(hand, table_cards, num_opponents, seed_value = None):

    '''
    input examples:
    hand: ['H5', 'D2']
    table_cards: ['D5', 'DQ', 'S3'] up to 2 more cards
    num_opponents: 2
    '''
    start_time = time.time()
    win_score = 0
    tie_score = [0] * num_opponents
    #index 0 is tie with 1 opponent, index -1 is tie with all opponents
    lose_score = 0
    rounds = 2000
    #original_hand = hand.copy() #starting array for each simulation iter
    original_table_cards = table_cards.copy()
    #result will be score/rounds to determine showdown win rate in texas hold'em
    #given a starting point
    #rounds are decremented when ties occur
    if seed_value == None:
        seed_value = random.randint(1000,10000)


    deck = Deck(seed_value)

    
    iteration = 0
    while(iteration < rounds):
        iteration += 1
        #hand = original_hand.copy()
        table_cards = original_table_cards.copy()



        deck.removeCards(hand)#tick off cards in deck

        deck.removeCards(table_cards)


        opponent_hands = []#nested lists for each opponent
        for x in range(num_opponents):
            opponent_hands.append([])        

        for op_num in range(num_opponents):#append cards randomly from deck
            while(len(opponent_hands[op_num]) < 2):
                opponent_hands[op_num].append(deck.randomCard())

 
        while(len(table_cards) < 5):#fill out table_hands to 5 cards
            table_cards.append(deck.randomCard())

                
        for op_num in range(num_opponents):#merge with table hands for evaluation
            opponent_hands[op_num] = opponent_hands[op_num] + table_cards


        round_score = pe.handCompare(hand + table_cards, opponent_hands)


        if round_score == 0:#wins, losses and ties are tallied
            win_score += 1

            
        elif round_score == -1:
            lose_score += 1

        elif round_score > 0:
            tie_score[round_score-1] += 1

            

        deck.resetCards()


    return {'wins': win_score, 'ties': tie_score,\
            'losses': lose_score, 'rounds': rounds}


##import cProfile
##cProfile.run('monteCarloSim([\'H6\', \'H7\'], [\'D7\', \'C2\', \'S4\'], 2, 100)', 'monteCarloSim.profile')
##import pstats
##stats = pstats.Stats('monteCarloSim.profile')
##stats.strip_dirs().sort_stats('time').print_stats()
##
