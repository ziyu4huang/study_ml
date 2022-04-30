

# check original colab 
# https://colab.research.google.com/github/ray-project/tutorial/blob/master/tune_exercises/exercise_1_basics.ipynb#scrollTo=CbYE0EwkuH_D

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
plt.style.use('ggplot')
####%matplotlib inline

# Visualize your data


from sklearn.datasets import load_iris

iris = load_iris()
true_data = iris['data']
true_label = iris['target']
names = iris['target_names']
feature_names = iris['feature_names']

def plot_data(X, y):
    # Visualize the data sets
    plt.figure(figsize=(16, 6))
    plt.subplot(1, 2, 1)
    for target, target_name in enumerate(names):
        X_plot = X[y == target]
        plt.plot(X_plot[:, 0], X_plot[:, 1], linestyle='none', marker='o', label=target_name)
    plt.xlabel(feature_names[0])
    plt.ylabel(feature_names[1])
    plt.axis('equal')
    plt.legend();

    plt.subplot(1, 2, 2)
    for target, target_name in enumerate(names):
        X_plot = X[y == target]
        plt.plot(X_plot[:, 2], X_plot[:, 3], linestyle='none', marker='o', label=target_name)
    plt.xlabel(feature_names[2])
    plt.ylabel(feature_names[3])
    plt.axis('equal')
    plt.legend();

plot_data(true_data, true_label)
# trigger GUI to show it in WSL (need wslg on Windows 11 or X11 capability)
plt.show()


