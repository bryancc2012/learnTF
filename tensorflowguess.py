#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 17:05:53 2017

@author: bryancc2012
"""

import tensorflow as tf
from pandas import DataFrame as df
import numpy as np
from sklearn.model_selection import train_test_split
import math


def getwinlost(result):
    if result<0:
        resultwl=-1
    elif result == 0:
        resultwl=0
    else :
        resultwl=1
    return(resultwl)

gamedf=df.from_csv("gamedata.csv", header=None, index_col=0)

#gamedatahead=("score1","score2","asias1","asias2","asiash","asiae1","asiae2","asiaeh","eurosw","eurosd","eurosl","euroew","euroed","euroel","euroswd","eurosdd","eurosld","euroewd","euroedd","euroeld")
#gamedf.column= gamedatahead

print(len(gamedf))

gamedf=df.dropna(gamedf)

print(len(gamedf))


gamedf["result"]=gamedf[1]-gamedf[2]

gamedf["resultwl"]=gamedf["result"].apply(getwinlost)

gamedf["asiad1"]=((gamedf[6]-gamedf[3])/gamedf[3])
gamedf["asiad2"]=((gamedf[7]-gamedf[4])/gamedf[4])
gamedf["asiadh"]=((gamedf[8]-gamedf[5])/gamedf[5])
gamedf["eurodw"]=((gamedf[12]-gamedf[9])/gamedf[12])
gamedf["eurodd"]=((gamedf[13]-gamedf[10])/gamedf[13])
gamedf["eurodl"]=((gamedf[14]-gamedf[11])/gamedf[14])
gamedf.dropna()

gamedataai=gamedf[[6,7,8,12,13,14, "asiad1","asiad2","asiadh","eurodw","eurodd","eurodl"]]


xarray=np.array(gamedataai, dtype=np.float32)
yarray=np.array(gamedf["resultwl"], dtype=np.int8)
ylable=np.eye(3)[yarray]

lablelen=len(ylable)
ylable.shape=(lablelen,3)



X_train, X_test, y_train, y_test = train_test_split(xarray, ylable, test_size=0.1,random_state=0)

print (X_train.shape, y_train.shape, X_test.shape, y_test.shape)

dataset_size=len(X_train)
learning_rates = 0.0011
training_epochs = 5
batch_size = 10
training_steps= math.ceil(dataset_size/batch_size)*training_epochs

# Network Parameters
n_hidden_1 = 512 # 1st layer number of features
n_hidden_2 = 512 # 2nd layer number of features
n_hidden_3 = 512
n_input = 12 # MNIST data input (img shape: 28*28)
n_classes = 3 # MNIST total classes (0-9 digits)

# tf Graph input
with tf.name_scope("inputs"):
    x = tf.placeholder("float32",[None, n_input], name="x_input")
    y = tf.placeholder("float32",[None, n_classes], name="y_input")


# Create model
def multilayer_perceptron(x, weights, biases):
    # Hidden layer with RELU activation
    with tf.name_scope("layer1"):
        layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'], name="layer1")
        layer_1 = tf.tanh(layer_1)
        # Hidden layer with RELU activation
    with tf.name_scope("layer2"):
        layer_2 = tf.add(tf.matmul(layer_1, weights['h2']), biases['b2'], name="layer2")
        layer_2 = tf.tanh(layer_2)
        # Output layer with linear activation
    with tf.name_scope("layer3"):
        layer_3 = tf.add(tf.matmul(layer_2, weights['h3']), biases['b3'], name="layer3")
        layer_3 = tf.tanh(layer_3)
    with tf.name_scope("outlayer"):
        out_layer = tf.matmul(layer_3, weights['out']) + biases['out']
        return out_layer


with tf.name_scope("W"):
    weights = {
        'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
        'h2': tf.Variable(tf.random_normal([n_hidden_1, n_hidden_2])),
        'h3': tf.Variable(tf.random_normal([n_hidden_2, n_hidden_3])),
        'out': tf.Variable(tf.random_normal([n_hidden_3, n_classes]))
    }
with tf.name_scope("b"):
    biases = {
        'b1': tf.Variable(tf.random_normal([n_hidden_1])),
        'b2': tf.Variable(tf.random_normal([n_hidden_2])),
        'b3': tf.Variable(tf.random_normal([n_hidden_3])),
        'out': tf.Variable(tf.random_normal([n_classes]))
    }

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
with tf.name_scope("cost"):
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=pred, labels=y))
    tf.summary.scalar("cost",cost)
with tf.name_scope("optimizer"):
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rates).minimize(cost)

with tf.name_scope("accuracy"):
    correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    tf.summary.scalar("accuracy",accuracy)

# Initializing the variables
init = tf.global_variables_initializer()


# Launch the graph
with tf.Session() as sess:
    merged = tf.summary.merge_all()
    Writer = tf.summary.FileWriter("logs/", graph=sess.graph)
    sess.run(init)
    for i in range (training_steps):
        start= (i * batch_size) % dataset_size    
        end=min(start + batch_size, dataset_size)
        _, c=sess.run([optimizer, cost], feed_dict={x: X_train[start:end], y: y_train[start:end]})
        if i % 100 == 0:
            summary, total_cost=sess.run([merged,cost], feed_dict={x:X_train, y:y_train})
            print("after %d training steps, total cost is %g" %(i, total_cost))
            print("Testing Accuracy:", sess.run(accuracy, feed_dict={x: X_test, y: y_test}))
            Writer.add_summary(summary, i)
    Writer.close()

