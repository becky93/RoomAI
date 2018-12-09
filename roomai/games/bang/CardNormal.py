#!/bin/python

import roomai

class NormalCardNames:
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


class NormalCardSuits:
    Club    = "Club"
    Heart   = "Heart"
    Diamond = "Diamond"
    Spade   = "Spade"

class NormalCardColors:
    Blue = "Blue"
    Brown = "Brown"


class NormalCard(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (A,2,3,4,....,K) and a suit (Spade, Heart, Diamond, Club). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. \n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker normalcard by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.games.texasholdem \n
    >> normalcard = roomai.games.texasholdem.Card.lookup("2_Spade") \n
    >> normalcard.point \n
    2\n
    >> normalcard.suit\n
    Spade\n
    >> normalcard.point_rank\n
    0\n
    >> normalcard.suit_rank\n
    0\n
    >> normalcard.key\n
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
    point = property(__get_point__, doc="The point of the poker normalcard")

    def __get_suit__(self):
        return self.__suit__
    suit = property(__get_suit__, doc="The suit of the poker normalcard")


    def __get_card__(self):
        return self.__card__
    card = property(__get_card__, doc="the normalcard of the poker normalcard")

    def __get_color__(self):
        return self.__color__
    color = property(__get_color__, doc = "the border color of the poker normalcard")

    def __get_key__(self):
        return self.__key__
    key = property(__get_key__, doc="The key of the poker normalcard")



    @classmethod
    def lookup(cls, key):
        '''
        lookup a Card with the specified key

        :param key: The specified key
        :return: The Card with the specified key
        '''

        logger = roomai.get_logger()
        if key not in NormalCardsDict:
            logger.fatal("key (%s) is not invalid poker normalcard key"%(key))
            raise ValueError("key (%s) is not invalid poker normalcard key"%(key))

        return NormalCardsDict[key]


    def __deepcopy__(self, memodict={}):
        return NormalCardsDict[self.key]

NormalCardsDict = dict()
###############################
NormalCardsDict["%s-A-%s" % (NormalCardNames.Carabine, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Carabine, "A", NormalCardSuits.Club, NormalCardColors.Blue)
for i in range(2,8):
    NormalCardsDict["%s-%d-%s" % (NormalCardNames.Duello, i, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Bang, "%d" % (i), NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-8-%s" % (NormalCardNames.Duello, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Duello, "8", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-9-%s" % (NormalCardNames.Emporia, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Emporia, "9", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Volcanic, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Volcanic, "10", NormalCardSuits.Club, NormalCardColors.Blue)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Schofield, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Schofield, "J", NormalCardSuits.Club, NormalCardColors.Blue)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Schofield, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Schofield, "Q", NormalCardSuits.Club, NormalCardColors.Blue)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Remington, NormalCardSuits.Club)] = NormalCard(NormalCardNames.Remington, "K", NormalCardSuits.Club, NormalCardColors.Blue)


###############################
NormalCardsDict["%s-A-%s" % (NormalCardNames.Panic, NormalCardSuits.Heart)]          = NormalCard(NormalCardNames.Panic, "A", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-2-%s" % (NormalCardNames.Dynamite, NormalCardSuits.Heart)]       = NormalCard(NormalCardNames.Dynamite, "2", NormalCardSuits.Heart, NormalCardColors.Blue)
NormalCardsDict["%s-3-%s" % (NormalCardNames.WellsFargo, NormalCardSuits.Heart)]     = NormalCard(NormalCardNames.WellsFargo, "3", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-4-%s" % (NormalCardNames.Prigione, NormalCardSuits.Heart)]       = NormalCard(NormalCardNames.Prigione, "4", NormalCardSuits.Heart, NormalCardColors.Blue)
NormalCardsDict["%s-5-%s" % (NormalCardNames.Saloon, NormalCardSuits.Heart)]         = NormalCard(NormalCardNames.Saloon, "5", NormalCardSuits.Heart, NormalCardColors.Brown)
for i in range(6,10):
    NormalCardsDict["%s-%d-%s" % (NormalCardNames.Beer, i, NormalCardSuits.Heart)]  = NormalCard(NormalCardNames.Beer, "%d" % (i), NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Catling, NormalCardSuits.Heart)]       = NormalCard(NormalCardNames.Catling, "10", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Beer, NormalCardSuits.Heart)]           = NormalCard(NormalCardNames.Beer, "J", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Bang, NormalCardSuits.Heart)]           = NormalCard(NormalCardNames.Bang, "Q", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.CatBalou, NormalCardSuits.Heart)]       = NormalCard(NormalCardNames.CatBalou, "K", NormalCardSuits.Heart, NormalCardColors.Brown)


