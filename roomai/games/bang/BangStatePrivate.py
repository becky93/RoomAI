#!/bin/python
<<<<<<< HEAD
=======

>>>>>>> 5f28e31e659dd7808127c3c3cc386e6892a93982
from roomai.games.common import AbstractStatePrivate

class BangStatePrivate(AbstractStatePrivate):
    def __init__(self):
<<<<<<< HEAD
        self.__library__        = []
        self.__discard_pile__   = []

    def __get_library__(self):  return tuple(self.__library__)
    library = property()
=======
        self.__library__ = []

>>>>>>> 5f28e31e659dd7808127c3c3cc386e6892a93982
