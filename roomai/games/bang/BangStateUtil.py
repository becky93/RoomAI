#!/bin/python

import roomai

class RoleNames:
    sheriff        = "sheriff"
    deputy_sheriff = "deputy_sheriff"
    outlaw         = "outlaw"
    renegade       = "renegade"

class CharactorNames:
    Bart_Cassidy   = "Bart_Cassidy"
    #Bart Cassidy = Butch Cassidy – Each time he loses a life point, he immediately draws a card from the deck. (4 life points)
    Black_Jack     = "Black_Jack"
    #Black Jack = Tom Ketchum (known as Black Jack) – During phase 1 of his turn, he must show the second card he draws: if it's a Heart or Diamond, he draws one additional card that turn (without revealing it). (4 life points)
    Calamity_Janet = "Calamity_Janet"
    #Calamity Janet = Calamity Jane – She can use "Bang!" cards as "Missed!" cards and vice versa. She is still subject to "Bang!" limitations: If she plays a Missed! card as a "Bang!", she cannot play another "Bang!" card that turn (unless she has a Volcanic in play). (4 life points)
    EI_Gringo      = "EI_Gringo"
    #El Gringo = gringo (slang Spanish word) – Each time he loses a life point due to a card played by another player, he draws a random card from the hands of that player (one card for each life). If the player has no more cards, he does not draw. (3 life points)
    Jesse_Jones    = "Jesse_Jones"
    #Jesse Jones = Jesse James – During phase 1 of his turn, he may choose to draw the first card from the deck, or randomly from the hand of any other player. Then he draws the second card from the deck. (4 life points)
    Jourdonnais    = "Jourdonnais"
    #Jourdonnais = "Frenchy" Jourdonnais, the riverboat captain in The Big Sky novel and movie (Fictional person) – He is considered to have Barrel in play at all times; he can "draw!" when he is the target of a BANG!, and on a Heart he is missed. If he has another real Barrel card in play he can count both of them, giving him two chances to cancel the BANG! before playing a Missed! (4 life points)
    Kit_Carlson    = "Kit_Carlson"
    #Kit Carlson = Kit Carson – During the phase 1 of his turn, he looks at the top three cards of the deck: he chooses 2 to draw, and puts the other one back on the top of the deck, face down. (4 life points)
    Lucky_Duke     = "Lucky_Duke"
    #Lucky Duke = Lucky Luke (Fictional person) – Each time he is required to "draw!", he flips the top two cards from the deck, and chooses the result he prefers. Discard both cards afterward. (4 life points)
    Paul_Regret    = "Paul_Regret"
    #Paul Regret = Paul Regret – The Comancheros (film) – He is considered to have a Mustang in play at all times; all other players must add 1 to the distance to him. If he has another real Mustang in play, he can count both of them, increasing all distance to him by a total of 2. (3 life points)
    Pedro_Ramirez  = "Pedro_Ramirez"
    #Pedro Ramirez = Tuco Ramirez – The Ugly in the film The Good, the Bad and the Ugly (Fictional person) – During phase 1 of his turn, he may choose to draw the first card from the top of the discard pile or from the deck. Then he draws the second card from the deck. (4 life points)
    Rose_Doolan    = "Rose_Doolan"
    #Rose Doolan = She is considered to have a Scope (Appaloosa in older versions) in play at all times; she sees the other players at a distance decreased by 1. If she has another real Scope in play, she can count both of them, reducing her distance to all other players by a total of 2. (4 life points)
    Sid_Ketchum    = "Sid_Ketchum"
    #Sid Ketchum = Tom Ketchum – At any time, he may discard 2 cards from his hand to regain one life point. If he is willing and able, he can use this ability more than once at a time. (4 life points)
    Slab_Killer    = "Slab_Killer"
    #Slab the Killer = Angel Eyes, the Bad in the film The Good, the Bad and the Ugly (Fictional person) – Players trying to cancel his BANG! cards need to play 2 Missed!. The Barrel effect, if successfully used, only counts as one Missed! (4 life points)
    Suzy_Lafayette = "Suzy_Lafayette"
    #Suzy Lafayette = As soon as she has no cards in her hand, she instantly draws a card from the draw pile. (4 life points)
    Vulture_Sam    = "Vulture_Sam"
    #Vulture Sam = Whenever a character is eliminated from the game, Sam takes all the cards that player had in his hand and in play, and adds them to his hand. (4 life points)
    Willy_Kid      = "Willy_Kid"
    #Willy the Kid = Billy the Kid – He can play any number of "Bang!" cards. (4 life points)

