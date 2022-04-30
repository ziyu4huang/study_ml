
# creat a model training procedure (using Keras)


import numpy as np
np.random.seed(0)

import tensorflow as tf
try:
    tf.get_logger().setLevel('INFO')
except Exception as exc:
    print(exc)
import warnings
warnings.simplefilter("ignore")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from tensorflow.keras.optimizers import SGD, Adam
from tensorflow.keras.callbacks import ModelCheckpoint

import ray
from ray import tune
from ray.tune.examples.utils import get_iris_data

import inspect
import pandas as pd
import matplotlib.pyplot as plt


def create_model(learning_rate, dense_1, dense_2):
    assert learning_rate > 0 and dense_1 > 0 and dense_2 > 0, "Did you set the right configuration?"
    model = Sequential()
    model.add(Dense(int(dense_1), input_shape=(4,), activation='relu', name='fc1'))
    model.add(Dense(int(dense_2), activation='relu', name='fc2'))
    model.add(Dense(3, activation='softmax', name='output'))
    optimizer = SGD(lr=learning_rate)
    model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_on_iris():
    train_x, train_y, test_x, test_y = get_iris_data()
    model = create_model(learning_rate=0.1, dense_1=2, dense_2=2)
    # This saves the top model. `accuracy` is only available in TF2.0.
    checkpoint_callback = ModelCheckpoint(
        "model.h5", monitor='accuracy', save_best_only=True, save_freq=2)

    # Train the model
    model.fit(
        train_x, train_y,
        validation_data=(test_x, test_y),
        verbose=0, batch_size=10, epochs=20, callbacks=[checkpoint_callback])
    return model


### start run the mode
original_model = train_on_iris()  # This trains the model and returns it.
train_x, train_y, test_x, test_y = get_iris_data()
original_loss, original_accuracy = original_model.evaluate(test_x, test_y, verbose=0)
print("Loss is {:0.4f}".format(original_loss))
print("Accuracy is {:0.4f}".format(original_accuracy))