#################################
NormalCardsDict["%s-A-%s" % (NormalCardNames.Bang, NormalCardSuits.Spade)]          = NormalCard(NormalCardNames.Bang, "A", NormalCardSuits.Spade, NormalCardColors.Brown)
for i in range(2,9):
    NormalCardsDict["%s-%d-%s" % (NormalCardNames.Miss, i, NormalCardSuits.Spade)]  = NormalCard(NormalCardNames.Miss, "%d" % (i), NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-9-%s" % (NormalCardNames.StageCoach, NormalCardSuits.Spade)]     = NormalCard(NormalCardNames.StageCoach, "9", NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Prigione, NormalCardSuits.Spade)]      = NormalCard(NormalCardNames.Prigione, "10", NormalCardSuits.Spade, NormalCardColors.Blue)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Prigione, NormalCardSuits.Spade)]       = NormalCard(NormalCardNames.Prigione, "J", NormalCardSuits.Spade, NormalCardColors.Blue)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Barrel, NormalCardSuits.Spade)]       = NormalCard(NormalCardNames.Barrel, "Q", NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Schofield, NormalCardSuits.Spade)]       = NormalCard(NormalCardNames.Schofield, "K", NormalCardSuits.Spade, NormalCardColors.Blue)

#######################################
NormalCardsDict["%s-A-%s" % (NormalCardNames.Bang, NormalCardSuits.Diamond)]          = NormalCard(NormalCardNames.Bang, "A", NormalCardSuits.Diamond, NormalCardColors.Brown)
for i in range(2,11):
    NormalCardsDict["%s-%d-%s" % (NormalCardNames.Bang, i, NormalCardSuits.Diamond)]  = NormalCard(NormalCardNames.Bang, "%d" % (i), NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Bang, NormalCardSuits.Diamond)]       = NormalCard(NormalCardNames.Bang, "J", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Bang, NormalCardSuits.Diamond)]       = NormalCard(NormalCardNames.Bang, "Q", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Bang, NormalCardSuits.Diamond)]       = NormalCard(NormalCardNames.Bang, "K", NormalCardSuits.Diamond, NormalCardColors.Brown)




##########################################
NormalCardsDict["%s-8-%s" % (NormalCardNames.Mustang, NormalCardSuits.Heart)]   = NormalCard(NormalCardNames.Mustang, "8", NormalCardSuits.Heart, NormalCardColors.Blue)
NormalCardsDict["%s-9-%s" % (NormalCardNames.Mustang, NormalCardSuits.Heart)]   = NormalCard(NormalCardNames.Mustang, "9", NormalCardSuits.Heart, NormalCardColors.Blue)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Beer, NormalCardSuits.Heart)]     = NormalCard(NormalCardNames.Beer, "10", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Panic, NormalCardSuits.Heart)]     = NormalCard(NormalCardNames.Panic, "J", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Panic, NormalCardSuits.Heart)]     = NormalCard(NormalCardNames.Panic, "Q", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Bang, NormalCardSuits.Heart)]      = NormalCard(NormalCardNames.Bang, "K", NormalCardSuits.Heart, NormalCardColors.Brown)
NormalCardsDict["%s-A-%s" % (NormalCardNames.Bang, NormalCardSuits.Heart)]      = NormalCard(NormalCardNames.Bang, "A", NormalCardSuits.Heart, NormalCardColors.Brown)