class CharactorCard(object):
    def __init__(self, person, hp):
        self.__person__ = person
        self.__hp__   = hp

    def __get_person__(self):
        return self.__person__
    person = property(__get_person__, doc="The person name of charactor")

    def __get_hp__(self):
        return self.__hp__
    hp = property(__get_hp__, doc = "The init hp of this charactor")

AllCharactorsDict = dict()
AllCharactorsDict[CharactorNames.Jesse_Jones] = CharactorCard(CharactorNames.Jesse_Jones,4)
AllCharactorsDict[CharactorNames.Vulture_Sam] = CharactorCard(CharactorNames.Vulture_Sam,4)
AllCharactorsDict[CharactorNames.Bart_Cassidy] = CharactorCard(CharactorNames.Bart_Cassidy,4)
AllCharactorsDict[CharactorNames.Calamity_Janet] = CharactorCard(CharactorNames.Calamity_Janet,4)
AllCharactorsDict[CharactorNames.Black_Jack]  = CharactorCard(CharactorNames.Black_Jack,4)
AllCharactorsDict[CharactorNames.Jourdonnais] = CharactorCard(CharactorNames.Jourdonnais,4)
AllCharactorsDict[CharactorNames.Kit_Carlson] = CharactorCard(CharactorNames.Kit_Carlson,4)
AllCharactorsDict[CharactorNames.Rose_Doolan] = CharactorCard(CharactorNames.Rose_Doolan,4)
AllCharactorsDict[CharactorNames.Suzy_Lafayette] = CharactorCard(CharactorNames.Suzy_Lafayette,4)
AllCharactorsDict[CharactorNames.Sid_Ketchum] = CharactorCard(CharactorNames.Sid_Ketchum,4)
AllCharactorsDict[CharactorNames.EI_Gringo] = CharactorCard(CharactorNames.EI_Gringo,3)
AllCharactorsDict[CharactorNames.Lucky_Duke] = CharactorCard(CharactorNames.Lucky_Duke,4)
AllCharactorsDict[CharactorNames.Slab_Killer] = CharactorCard(CharactorNames.Slab_Killer,4)
AllCharactorsDict[CharactorNames.Paul_Regret] = CharactorCard(CharactorNames.Paul_Regret, 3)
AllCharactorsDict[CharactorNames.Pedro_Ramirez] = CharactorCard(CharactorNames.Pedro_Ramirez, 4)
AllCharactorsDict[CharactorNames.Willy_Kid] = CharactorCard(CharactorNames.Willy_Kid,4)


class BangCardNames:
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


class BangCardSuits:
    Club    = "Club"
    Heart   = "Heart"
    Diamond = "Diamond"
    Spade   = "Spade"

class BangCardColors:
    Blue = "Blue"
    Brown = "Brown"


class BangCard(object):
    '''
    A Poker Card. \n
    A Poker Card has a point (A,2,3,4,....,K) and a suit (Spade, Heart, Diamond, Club). \n
    Different points have different ranks, for example the point 2's rank is 0, and the point A's rank is 12. \n
    Different suits have different ranks too. \n
    A Poker Card has a key (point_suit). We strongly recommend you to get a poker card by using the class function lookup with the key. \n
    Examples of the class usages: \n
    >> import roomai.games.texasholdem \n
    >> card = roomai.games.texasholdem.BangCard.lookup("2_Spade") \n
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
        lookup a BangCard with the specified key

        :param key: The specified key
        :return: The BangCard with the specified key
        '''

        logger = roomai.get_logger()
        if key not in AllPokerCardsDict:
            logger.fatal("key (%s) is not invalid poker card key"%(key))
            raise ValueError("key (%s) is not invalid poker card key"%(key))

        return AllPokerCardsDict[key]


    def __deepcopy__(self, memodict={}):
        return AllPokerCardsDict[self.key]

