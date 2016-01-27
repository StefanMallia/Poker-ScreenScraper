import pokerChecks as pc

def evaluateHand(cards):
    #print(cards)

    #print(cards)
    '''
    hand_strength_dict = {#converting hand ranks into numerical values
        'HC': 0, 'Pa':100] + 'TP': 200] + 'TK': 300,
        'St': 400] + 'Fl':500] + 'FH':600] + 'FK':700] + 'SF':800}
    '''


    cards = pc.convertToRanks(cards)
    #print(cards)
    
    straight_flush = pc.isStraightFlush(cards)
    if(straight_flush != False):
        return [800] + straight_flush

    four_of_kind = pc.isFourOfKind(cards)

    if(four_of_kind != False):
        return [700] + four_of_kind


    full_house = pc.isFullHouse(cards)

    if(full_house != False):
        return [600] + full_house


    flush = pc.isFlush(cards)
    if(flush != False):
        return [500] + flush


    straight = pc.isStraight(cards)    
    if(straight != False):
        return [400] + straight

    
    three_of_kind = pc.isThreeOfKind(cards)


    if(three_of_kind != False):
        return [300] + three_of_kind


    two_pair = pc.isTwoPair(cards)

    if(two_pair != False):
        return [200] + two_pair


    pair = pc.isPair(cards)

    if(pair != False):
        return [100] + pair

    #print(cards)
    return [0] + pc.highCard(cards)





def handCompare(player_hand, opponent_hands):
    '''
    Returns 1 or 0 depending on whether player hand dominates
    all other hands
    -1 if tie is found
    
    Convert example:
    High card Queen of spades: SQHC => 12HC  =>  [0, 12] => 012
    Pair of Jacks (one of them being clubs): CJPa => 11Pa    =>  [1, 11] => 111 so     111 > 012
    '''
    #print(player_hand, opponent_hands[0])


    
    player_hand_eval = evaluateHand(player_hand)
    #print(player_hand_eval)


    opponent_hands_eval = []

    for hand in opponent_hands:        
        opponent_hands_eval.append(evaluateHand(hand))

      
    opponent_hands_eval.sort(reverse=True)



    tie_count = 0    
    for x in range(len(opponent_hands_eval)):
        if player_hand_eval == opponent_hands_eval[x]:
            tie_count += 1            
        else:
            break

    if player_hand_eval > max(opponent_hands_eval):
        return 0
    

    
    elif player_hand_eval < max(opponent_hands_eval):
        return -1

    elif tie_count > 0:# len(opponent_hands_eval):#>0:
        return tie_count