NormalCardsDict["%s-8-%s" % (NormalCardNames.Bang, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Bang, "8", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-9-%s" % (NormalCardNames.Bang, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Bang, "9", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Miss, NormalCardSuits.Club)]     = NormalCard(NormalCardNames.Miss, "10", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Miss, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Miss, "J", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Miss, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Miss, "Q", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Miss, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Miss, "K", NormalCardSuits.Club, NormalCardColors.Brown)
NormalCardsDict["%s-A-%s" % (NormalCardNames.Miss, NormalCardSuits.Club)]      = NormalCard(NormalCardNames.Miss, "A", NormalCardSuits.Club, NormalCardColors.Brown)


NormalCardsDict["%s-8-%s" % (NormalCardNames.Panic, NormalCardSuits.Diamond)]           = NormalCard(NormalCardNames.Panic, "8", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-9-%s" % (NormalCardNames.CatBalou, NormalCardSuits.Diamond)]        = NormalCard(NormalCardNames.CatBalou, "9", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.CatBalou, NormalCardSuits.Diamond)]       = NormalCard(NormalCardNames.CatBalou, "10", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-J-%s" % (NormalCardNames.CatBalou, NormalCardSuits.Diamond)]        = NormalCard(NormalCardNames.CatBalou, "J", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Duello, NormalCardSuits.Diamond)]          = NormalCard(NormalCardNames.Duello, "Q", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Indian, NormalCardSuits.Diamond)]          = NormalCard(NormalCardNames.Indian, "K", NormalCardSuits.Diamond, NormalCardColors.Brown)
NormalCardsDict["%s-A-%s" % (NormalCardNames.Indian, NormalCardSuits.Diamond)]          = NormalCard(NormalCardNames.Indian, "A", NormalCardSuits.Diamond, NormalCardColors.Brown)


NormalCardsDict["%s-8-%s" % (NormalCardNames.Winchester, NormalCardSuits.Spade)]        = NormalCard(NormalCardNames.Winchester, "8", NormalCardSuits.Spade, NormalCardColors.Blue)
NormalCardsDict["%s-9-%s" % (NormalCardNames.StageCoach, NormalCardSuits.Spade)]        = NormalCard(NormalCardNames.StageCoach, "9", NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-10-%s" % (NormalCardNames.Volcanic, NormalCardSuits.Spade)]         = NormalCard(NormalCardNames.Volcanic, "10", NormalCardSuits.Spade, NormalCardColors.Blue)
NormalCardsDict["%s-J-%s" % (NormalCardNames.Duello, NormalCardSuits.Spade)]            = NormalCard(NormalCardNames.Duello, "J", NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-Q-%s" % (NormalCardNames.Emporia, NormalCardSuits.Spade)]           = NormalCard(NormalCardNames.Emporia, "Q", NormalCardSuits.Spade, NormalCardColors.Brown)
NormalCardsDict["%s-K-%s" % (NormalCardNames.Barrel, NormalCardSuits.Spade)]            = NormalCard(NormalCardNames.Barrel, "K", NormalCardSuits.Spade, NormalCardColors.Blue)
NormalCardsDict["%s-A-%s" % (NormalCardNames.Appaloosa, NormalCardSuits.Spade)]         = NormalCard(NormalCardNames.Appaloosa, "A", NormalCardSuits.Spade, NormalCardColors.Blue)


AllNormalCards = list(NormalCardsDict.values()) + [NormalCardsDict["%s-9-%s" % (NormalCardNames.StageCoach, NormalCardSuits.Spade)]]

if __name__ == "__main__":

    print (len(AllNormalCards))
    count = 0
    for c in NormalCardsDict.values():
        if c.color == NormalCardColors.Blue:
            count += 1
    print ("blue", count)
