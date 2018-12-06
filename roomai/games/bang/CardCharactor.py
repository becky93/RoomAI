#!/bin/python

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
        self.__key__  = person

    def __get_person__(self):
        return self.__person__
    person = property(__get_person__, doc="The person name of charactor")

    def __get_hp__(self):
        return self.__hp__
    hp = property(__get_hp__, doc = "The init hp of this charactor")


    def __get_key__(self):  return self.__key__
    key = property(__get_key__, doc = "The key of this charactor")

    def __deepcopy__(self, memodict={}):
        return CharactorsDict[self.__key__]


CharactorsDict = dict()
CharactorsDict[CharactorNames.Jesse_Jones] = CharactorCard(CharactorNames.Jesse_Jones, 4)
CharactorsDict[CharactorNames.Vulture_Sam] = CharactorCard(CharactorNames.Vulture_Sam, 4)
CharactorsDict[CharactorNames.Bart_Cassidy] = CharactorCard(CharactorNames.Bart_Cassidy, 4)
CharactorsDict[CharactorNames.Calamity_Janet] = CharactorCard(CharactorNames.Calamity_Janet, 4)
CharactorsDict[CharactorNames.Black_Jack]  = CharactorCard(CharactorNames.Black_Jack, 4)
CharactorsDict[CharactorNames.Jourdonnais] = CharactorCard(CharactorNames.Jourdonnais, 4)
CharactorsDict[CharactorNames.Kit_Carlson] = CharactorCard(CharactorNames.Kit_Carlson, 4)
CharactorsDict[CharactorNames.Rose_Doolan] = CharactorCard(CharactorNames.Rose_Doolan, 4)
CharactorsDict[CharactorNames.Suzy_Lafayette] = CharactorCard(CharactorNames.Suzy_Lafayette, 4)
CharactorsDict[CharactorNames.Sid_Ketchum] = CharactorCard(CharactorNames.Sid_Ketchum, 4)
CharactorsDict[CharactorNames.EI_Gringo] = CharactorCard(CharactorNames.EI_Gringo, 3)
CharactorsDict[CharactorNames.Lucky_Duke] = CharactorCard(CharactorNames.Lucky_Duke, 4)
CharactorsDict[CharactorNames.Slab_Killer] = CharactorCard(CharactorNames.Slab_Killer, 4)
CharactorsDict[CharactorNames.Paul_Regret] = CharactorCard(CharactorNames.Paul_Regret, 3)
CharactorsDict[CharactorNames.Pedro_Ramirez] = CharactorCard(CharactorNames.Pedro_Ramirez, 4)
CharactorsDict[CharactorNames.Willy_Kid] = CharactorCard(CharactorNames.Willy_Kid, 4)
