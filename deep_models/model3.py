from reprocess_data import reprocess_data1

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.callbacks import History
from tensorflow.keras.regularizers import l2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import  metrics


def model3(X_train, X_test, X_valid, y_train, y_test, y_valid):
    y_train = np.array(y_train)
    y_test = np.array(y_test)
    y_valid = np.array(y_valid)

    keras.backend.clear_session()
    np.random.seed(42)
    tf.random.set_seed(42)

    model = keras.models.Sequential([
        keras.layers.Conv2D(filters=64, kernel_size=(3, 3), padding="Same", activation="relu",
                            input_shape=(128, 128, 3)),
        keras.layers.MaxPool2D(pool_size=(2, 2), strides=(2, 2)),
        keras.layers.BatchNormalization(),
        keras.layers.Dropout(0.3),
        keras.layers.Flatten(),
        keras.layers.Dense(1024, activation="relu"),
        keras.layers.Dropout(0.2),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(512, activation="relu"),
        keras.layers.Dropout(0.5),
        keras.layers.BatchNormalization(),
        keras.layers.Dense(5, activation="softmax")
    ])

    model.summary()

    model.compile(loss="sparse_categorical_crossentropy",
                  optimizer="Adam",
                  metrics=["accuracy"])

    history = model.fit(X_train, y_train, epochs=30,
                        validation_data=(X_valid, y_valid))

    pd.DataFrame(history.history).plot(figsize=(8, 5))
    plt.grid(True)
    plt.gca().set_ylim(0, 1)
    plt.show()

    y_pred = model.predict_classes(X_test)
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print(accuracy)

    return model, history


X_train, X_test, X_valid, y_train, y_test, y_valid = reprocess_data1()
model3(X_train, X_test, X_valid, y_train, y_test, y_valid)
#accuracy = 0.5269645608628659