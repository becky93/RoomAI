#!/bin/python
#!coding:utf-8

import shutil
import time
import random
import roomai.common

def remove_path(path):
    shutil.rmtree(path)

import sys
sys.path.append("/cephfs/person/gotoli/dqnalgorithm")
sys.path.append("/cephfs/person/gotoli/roomai")

import roomai
import roomai.sevenking
import dqnalgorithm
from sevenking import SevenKingModel_ThreePlayers
import tensorflow as tf

if __name__ == "__main__":

    env = roomai.sevenking.SevenKingEnv()
    train_players        = [SevenKingModel_ThreePlayers() for i in range(3)] + [roomai.common.RandomChancePlayer()]
    eval_random_players  = [None] + [roomai.common.RandomPlayer() for i in range(2)] + [roomai.common.RandomChancePlayer()]
    eval_rule_players    = [None] + [roomai.sevenking.AlwaysMaxPatternPlayer() for i in range(2)] + [roomai.common.RandomChancePlayer()]
    

    dqn = dqnalgorithm.DqnAlgorithm()
    import sevenking.sevenkingplayer
    tensorboard_address = "/cephfs/person/gotoli/dqnalgorithm/tensorboard1"
    sevenking.sevenkingplayer.remove_path(tensorboard_address)

    with tf.Graph().as_default() as g:
        ai_vs_random_score = tf.placeholder(tf.float32, [1])
        tf.summary.scalar('ai_vs_random_score', tf.reduce_mean(ai_vs_random_score))
        ai_vs_rule_score   = tf.placeholder(tf.float32, [1])
        tf.summary.scalar('ai_vs_rule_score', tf.reduce_mean(ai_vs_rule_score))
        merged_summary = tf.summary.merge_all()
        sess = tf.Session()
        writer = tf.summary.FileWriter(tensorboard_address, sess.graph)

    for i in range(10000):
        dqn.train(env=env, players=train_players, params={"num_normal_players": 3, "num_iters":10})
        eval_random_players[0] = train_players[0]
        eval_rule_players[0] = train_players[0]
        
        scores_vs_random = dqn.eval(env=env, players= eval_random_players)
        scores_vs_rule   = dqn.eval(env=env, players= eval_rule_players)

        merged_summary1 = sess.run(merged_summary, feed_dict={ai_vs_random_score: [scores_vs_random[0]], ai_vs_rule_score:[scores_vs_rule[0]]})
        writer.add_summary(merged_summary1,i)