AllPokerCardsDict = dict()
###############################
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Carabine, BangCardSuits.Club)] = BangCard(BangCardNames.Carabine, "A", BangCardSuits.Club, BangCardColors.Blue)
for i in range(2,8):
    AllPokerCardsDict["%s-%d-%s" % (BangCardNames.Duello, i, BangCardSuits.Club)] = BangCard(BangCardNames.Bang, "%d" % (i), BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-8-%s" % (BangCardNames.Duello, BangCardSuits.Club)] = BangCard(BangCardNames.Duello, "8", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.Emporia, BangCardSuits.Club)] = BangCard(BangCardNames.Emporia, "9", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Volcanic, BangCardSuits.Club)] = BangCard(BangCardNames.Volcanic, "10", BangCardSuits.Club, BangCardColors.Blue)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Schofield, BangCardSuits.Club)] = BangCard(BangCardNames.Schofield, "J", BangCardSuits.Club, BangCardColors.Blue)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Schofield, BangCardSuits.Club)] = BangCard(BangCardNames.Schofield, "Q", BangCardSuits.Club, BangCardColors.Blue)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Remington, BangCardSuits.Club)] = BangCard(BangCardNames.Remington, "K", BangCardSuits.Club, BangCardColors.Blue)


###############################
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Panic, BangCardSuits.Heart)]          = BangCard(BangCardNames.Panic, "A", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-2-%s" % (BangCardNames.Dynamite, BangCardSuits.Heart)]       = BangCard(BangCardNames.Dynamite, "2", BangCardSuits.Heart, BangCardColors.Blue)
AllPokerCardsDict["%s-3-%s" % (BangCardNames.WellsFargo, BangCardSuits.Heart)]     = BangCard(BangCardNames.WellsFargo, "3", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-4-%s" % (BangCardNames.Prigione, BangCardSuits.Heart)]       = BangCard(BangCardNames.Prigione, "4", BangCardSuits.Heart, BangCardColors.Blue)
AllPokerCardsDict["%s-5-%s" % (BangCardNames.Saloon, BangCardSuits.Heart)]         = BangCard(BangCardNames.Saloon, "5", BangCardSuits.Heart, BangCardColors.Brown)
for i in range(6,10):
    AllPokerCardsDict["%s-%d-%s" % (BangCardNames.Beer, i, BangCardSuits.Heart)]  = BangCard(BangCardNames.Beer, "%d" % (i), BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Catling, BangCardSuits.Heart)]       = BangCard(BangCardNames.Catling, "10", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Beer, BangCardSuits.Heart)]           = BangCard(BangCardNames.Beer, "J", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Bang, BangCardSuits.Heart)]           = BangCard(BangCardNames.Bang, "Q", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.CatBalou, BangCardSuits.Heart)]       = BangCard(BangCardNames.CatBalou, "K", BangCardSuits.Heart, BangCardColors.Brown)


#################################
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Bang, BangCardSuits.Spade)]          = BangCard(BangCardNames.Bang, "A", BangCardSuits.Spade, BangCardColors.Brown)
for i in range(2,9):
    AllPokerCardsDict["%s-%d-%s" % (BangCardNames.Miss, i, BangCardSuits.Spade)]  = BangCard(BangCardNames.Miss, "%d" % (i), BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.StageCoach, BangCardSuits.Spade)]     = BangCard(BangCardNames.StageCoach, "9", BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Prigione, BangCardSuits.Spade)]      = BangCard(BangCardNames.Prigione, "10", BangCardSuits.Spade, BangCardColors.Blue)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Prigione, BangCardSuits.Spade)]       = BangCard(BangCardNames.Prigione, "J", BangCardSuits.Spade, BangCardColors.Blue)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Barrel, BangCardSuits.Spade)]       = BangCard(BangCardNames.Barrel, "Q", BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Schofield, BangCardSuits.Spade)]       = BangCard(BangCardNames.Schofield, "K", BangCardSuits.Spade, BangCardColors.Blue)

#######################################
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Bang, BangCardSuits.Diamond)]          = BangCard(BangCardNames.Bang, "A", BangCardSuits.Diamond, BangCardColors.Brown)
for i in range(2,11):
    AllPokerCardsDict["%s-%d-%s" % (BangCardNames.Bang, i, BangCardSuits.Diamond)]  = BangCard(BangCardNames.Bang, "%d" % (i), BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Bang, BangCardSuits.Diamond)]       = BangCard(BangCardNames.Bang, "J", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Bang, BangCardSuits.Diamond)]       = BangCard(BangCardNames.Bang, "Q", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Bang, BangCardSuits.Diamond)]       = BangCard(BangCardNames.Bang, "K", BangCardSuits.Diamond, BangCardColors.Brown)




