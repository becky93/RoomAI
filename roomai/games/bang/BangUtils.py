#!/bin/python

from roomai.games.bang import PlayingCardNames
Duello = "Duello"
Carabine = "Carabine"
Bang = "Bang"
Emporia = "Emporia"
Volcanic = "Volcanic"
Schofield = "Schofield"
Remington = "Remington"
Panic = "Panic"
Dynamite = "Dynamite"
WellsFargo = "WellsFargo"
Prigione = "Prigione"
Saloon = "Saloon"
Beer = "Beer"
Catling = "Catling"
CatBalou = "CatBalou"
Miss = "Miss"
StageCoach = "StageCoach"
Barrel = "Barrel"
Mustang = "Mustang"
Indian = "Indian"
Winchester = "Winchester"
Appaloosa = "Appaloosa"

class Utils:
    @classmethod
    def __generate_card_actions__(cls, env):
        turn = env.public_state_history[-1].turn
        person_state = env.person_states_history[turn][-1]
        for card in person_state.hand_cards:
            if card.name == PlayingCardNames.Duello:
                pass
            elif card.name == PlayingCardNames.Carabine:
                pass
            elif card.name == PlayingCardNames.Bang:
                pass
            elif card.name == PlayingCardNames.Emporia:
                pass
            elif card.name == PlayingCardNames.Volcanic:
                pass
            elif card.name == PlayingCardNames.Schofield:
                pass
            elif card.name == PlayingCardNames.Remington:
                pass
            elif card.name == PlayingCardNames.Panic:
                pass
            elif card.name == PlayingCardNames.Dynamite:
                pass
            elif card.name == PlayingCardNames.WellsFargo:
                pass
            elif card.name == PlayingCardNames.Prigione:
                pass
            elif card.name == PlayingCardNames.Saloon:
                pass
            elif card.name == PlayingCardNames.Beer:
                pass
            elif card.name == PlayingCardNames.Catling:
                pass
            elif card.name == PlayingCardNames.CatBalou:
                pass
            elif card.name == PlayingCardNames.Miss:
                pass
            elif card.name == PlayingCardNames.StageCoach:
                pass
            elif card.name == PlayingCardNames.Barrel:
                pass
            elif card.name == PlayingCardNames.Mustang:
                pass
            elif card.name == PlayingCardNames.Indian:
                pass
            elif card.name == PlayingCardNames.Winchester:
                pass
            elif card.name == PlayingCardNames.Appaloosa:
                pass