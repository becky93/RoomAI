#!/bin/python
import logging;
import sys;

project_name = "roomai";

'%(asctime)s|process:%(process)d|filename:%(filename)s|lineNum:%(lineno)d|level:%(levelno)s|log_msg:%(message)s'

logger = logging.getLogger(project_name);
handler = logging.StreamHandler(sys.stderr);
formatter = logging.Formatter("%(asctime)s - line %(lineno)d in %(filename)s - %(levelname)s - %(message)s");

logger.setLevel(logging.INFO);
handler.setLevel(logging.INFO);
handler.setFormatter(formatter);
logger.addHandler(handler);

def version():
    '''

    :return: The version of RoomAI 
    '''
    version = "0.1.1"
    print("roomai-%s" % version)
    return ("roomai-%s" % version)


def set_loglevel(level):
    '''
    set the level of log
    
    :param level: 
    :return: 
    '''
    logger.setLevel(level)
    handler.setLevel(level)

def get_logger():
    '''
    get the logger
    
    :return: 
    '''
    return logger


def make(game_name):
    if game_name == "bridge":
        import roomai.bridge
        return roomai.bridge.BridgeEnv()
    elif game_name == "sevenking":
        import roomai.sevenking
        return roomai.sevenking.SevenKingEnv()
    elif game_name == "kuhn":
        import roomai.kuhn
        return roomai.kuhn.KuhnPokerEnv()
    else:
        raise ValueError("")