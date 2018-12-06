#!/bin/python

import roomai

class CardNames:
    Duello      = "Duello"
    Carabine    = "Carabine"
    Bang        = "Bang"
    Emporia     = "Emporia"
    Volcanic    = "Volcanic"
    Schofield   = "Schofield"
    Remington   = "Remington"
    Panic       = "Panic"
    Dynamite    = "Dynamite"
    WellsFargo  = "WellsFargo"
    Prigione    = "Prigione"
    Saloon      = "Saloon"
    Beer        = "Beer"
    Catling     = "Catling"
    CatBalou    = "CatBalou"
    Miss        = "Miss"
    StageCoach  = "StageCoach"
    Barrel      = "Barrel"
    Mustang     = "Mustang"
    Indian      = "Indian"
    Winchester  = "Winchester"
    Appaloosa   = "Appaloosa"


class CardSuits:
    Club    = "Club"
    Heart   = "Heart"
    Diamond = "Diamond"
    Spade   = "Spade"

class CardColors:
    Blue = "Blue"
    Brown = "Brown"


class Card(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (A,2,3,4,....,K) and a suit (Spade, Heart, Diamond, Club). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. \n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker card by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.games.texasholdem \n
    >> card = roomai.games.texasholdem.Card.lookup("2_Spade") \n
    >> card.point \n
    2\n
    >> card.suit\n
    Spade\n
    >> card.point_rank\n
    0\n
    >> card.suit_rank\n
    0\n
    >> card.key\n
    "2_Spade"\n
    '''

    def __init__(self, card, point, suit, color):

        self.__point__      = point
        self.__suit__       = suit
        self.__card__       = card
        self.__color__      = color
        self.__key__ = "%s-%s-%s" % (self.__card__, self.__point__, self.__suit__)

    def __get_point__(self):
        return self.__point__
    point = property(__get_point__, doc="The point of the poker card")

    def __get_suit__(self):
        return self.__suit__
    suit = property(__get_suit__, doc="The suit of the poker card")


    def __get_card__(self):
        return self.__card__
    card = property(__get_card__, doc="the card of the poker card")

    def __get_color__(self):
        return self.__color__
    color = property(__get_color__, doc = "the border color of the poker card")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the poker card")



    @classmethod
    def lookup(cls, key):
        '''
        lookup a Card with the specified key

        :param key: The specified key
        :return: The Card with the specified key
        '''

        logger = roomai.get_logger()
        if key not in CardsDict:
            logger.fatal("key (%s) is not invalid poker card key"%(key))
            raise ValueError("key (%s) is not invalid poker card key"%(key))

        return CardsDict[key]


    def __deepcopy__(self, memodict={}):
        return CardsDict[self.key]

CardsDict = dict()
###############################
CardsDict["%s-A-%s" % (CardNames.Carabine, CardSuits.Club)] = Card(CardNames.Carabine, "A", CardSuits.Club, CardColors.Blue)
for i in range(2,8):
    CardsDict["%s-%d-%s" % (CardNames.Duello, i, CardSuits.Club)] = Card(CardNames.Bang, "%d" % (i), CardSuits.Club, CardColors.Brown)
CardsDict["%s-8-%s" % (CardNames.Duello, CardSuits.Club)] = Card(CardNames.Duello, "8", CardSuits.Club, CardColors.Brown)
CardsDict["%s-9-%s" % (CardNames.Emporia, CardSuits.Club)] = Card(CardNames.Emporia, "9", CardSuits.Club, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.Volcanic, CardSuits.Club)] = Card(CardNames.Volcanic, "10", CardSuits.Club, CardColors.Blue)
CardsDict["%s-J-%s" % (CardNames.Schofield, CardSuits.Club)] = Card(CardNames.Schofield, "J", CardSuits.Club, CardColors.Blue)
CardsDict["%s-Q-%s" % (CardNames.Schofield, CardSuits.Club)] = Card(CardNames.Schofield, "Q", CardSuits.Club, CardColors.Blue)
CardsDict["%s-K-%s" % (CardNames.Remington, CardSuits.Club)] = Card(CardNames.Remington, "K", CardSuits.Club, CardColors.Blue)


###############################
CardsDict["%s-A-%s" % (CardNames.Panic, CardSuits.Heart)]          = Card(CardNames.Panic, "A", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-2-%s" % (CardNames.Dynamite, CardSuits.Heart)]       = Card(CardNames.Dynamite, "2", CardSuits.Heart, CardColors.Blue)
CardsDict["%s-3-%s" % (CardNames.WellsFargo, CardSuits.Heart)]     = Card(CardNames.WellsFargo, "3", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-4-%s" % (CardNames.Prigione, CardSuits.Heart)]       = Card(CardNames.Prigione, "4", CardSuits.Heart, CardColors.Blue)
CardsDict["%s-5-%s" % (CardNames.Saloon, CardSuits.Heart)]         = Card(CardNames.Saloon, "5", CardSuits.Heart, CardColors.Brown)
for i in range(6,10):
    CardsDict["%s-%d-%s" % (CardNames.Beer, i, CardSuits.Heart)]  = Card(CardNames.Beer, "%d" % (i), CardSuits.Heart, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.Catling, CardSuits.Heart)]       = Card(CardNames.Catling, "10", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-J-%s" % (CardNames.Beer, CardSuits.Heart)]           = Card(CardNames.Beer, "J", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Bang, CardSuits.Heart)]           = Card(CardNames.Bang, "Q", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.CatBalou, CardSuits.Heart)]       = Card(CardNames.CatBalou, "K", CardSuits.Heart, CardColors.Brown)


#################################
CardsDict["%s-A-%s" % (CardNames.Bang, CardSuits.Spade)]          = Card(CardNames.Bang, "A", CardSuits.Spade, CardColors.Brown)
for i in range(2,9):
    CardsDict["%s-%d-%s" % (CardNames.Miss, i, CardSuits.Spade)]  = Card(CardNames.Miss, "%d" % (i), CardSuits.Spade, CardColors.Brown)
CardsDict["%s-9-%s" % (CardNames.StageCoach, CardSuits.Spade)]     = Card(CardNames.StageCoach, "9", CardSuits.Spade, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.Prigione, CardSuits.Spade)]      = Card(CardNames.Prigione, "10", CardSuits.Spade, CardColors.Blue)
CardsDict["%s-J-%s" % (CardNames.Prigione, CardSuits.Spade)]       = Card(CardNames.Prigione, "J", CardSuits.Spade, CardColors.Blue)
CardsDict["%s-Q-%s" % (CardNames.Barrel, CardSuits.Spade)]       = Card(CardNames.Barrel, "Q", CardSuits.Spade, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Schofield, CardSuits.Spade)]       = Card(CardNames.Schofield, "K", CardSuits.Spade, CardColors.Blue)

#######################################
CardsDict["%s-A-%s" % (CardNames.Bang, CardSuits.Diamond)]          = Card(CardNames.Bang, "A", CardSuits.Diamond, CardColors.Brown)
for i in range(2,11):
    CardsDict["%s-%d-%s" % (CardNames.Bang, i, CardSuits.Diamond)]  = Card(CardNames.Bang, "%d" % (i), CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-J-%s" % (CardNames.Bang, CardSuits.Diamond)]       = Card(CardNames.Bang, "J", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Bang, CardSuits.Diamond)]       = Card(CardNames.Bang, "Q", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Bang, CardSuits.Diamond)]       = Card(CardNames.Bang, "K", CardSuits.Diamond, CardColors.Brown)




##########################################
CardsDict["%s-8-%s" % (CardNames.Mustang, CardSuits.Heart)]   = Card(CardNames.Mustang, "8", CardSuits.Heart, CardColors.Blue)
CardsDict["%s-9-%s" % (CardNames.Mustang, CardSuits.Heart)]   = Card(CardNames.Mustang, "9", CardSuits.Heart, CardColors.Blue)
CardsDict["%s-10-%s" % (CardNames.Beer, CardSuits.Heart)]     = Card(CardNames.Beer, "10", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-J-%s" % (CardNames.Panic, CardSuits.Heart)]     = Card(CardNames.Panic, "J", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Panic, CardSuits.Heart)]     = Card(CardNames.Panic, "Q", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Bang, CardSuits.Heart)]      = Card(CardNames.Bang, "K", CardSuits.Heart, CardColors.Brown)
CardsDict["%s-A-%s" % (CardNames.Bang, CardSuits.Heart)]      = Card(CardNames.Bang, "A", CardSuits.Heart, CardColors.Brown)


CardsDict["%s-8-%s" % (CardNames.Bang, CardSuits.Club)]      = Card(CardNames.Bang, "8", CardSuits.Club, CardColors.Brown)
CardsDict["%s-9-%s" % (CardNames.Bang, CardSuits.Club)]      = Card(CardNames.Bang, "9", CardSuits.Club, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.Miss, CardSuits.Club)]     = Card(CardNames.Miss, "10", CardSuits.Club, CardColors.Brown)
CardsDict["%s-J-%s" % (CardNames.Miss, CardSuits.Club)]      = Card(CardNames.Miss, "J", CardSuits.Club, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Miss, CardSuits.Club)]      = Card(CardNames.Miss, "Q", CardSuits.Club, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Miss, CardSuits.Club)]      = Card(CardNames.Miss, "K", CardSuits.Club, CardColors.Brown)
CardsDict["%s-A-%s" % (CardNames.Miss, CardSuits.Club)]      = Card(CardNames.Miss, "A", CardSuits.Club, CardColors.Brown)


CardsDict["%s-8-%s" % (CardNames.Panic, CardSuits.Diamond)]           = Card(CardNames.Panic, "8", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-9-%s" % (CardNames.CatBalou, CardSuits.Diamond)]        = Card(CardNames.CatBalou, "9", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.CatBalou, CardSuits.Diamond)]       = Card(CardNames.CatBalou, "10", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-J-%s" % (CardNames.CatBalou, CardSuits.Diamond)]        = Card(CardNames.CatBalou, "J", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Duello, CardSuits.Diamond)]          = Card(CardNames.Duello, "Q", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Indian, CardSuits.Diamond)]          = Card(CardNames.Indian, "K", CardSuits.Diamond, CardColors.Brown)
CardsDict["%s-A-%s" % (CardNames.Indian, CardSuits.Diamond)]          = Card(CardNames.Indian, "A", CardSuits.Diamond, CardColors.Brown)


CardsDict["%s-8-%s" % (CardNames.Winchester, CardSuits.Spade)]        = Card(CardNames.Winchester, "8", CardSuits.Spade, CardColors.Blue)
CardsDict["%s-9-%s" % (CardNames.StageCoach, CardSuits.Spade)]        = Card(CardNames.StageCoach, "9", CardSuits.Spade, CardColors.Brown)
CardsDict["%s-10-%s" % (CardNames.Volcanic, CardSuits.Spade)]         = Card(CardNames.Volcanic, "10", CardSuits.Spade, CardColors.Blue)
CardsDict["%s-J-%s" % (CardNames.Duello, CardSuits.Spade)]            = Card(CardNames.Duello, "J", CardSuits.Spade, CardColors.Brown)
CardsDict["%s-Q-%s" % (CardNames.Emporia, CardSuits.Spade)]           = Card(CardNames.Emporia, "Q", CardSuits.Spade, CardColors.Brown)
CardsDict["%s-K-%s" % (CardNames.Barrel, CardSuits.Spade)]            = Card(CardNames.Barrel, "K", CardSuits.Spade, CardColors.Blue)
CardsDict["%s-A-%s" % (CardNames.Appaloosa, CardSuits.Spade)]         = Card(CardNames.Appaloosa, "A", CardSuits.Spade, CardColors.Blue)


AllCards = list(CardsDict.values()) + [CardsDict["%s-9-%s" % (CardNames.StageCoach, CardSuits.Spade)]]

if __name__ == "__main__":

    print (len(AllCards))
    count = 0
    for c in CardsDict.values():
        if c.color == CardColors.Blue:
            count += 1
    print ("blue", count)
