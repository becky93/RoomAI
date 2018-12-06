#!/bin/bash


class RoleNames:
    sheriff        = "sheriff"
    deputy_sheriff = "deputy_sheriff"
    outlaw         = "outlaw"
    renegade       = "renegade"

class RoleCard(object):

    def __init__(self, role):
        self.__role__ = role

    def __get_role__(self):
        return self.__role__
    role = property(__get_role__, doc="The role")



RolesDict = dict()
RolesDict[RoleNames.sheriff]        = RoleCard(RoleNames.sheriff)
RolesDict[RoleNames.deputy_sheriff] = RoleCard(RoleNames.deputy_sheriff)
RolesDict[RoleNames.outlaw]         = RoleCard(RoleNames.outlaw)
RolesDict[RoleNames.renegade]       = RoleCard(RoleNames.renegade)