##########################################
AllPokerCardsDict["%s-8-%s" % (BangCardNames.Mustang, BangCardSuits.Heart)]   = BangCard(BangCardNames.Mustang, "8", BangCardSuits.Heart, BangCardColors.Blue)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.Mustang, BangCardSuits.Heart)]   = BangCard(BangCardNames.Mustang, "9", BangCardSuits.Heart, BangCardColors.Blue)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Beer, BangCardSuits.Heart)]     = BangCard(BangCardNames.Beer, "10", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Panic, BangCardSuits.Heart)]     = BangCard(BangCardNames.Panic, "J", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Panic, BangCardSuits.Heart)]     = BangCard(BangCardNames.Panic, "Q", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Bang, BangCardSuits.Heart)]      = BangCard(BangCardNames.Bang, "K", BangCardSuits.Heart, BangCardColors.Brown)
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Bang, BangCardSuits.Heart)]      = BangCard(BangCardNames.Bang, "A", BangCardSuits.Heart, BangCardColors.Brown)


AllPokerCardsDict["%s-8-%s" % (BangCardNames.Bang, BangCardSuits.Club)]      = BangCard(BangCardNames.Bang, "8", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.Bang, BangCardSuits.Club)]      = BangCard(BangCardNames.Bang, "9", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Miss, BangCardSuits.Club)]     = BangCard(BangCardNames.Miss, "10", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Miss, BangCardSuits.Club)]      = BangCard(BangCardNames.Miss, "J", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Miss, BangCardSuits.Club)]      = BangCard(BangCardNames.Miss, "Q", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Miss, BangCardSuits.Club)]      = BangCard(BangCardNames.Miss, "K", BangCardSuits.Club, BangCardColors.Brown)
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Miss, BangCardSuits.Club)]      = BangCard(BangCardNames.Miss, "A", BangCardSuits.Club, BangCardColors.Brown)


AllPokerCardsDict["%s-8-%s" % (BangCardNames.Panic, BangCardSuits.Diamond)]           = BangCard(BangCardNames.Panic, "8", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.CatBalou, BangCardSuits.Diamond)]        = BangCard(BangCardNames.CatBalou, "9", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.CatBalou, BangCardSuits.Diamond)]       = BangCard(BangCardNames.CatBalou, "10", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.CatBalou, BangCardSuits.Diamond)]        = BangCard(BangCardNames.CatBalou, "J", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Duello, BangCardSuits.Diamond)]          = BangCard(BangCardNames.Duello, "Q", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Indian, BangCardSuits.Diamond)]          = BangCard(BangCardNames.Indian, "K", BangCardSuits.Diamond, BangCardColors.Brown)
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Indian, BangCardSuits.Diamond)]          = BangCard(BangCardNames.Indian, "A", BangCardSuits.Diamond, BangCardColors.Brown)


AllPokerCardsDict["%s-8-%s" % (BangCardNames.Winchester, BangCardSuits.Spade)]        = BangCard(BangCardNames.Winchester, "8", BangCardSuits.Spade, BangCardColors.Blue)
AllPokerCardsDict["%s-9-%s" % (BangCardNames.StageCoach, BangCardSuits.Spade)]        = BangCard(BangCardNames.StageCoach, "9", BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-10-%s" % (BangCardNames.Volcanic, BangCardSuits.Spade)]         = BangCard(BangCardNames.Volcanic, "10", BangCardSuits.Spade, BangCardColors.Blue)
AllPokerCardsDict["%s-J-%s" % (BangCardNames.Duello, BangCardSuits.Spade)]            = BangCard(BangCardNames.Duello, "J", BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-Q-%s" % (BangCardNames.Emporia, BangCardSuits.Spade)]           = BangCard(BangCardNames.Emporia, "Q", BangCardSuits.Spade, BangCardColors.Brown)
AllPokerCardsDict["%s-K-%s" % (BangCardNames.Barrel, BangCardSuits.Spade)]            = BangCard(BangCardNames.Barrel, "K", BangCardSuits.Spade, BangCardColors.Blue)
AllPokerCardsDict["%s-A-%s" % (BangCardNames.Appaloosa, BangCardSuits.Spade)]         = BangCard(BangCardNames.Appaloosa, "A", BangCardSuits.Spade, BangCardColors.Blue)


AllPokerCards = list(AllPokerCardsDict.values()) + [AllPokerCardsDict["%s-9-%s" % (BangCardNames.StageCoach, BangCardSuits.Spade)]]



if __name__ == "__main__":

    print (len(AllPokerCards))
    count = 0
    for c in AllPokerCardsDict.values():
        if c.color == BangCardColors.Blue:
            count += 1
    print ("blue", count)
