#!/bin/python
#!coding:utf-8

import sys
sys.path.append("/cephfs/person/gotoli/dqnalgorithm")
sys.path.append("/cephfs/person/gotoli/roomai")

import shutil
import time
import random
import roomai.common

def remove_path(path):
    shutil.rmtree(path)



import roomai
import roomai.sevenking
import roomai.common
from models.dqn.sevenking import SevenKingModel_ThreePlayers
from models.dqn.dqnalgorithm import DqnAlgorithm
import tensorflow as tf
import models

if __name__ == "__main__":

    env = roomai.sevenking.SevenKingEnv()
    train_players        = [SevenKingModel_ThreePlayers()] + [roomai.sevenking.AlwaysMaxPatternPlayer()] + [roomai.common.RandomChancePlayer()]
    eval_random_players  = [None] + [roomai.common.RandomPlayer() for i in range(2)] + [roomai.common.RandomChancePlayer()]
    eval_rule_players    = [None] + [roomai.sevenking.AlwaysMaxPatternPlayer() for i in range(2)] + [roomai.common.RandomChancePlayer()]
    

    dqn = DqnAlgorithm()
    tensorboard_address = "/cephfs/person/gotoli/dqn/tensorboard_vs_rule"
    models.dqn.sevenking.sevenkingplayer.remove_path(tensorboard_address)

    with tf.Graph().as_default() as g:
        ai_vs_random_score = tf.placeholder(tf.float32, [1])
        tf.summary.scalar('ai_vs_random_score', tf.reduce_mean(ai_vs_random_score))
        ai_vs_rule_score   = tf.placeholder(tf.float32, [1])
        tf.summary.scalar('ai_vs_rule_score', tf.reduce_mean(ai_vs_rule_score))
        merged_summary = tf.summary.merge_all()
        sess = tf.Session()
        writer = tf.summary.FileWriter(tensorboard_address, sess.graph)

    for i in range(10000):
        dqn.train(env=env, players=train_players, params={"num_normal_players": 3, "num_iters":50})
        eval_random_players[0] = train_players[0]
        eval_rule_players[0] = train_players[0]
        
        scores_vs_random = dqn.eval(env=env, players= eval_random_players)
        scores_vs_rule   = dqn.eval(env=env, players= eval_rule_players)

        merged_summary1 = sess.run(merged_summary, feed_dict={ai_vs_random_score: [scores_vs_random[0]], ai_vs_rule_score:[scores_vs_rule[0]]})
        writer.add_summary(merged_summary1,i)