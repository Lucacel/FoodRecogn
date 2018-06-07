import collections
import os
import stat
import shutil
from collections import defaultdict

import matplotlib.image as img
import numpy as np
import scipy
from keras import Sequential
from keras.models import Model
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input, decode_predictions

from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, GlobalAveragePooling2D, Dropout, BatchNormalization, Activation, Input
from keras.optimizers import SGD
from os.path import join

'''
---------------- Preparing data --------------
'''
class_to_ix = {}
ix_to_class = {}
with open('res/food-101/meta/classes.txt', 'r') as txt:
    classes = [l.strip() for l in txt.readlines()]
    class_to_ix = dict(zip(classes, range(len(classes))))
    ix_to_class = dict(zip(range(len(classes)), classes))
    class_to_ix = {v: k for k, v in ix_to_class.items()}
sorted_class_to_ix = collections.OrderedDict(sorted(class_to_ix.items()))


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, dst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass  # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def generate_dir_file_map(path):
    dir_files = defaultdict(list)
    with open(path, 'r') as txt:
        files = [l.strip() for l in txt.readlines()]
        for f in files:
            dir_name, id = f.split('/')
            dir_files[dir_name].append(id + '.jpg')
    return dir_files


def ignore_train(d, filenames):
    print(d)
    subdir = d.split('/')[-1]
    to_ignore = train_dir_files[subdir]
    return to_ignore



def ignore_test(d, filenames):
    print(d)
    subdir = d.split('/')[-1]
    to_ignore = test_dir_files[subdir]
    return to_ignore


'''
---------------- Loading Images --------------
'''


def load_images(root, min_size=299):
    all_images = []
    all_classes = []
    resize_count = 0
    invalid_count = 0
    for i, subdir in enumerate(os.listdir(root)):
        imgs = os.listdir(os.path.join(root, subdir))
        class_ix = class_to_ix[subdir]
        print(i, class_ix, subdir)
        for img_name in imgs:
            img_arr = img.imread(join(root, subdir, img_name))
            img_arr_rs = img_arr
            try:
                w, h, _ = img_arr.shape
                if w < min_size:
                    wpercent = (min_size / float(w))
                    hsize = int((float(h) * float(wpercent)))
                    img_arr_rs = scipy.misc.imresize(img_arr, (min_size, hsize))
                    resize_count += 1
                elif h < min_size:
                    hpercent = (min_size / float(h))
                    wsize = int((float(w) * float(hpercent)))
                    img_arr_rs = scipy.misc.imresize(img_arr, (wsize, min_size))
                    resize_count += 1
                all_images.append(img_arr_rs)
                all_classes.append(class_ix)
            except:
                print('Skipping bad images: ', subdir, img_name)
                invalid_count += 1
    print(len(all_images), 'images_loaded')
    print(resize_count, 'images resized')
    print(invalid_count, 'images skipped')
    return np.array(all_images), np.array(all_classes)


'''
---------------- Model Part ------------------
Creating architecture
Compiling model
TODO: Training model
'''

model = Sequential()


def create_architecture(inp_shape):
    input_shape = inp_shape
 
    model.add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same', activation='relu'))
    model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(1024, activation='relu'))
    model.add(Dense(101, activation='softmax'))

def model_compliation():
    model.compile(optimizer='rmsprop',
        loss='categorical_crossentropy',
        metrics=['accuracy'])


if __name__ == '__main__':
    if not os.path.isdir('res/food-101/test') and not os.path.isdir('res/food-101/train'):
        train_dir_files = generate_dir_file_map('res/food-101/meta/train.txt')
        test_dir_files = generate_dir_file_map('res/food-101/meta/test.txt')
        copytree('res/food-101/images', 'res/food-101/train', ignore=ignore_train)
        copytree('res/food-101/images', 'res/food-101/test', ignore=ignore_test)
    else:
        print("Train/Test files already copied into separate folders.")



