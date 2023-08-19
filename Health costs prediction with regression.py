# -*- coding: utf-8 -*-
"""fcc_predict_health_costs_with_regression.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RwyYZKHnaTraezNOQzomAftmiY0vsXvt
"""

# import libraries
!pip install -q git+https://github.com/tensorflow/docs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from IPython.display import clear_output

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling

# import data
!wget https://cdn.freecodecamp.org/project-data/health-costs/insurance.csv
dataset = pd.read_csv('insurance.csv')
dataset.tail()

dataset['sex'].replace(to_replace=['female', 'male'], value=[0, 1], inplace=True)
dataset['smoker'].replace(to_replace=['no', 'yes'], value=[0, 1], inplace=True)
dataset['region'].replace(to_replace=['southwest', 'southeast', 'northwest', 'northeast'], value=[1, 2, 3, 4], inplace=True)

# get the locations
x = dataset.iloc[:, :-1]
y = dataset.iloc[:, -1]

# split the dataset
train_dataset, test_dataset, train_labels, test_labels = train_test_split(x, y, test_size=0.2, random_state=0)

normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_dataset))
first = np.array(train_dataset[:1])

with np.printoptions(precision=2, suppress=True):
  print('First example:', first)
  print()
  print('Normalized:', normalizer(first).numpy())

def build_and_compile_model(norm):
  model = keras.Sequential([
      norm,
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
  ])

  model.compile(loss='mean_absolute_error',
                optimizer=tf.keras.optimizers.Adam(0.001))
  return model

model = build_and_compile_model(normalizer)
model.summary()

history = model.fit(
     train_dataset,
     train_labels,
     verbose=0, epochs=100)

test_results = {}

test_results['model'] = model.evaluate(test_dataset, test_labels, verbose=0)
mae = round(test_results['model'],2)

print("Testing set Mean Abs Error: {:5.2f} expenses".format(mae))

if mae < 3500:
  print("You passed the challenge. Great job!")
else:
  print("The Mean Abs Error must be less than 3500. Keep trying.")

# plot predictions
test_predictions = model.predict(test_dataset).flatten()

a = plt.axes(aspect='equal')
plt.scatter(test_labels, test_predictions, color = 'lime')
plt.xlabel('True values (expenses)')
plt.ylabel('Predictions (expenses)')
lims = [0, 50000]
plt.xlim(lims)
plt.ylim(lims)
_ = plt.plot(lims,lims,color = 'green')
