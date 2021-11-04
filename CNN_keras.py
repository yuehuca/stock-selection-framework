# -*- coding: utf-8 -*-

import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
import matplotlib.pyplot as plt

def cnn_keras(array_samples_train, array_samples_test, array_targets_classification_train, 
              array_targets_classification_test, array_targets_classification_onecol_train, 
              array_targets_classification_onecol_test, array_target_train, 
              array_targets_test, seed_value, seed_value_shuffle):
    #很多随机初始值太差，同时网络太深导致一开始就难以优化，0比较稳定
        
    np.random.seed(seed_value_shuffle)
    tf.random.set_seed(seed_value)
    
    # Model / data parameters
    x_train = array_samples_train
    x_test = array_samples_test
    
    y_train = array_targets_classification_train
    y_test = array_targets_classification_test
    
    #y_train = array_targets_classification_onecol_train
    #y_test = array_targets_classification_onecol_test
    
    #直接用变化率作目标效果不佳
    #y_train = array_target_train
    #y_test = array_targets_test
    
    #混淆样本
    index_shuffle = np.arange(len(y_train))
    np.random.shuffle(index_shuffle)
    x_train = x_train[index_shuffle, :, :, :]
    y_train = y_train[index_shuffle]
    
    num_classes = y_train.shape[1]
    input_shape = x_train[0].shape
    
    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(2, kernel_size=(1, 1), activation="relu"),
            layers.Conv2D(4, kernel_size=(3, 3), activation="relu"),
            #layers.Conv2D(8, kernel_size=(1, 1), activation="relu"),
            #layers.Conv2D(16, kernel_size=(1, 1), activation="relu"),
            #layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            #layers.Conv2D(64, kernel_size=(1, 1), activation="relu"),
            #layers.Conv2D(128, kernel_size=(1, 1), activation="relu"),
            #layers.Conv2D(256, kernel_size=(3, 3), activation="relu"),
            #layers.MaxPooling2D(pool_size=(2, 2)), #池化层感觉效果一般
            #layers.Dense(10, activation="relu"), #全连接曾加上以后泛化能力反而变差
            layers.Flatten(),
            layers.Dropout(0.1),
            layers.Dense(num_classes, activation="softmax"), #二维输出时可用softmax
        ]
    )
    
    #model.summary()
    
    batch_size = len(y_train) #len(y_train)，为1时效果不佳，训练后期loss突然暴增，可能是学习率过大的原因
    epochs = 100
    
    #lr_schedule = keras.optimizers.schedules.ExponentialDecay(initial_learning_rate=0.001, decay_steps=1000, decay_rate=0.5)
    #opt = keras.optimizers.Adam(learning_rate=lr_schedule) #默认固定0.001
    model.compile(loss="mean_squared_error", optimizer="adam", metrics=["accuracy"])
    #categorical_crossentropy, mean_squared_error;默认optimizer="adam",可选optimizer=opt, metrics=["accuracy"]
    
    history_keras = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, shuffle=False, 
                              verbose=0, validation_split=0.1)
                              #validation_data=(x_test, y_test), verbose=1)
    #validation_split=0.1, validation_data=(x_test, y_test)
    
    results_test = model.predict(x_test, batch_size=len(x_test), verbose=0)
    
    #score = model.evaluate(x_train, y_train, verbose=0)
    #print("Train loss:", score[0])
    #print("Train accuracy:", score[1])
    
    validation_loss = history_keras.history['val_loss'][len(history_keras.history['val_loss']) - 1]
    validation_accuracy = history_keras.history['val_accuracy'][len(history_keras.history['val_accuracy']) - 1]
    print("Val loss:", validation_loss)
    print("Val accuracy:", validation_accuracy)
    
    #score = model.evaluate(x_test, y_test, verbose=0)
    #print("Test loss:", score[0])
    #print("Test accuracy:", score[1])

    # # list all data in history
    # history_keras.history.keys()
    # # summarize history for accuracy
    # plt.figure()
    # plt.plot(history_keras.history['accuracy'])
    # plt.plot(history_keras.history['val_accuracy'])
    # plt.title('model accuracy')
    # plt.ylabel('accuracy')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()
    # # summarize history for loss
    # plt.figure()
    # plt.plot(history_keras.history['loss'])
    # plt.plot(history_keras.history['val_loss'])
    # plt.title('model loss')
    # plt.ylabel('loss')
    # plt.xlabel('epoch')
    # plt.legend(['train', 'test'], loc='upper left')
    # plt.show()

    
    return results_test, y_train, validation_loss
    
    
