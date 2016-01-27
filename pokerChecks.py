    

def convertToRanks(cards):
    '''
    Converting cards into numeric value for evaluation
    example ['H6'] --> [6, 'H'] (numeric value at index 0 for sorting
    '''
    convertDict = {'2':2, '3':3, '4':4, '5':5, '6':6,
                   '7':7, '8':8, '9':9, '10':10,
                   'J': 11, 'Q': 12, 'K': 13, 'A': 14}

    newList = [(convertDict[card[1:]], card[0]) for card in (cards)]

    newList.sort(reverse = True)

    return tuple(newList)



def isStraightFlush(cards):


    dict_list = {'C': [], 'D': [], 'H': [], 'S': []}

    #print(cards)
    for card in cards:        
        dict_list[card[1]].append(card[0])

    for key in dict_list:
        if dict_list[key] and dict_list[key][0] == 14:
            dict_list[key] =  dict_list[key] + [1]
            
        count = 0
        result_index = 0
        for x in range(len(dict_list[key])-1):
            if dict_list[key][x] - dict_list[key][x+1] == 1:
                count += 1
            else:
                count = 0
                result_index = x + 1

        
            if count == 4:
                result = [dict_list[key][result_index], key]
                return [result[0]]


    return False


def isStraight(cards):
    '''
    input example: ['H6', 'S9', 'D10', 'DQ', 'SK', 'CA', 'SA']
    checks whether there is a straight
    First converts cards into numeric values, then sorts, measure distance between successive cards
    returns highest card string if straight, else returns false
    '''



    if cards[-1] == 14:
        cards = cards + [1, cards[0][1]]

    cards2 = []
    for x in range(len(cards)):
        if(cards[x] not in cards2):
            cards2.append(cards[x])

    if cards2[0][0] == 14:
        cards2 = cards2 + [[1, cards2[0][1]]]

        

    count = 0
    result_index = 0
    for x in range(len(cards2)-1):
        if cards2[x][0] - cards2[x+1][0] == 1:
            count += 1
        else:
            count = 0
            result_index = x + 1
    
        if count == 4:
            return [cards2[result_index][0]]

    return False

def isFlush(cards):


    keys = ['C', 'D', 'H', 'S']
    for key in keys:
        cards2 = []

        for y in range(len(cards)):
            if cards[y][1] == key:
                cards2.append(cards[y][0])

        if len(cards2) == 5:
            return cards2

    return False


def isFourOfKind(cards):


    
    for x in range(len(cards)-1):
        count = 0

        for y in range(x, len(cards)):
            if cards[x][0] == cards[y][0]:
                count += 1


        if count == 4:
            kickers = []
            for card in cards:
                if card[0] != cards[x][0] and card[0] not in kickers:
                    kickers.append(card[0])

            
            return [cards[x][0]] + [kickers[0]]

    return False

def isFullHouse(cards):


    result = 0      
    for x in range(len(cards)):
        count = 0

        for y in range(len(cards)):
            if cards[x][0] == cards[y][0]:
                count += 1                

        
        if count == 3:
            cards_list = [[element for element in card] for card in cards]
            result = cards_list[x][0]
            cards_list[x][0] = 0#removing from hand to search for 3 more pair or 2 more pair
            cards_list[x+1][0] = -1#list is sorted so equal values neighbor each other
            cards_list[x+2][0] = -2
            break
    

    if result:
        for x in range(len(cards_list)):
            count = 0

            for y in range(len(cards_list)):
                if cards_list[x][0] == cards_list[y][0]:
                    count += 1 


            if count == 3 or count == 2:                    
                return [result] + [cards_list[x][0]]

    return False

    
def isThreeOfKind(cards):
    
    
    
    for x in range(len(cards)):
        count = 0

        for y in range(len(cards)):
            if cards[x][0] == cards[y][0]:
                count += 1                

        
        if count == 3:            
            kickers = []
            for card in cards:
                if card[0] != cards[x][0] and card[0] not in kickers:
                    kickers.append(card[0])
                    
            return [cards[x][0]] + kickers[0:2]

    return False




    
    
def isPair(cards):
    


    result = 0
    for x in range(len(cards)):
        count = 0

        for y in range(len(cards)):
            if cards[x][0] == cards[y][0]:
                count += 1
                

        if count == 2:
            
            kickers = []
            for card in cards:
                if card[0] != cards[x][0] and card[0] not in kickers:
                    kickers.append(card[0])
                    
            return [cards[x][0]] + kickers[0:3]
                    
    return False


def isTwoPair(cards):



    result = []
    for x in range(len(cards)):
        count = 0

        for y in range(len(cards)):
            if cards[x][0] == cards[y][0]:
                count += 1
                

        if count == 2 and cards[x][0] not in result:
            result.append(cards[x][0])


    if len(result) == 2:
        kickers = []
        for card in cards:
            if card[0] not in result and card[0] not in kickers:
                kickers.append(card[0])

        return [result[0]] + [result[1]] + [kickers[0]]
    else:
        return False
        
    


def highCard(cards):


    return [result[0] for result in cards[0:5]]

