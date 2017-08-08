import os
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import SGD, Adagrad, Adadelta
import numpy as np
from keras.callbacks import LearningRateScheduler, Callback
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from time import time
from keras.utils.np_utils import to_categorical
import sys
from vgg16 import VGG16
from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout
from keras.callbacks import ModelCheckpoint

BASE_PATH = '/home/arassadin/develop/emotiw/data_phase3'

BATCH_SIZE = 40
GPUS = [0, 1, 2, 3]

lr_base = 0.0001
lr_curr = lr_base

opt = Adagrad(lr_base, decay=1e-4)
model = VGG16()
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

X_train = np.concatenate( 
    (np.load(os.path.join(BASE_PATH, 'X_train.npy')), 
     np.load(os.path.join(BASE_PATH, 'X_val.npy'))
    ), axis=0 )
y_train = to_categorical(
    np.concatenate( (np.load(os.path.join(BASE_PATH, 'y_train.npy')), 
                     np.load(os.path.join(BASE_PATH, 'y_val.npy'))
                    ), axis=0), num_classes=3 )
print X_train.shape, y_train.shape

gen_train = ImageDataGenerator(
    featurewise_center=False,
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    rotation_range=10,
    width_shift_range=0.,
    height_shift_range=0.,
    shear_range=0.,
    zoom_range=0.1,
    channel_shift_range=5.0,
    fill_mode='nearest',
    cval=0.,
    horizontal_flip=True,
    vertical_flip=False,
    rescale=None)
traingen = gen_train.flow(X_train, y_train, batch_size=BATCH_SIZE)

mc = ModelCheckpoint('model_release.h5', verbose=1,
    save_best_only=True, monitor='loss')

model.fit_generator(traingen,
    steps_per_epoch=int(np.ceil(3629 / float(BATCH_SIZE))),
    epochs=30,
    callbacks=[mc]
)
