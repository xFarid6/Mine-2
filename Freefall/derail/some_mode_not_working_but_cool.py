# code a text generating ai

# import necessary modules for artificial intelligence
import os
import random
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.layers.experimental import preprocessing
from tensorflow.keras.models import Sequential


# create a class for the model 
class Model:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.model = None
        self.history = None
        self.checkpoint_path = None
        self.checkpoint_dir = None
        self.checkpoint_callback = None
        self.loss = None
        self.accuracy = None
        self.predictions = None

    def create_model(self, units, dropout, loss, optimizer, metrics):
        self.model = Sequential()
        self.model.add(LSTM(units, input_shape=(self.data.shape[1], self.data.shape[2])))
        self.model.add(Dropout(dropout))
        self.model.add(Dense(self.data.shape[2]))
        self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)

    def train_model(self, epochs, batch_size):
        self.checkpoint_path = "training_1/cp.ckpt"
        self.checkpoint_dir = os.path.dirname(self.checkpoint_path)
        self.checkpoint_callback = ModelCheckpoint(filepath=self.checkpoint_path, save_weights_only=True, verbose=1)
        self.history = self.model.fit(self.data, epochs=epochs, batch_size=batch_size, callbacks=[self.checkpoint_callback])

    def evaluate_model(self):
        self.loss, self.accuracy = self.model.evaluate(self.data)

    def predict(self, seed):
        self.predictions = self.model.predict(seed)

    def save_model(self):
        self.model.save(self.name)

    def load_model(self):
        self.model = keras.models.load_model(self.name)

    def plot_history(self):
        hist = pd.DataFrame(self.history.history)
        hist['epoch'] = self.history.epoch
        plt.figure()
        plt.xlabel('Epoch')
        plt.ylabel('Mean Abs Error [MPG]')
        plt.plot(hist['epoch'], hist['loss'], label='Train Error')
        plt.plot(hist['epoch'], hist['val_loss'], label='Val Error')
        plt.ylim([0, 5])
        plt.legend()
        plt.show()

    def plot_predictions(self):
        plt.plot(self.predictions, label='Predictions')
        plt.legend()
        plt.show()

# create a class for the data
# needed to generate text
# the data should be a list of strings
# each string is a sentence or a paragraph or a chapter 
# or a book or a collection of books
class Data:
    def __init__(self, data):
        self.data = data
        self.data_size = len(self.data)
        self.chars = sorted(list(set(self.data)))
        self.vocab_size = len(self.chars)
        self.char_to_int = dict((c, i) for i, c in enumerate(self.chars))
        self.int_to_char = dict((i, c) for i, c in enumerate(self.chars))
        self.seq_length = 100
        self.dataX = []
        self.dataY = []
        self.n_patterns = 0
        self.X = None
        self.y = None
        # self.X = np.reshape(self.X, (self.X.shape[0], self.X.shape[1], 1))
        # self.X = self.X / float(self.vocab_size)

    def create_data(self):
        for i in range(0, self.data_size - self.seq_length, 1):
            seq_in = self.data[i:i + self.seq_length]
            seq_out = self.data[i + self.seq_length]
            self.dataX.append([self.char_to_int[char] for char in seq_in])
            self.dataY.append(self.char_to_int[seq_out])
        self.n_patterns = len(self.dataX)
        self.X = np.reshape(self.dataX, (self.n_patterns, self.seq_length, 1))
        self.X = self.X / float(self.vocab_size)
        self.y = keras.utils.to_categorical(self.dataY)

    def get_data(self):
        return self.X, self.y

# create a class for the text generator
class TextGenerator:
    def __init__(self, model, data):
        self.model = model
        self.data = data
        self.start = np.random.randint(0, len(self.data.dataX) - 1)
        self.pattern = self.data.dataX[self.start]
        self.text = ""

    def generate_text(self, n_chars):
        for i in range(n_chars):
            x = np.reshape(self.pattern, (1, len(self.pattern), 1))
            x = x / float(self.data.vocab_size)
            prediction = self.model.predict(x, verbose=0)
            index = np.argmax(prediction)
            result = self.data.int_to_char[index]
            self.text += result
            self.pattern.append(index)
            self.pattern = self.pattern[1:len(self.pattern)]
        print("Done.")

    def get_text(self):
        return self.text

# write a paragraph that should be used as training data
# the paragraph should be 20 sentences long
# the paragraph should be a string that looks from a book
paragraph = "The first sentence. The second sentence. The third sentence. The fourth sentence. The fifth sentence. The sixth sentence. The seventh sentence. The eighth sentence. The ninth sentence. The tenth sentence. The eleventh sentence. The twelfth sentence. The thirteenth sentence. The fourteenth sentence. The fifteenth sentence. The sixteenth sentence. The seventeenth sentence. The eighteenth sentence. The nineteenth sentence. The twentieth sentence."

# create a data object
data = Data(paragraph)

# create the data
data.create_data()

# get the data
X, y = data.get_data()

# create a model object
model = Model("model.h5", X)

# create the model
model.create_model(256, 0.2, "categorical_crossentropy", "adam", ["accuracy"])

# train the model
model.train_model(100, 128)

# evaluate the model
model.evaluate_model()

# create a text generator object
text_generator = TextGenerator(model.model, data)

# generate text
text_generator.generate_text(1000)

# get the generated text
text = text_generator.get_text()

# print the generated text
print(text)

# save the model
model.save_model()

