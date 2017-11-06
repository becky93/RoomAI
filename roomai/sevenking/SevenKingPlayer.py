#!/bin/python

import roomai.sevenking
from roomai.sevenking import SevenKingAction
from roomai.sevenking import SevenKingPokerCard

class AlwaysFoldPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """

        if "" not in self.available_actions:
            min_card = None
            for a in self.available_actions.values():
                if a.pattern[0] == "p_0":
                    if min_card is None:    min_card = a.hand_card[0]
                    else:
                        card = a.hand_card[0]
                        if SevenKingPokerCard.compare(card, min_card) < 0 : min_card = card
            if min_card is None:
                return list(self.available_actions.values())[0]
            else:
                return SevenKingAction.lookup(min_card.key)
        else:
            return SevenKingAction("")

    def receive_info(self,info):
        """

        Args:
            info:
        """
        self.public_state      = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysNotFoldPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """
        for a in self.available_actions.values():
            if a.key != "":
                return a
        return SevenKingAction.lookup("")

    def receive_info(self, info):
        """

        Args:
            info:
        """
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysMinPlayer(roomai.common.AbstractPlayer):
    """
    """
    def take_action(self):
        """

        Returns:

        """
        min_card = None
        for a in self.available_actions.values():
            if a.pattern[0] == "p_1":
                if min_card is None:    min_card = a.cards[0]
                else:
                    card = a.cards[0]
                    if SevenKingPokerCard.compare(card, min_card) < 0 : min_card = card
        if min_card is None:
            return list(self.available_actions.values())[0]
        else:
            return SevenKingAction.lookup(min_card.key)

    def receive_info(self,info):
        """

        Args:
            info:
        """
        self.public_state      = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysMaxPlayer(roomai.common.AbstractPlayer):
    """
    always play the max available action
    """

    def take_action(self):
        """

        Returns:

        """
        max_action = SevenKingAction.lookup("")
        max_pattern = 0
        for a in self.available_actions.values():
            if(a.pattern[1]>max_pattern):
                max_pattern = a.pattern[1]
                max_action = a
            elif(a.pattern[1] == max_pattern):
                if(a.pattern[0] != 'p_0' and  (SevenKingPokerCard.compare(a.cards[-1], max_action.cards[-1])>0)):
                    max_action = a

        return max_action

    def receive_info(self, info):
        """

        Args:
            info:
        """
        self.public_state = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass

class AlwaysMaxPatternPlayer(roomai.common.AbstractPlayer):
    """
    first play the max pattern,
    then play the min cards when  pattern is equal
    """

    def take_action(self):
        """

        Returns:

        """
        max_action = SevenKingAction.lookup("")
        max_pattern = 0
        for a in self.available_actions.values():
            if(a.pattern[1]>max_pattern):
                max_pattern = a.pattern[1]
                max_action = a
            elif(a.pattern[1] == max_pattern):
                if(a.pattern[0] != 'p_0' and  (SevenKingPokerCard.compare(a.cards[-1], max_action.cards[-1])<0)):
                    max_action = a

        return max_action

    def receive_info(self, info):
        """

        Args:
            info:
        """
        self.public_state = info.public_state
        self.available_actions = info.person_state.available_actions

    def reset(self):
        """

        """
        pass