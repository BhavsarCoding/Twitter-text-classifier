import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("your data location")

sentences_train = []
labels_train = []
df.shape[0]

X_train = df["text"].iloc[0:6090]
Y_train = df["target"].iloc[0:6090]

for i in range(0,X_train.shape[0]):
    
    sentences_train.append(X_train[i])
    labels_train.append(Y_train[i])
    
tokens_train = Tokenizer(oov_token = "<OOV>")
tokens_train.fit_on_texts(sentences_train)
word_index = tokens_train.word_index
sequences_train = tokens_train.texts_to_sequences(sentences_train)
padded_train = pad_sequences(sequences_train,padding = "post")
print(padded_train[0])
print(padded_train.shape)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(19322,64),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(32, activation = "relu"),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(8, activation = 'relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation = 'sigmoid')
 ])
model.compile(loss = 'binary_crossentropy',optimizer = 'adam',metrics = ['accuracy'])

filepath = "bestmodelweights.hdf5"
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath, monitor='val_accuracy')
verbes = tf.keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=10)

sentences_val = []
labels_val = []

for i in range(6090,7613):
    
    sentences_val.append(df["text"][i])
    labels_val.append(df["target"][i])
    
sequences_val = tokens_train.texts_to_sequences(sentences_val)
padded_val = pad_sequences(sequences_val,padding = "post")
print(padded_val[0])
print(padded_val.shape)
Y_test = df["target"].iloc[6090:]


num_epochs = 4
training = model.fit(padded_train,Y_train,epochs = num_epochs,callbacks=[checkpoint],validation_data=(padded_val,Y_test ))
