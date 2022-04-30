
# Integrate to Tune
# ==================

# Now, let's use Tune to optimize a model that learns to classify Iris. This will happen in 
# two parts - modifying the training function to support Tune, and then configuring Tune.

# Let's first define a callback function to report intermediate training progress back 
# to Tune.

import tensorflow.keras as keras
from ray import tune
import inspect

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

from sklearn.datasets import load_iris

def get_iris_data(self):
    iris = load_iris()
    iris_data = iris.data # 鳶尾花特徵值(4個)
    iris_target = iris.target # 鳶尾花目標值(類別)

    return iris_data, iris_target

#from ray_tune.tf_basic_step2 import create_model


hyperparameter_space = {
    "lr": tune.loguniform(0.001, 0.1),  
    "dense_1": tune.uniform(2, 128),
    "dense_2": tune.uniform(2, 128),
}

config = hyperparameter_space

class TuneReporterCallback(keras.callbacks.Callback):
    """Tune Callback for Keras.

    The callback is invoked every epoch.
    """

    def __init__(self, logs={}):
        self.iteration = 0
        super(TuneReporterCallback, self).__init__()

    def on_epoch_end(self, batch, logs={}):
        self.iteration += 1
        tune.report(keras_info=logs, mean_accuracy=logs.get("accuracy"), mean_loss=logs.get("loss"))

### copyied from step2
def create_model(learning_rate, dense_1, dense_2):
    #assert learning_rate > 0 and dense_1 > 0 and dense_2 > 0, "Did you set the right configuration?"
    model = Sequential()
    model.add(Dense(int(dense_1), input_shape=(4,), activation='relu', name='fc1'))
    model.add(Dense(int(dense_2), activation='relu', name='fc2'))
    model.add(Dense(3, activation='softmax', name='output'))
    optimizer = SGD(lr=learning_rate)
    model.compile(optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return model


model = create_model(learning_rate=config["lr"], dense_1=config["dense_1"], dense_2=config["dense_2"])


def tune_iris():  # TODO: Change me.
    train_x, train_y, test_x, test_y = get_iris_data()
    model = create_model(learning_rate=0, dense_1=0, dense_2=0)  # TODO: Change me.
    checkpoint_callback = ModelCheckpoint(
        "model.h5", monitor='loss', save_best_only=True, save_freq=2)

    # Enable Tune to make intermediate decisions by using a Tune Callback hook. This is Keras specific.
    callbacks = [checkpoint_callback, TuneReporterCallback()]

    # Train the model
    model.fit(
        train_x, train_y,
        validation_data=(test_x, test_y),
        verbose=0,
        batch_size=10,
        epochs=20,
        callbacks=callbacks)

assert len(inspect.getargspec(tune_iris).args) == 1, "The `tune_iris` function needs to take in the arg `config`."

