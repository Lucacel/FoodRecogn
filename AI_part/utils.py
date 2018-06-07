import matplotlib.pyplot as plt
import os
import numpy as np
import time
from keras.preprocessing.image import ImageDataGenerator

"""
random images for each class
"""


def get_random_imgs():
    root_dir = 'res/food-101/images/'
    rows = 17
    cols = 6
    fig, ax = plt.subplots(rows, cols, figsize=(15, 25))
    sorted_food_dirs = sorted(os.listdir(root_dir))
    for i in range(rows):
        for j in range(cols):
            try:
                food_dir = sorted_food_dirs[i * cols + j]
            except:
                break
            all_files = os.listdir(os.path.join(root_dir, food_dir))
            rand_img = np.random.choice(all_files)
            img = plt.imread(os.path.join(root_dir, food_dir, rand_img))
            ax[i][j].imshow(img)
            ec = (0, .6, .1)
            fc = (0, .7, .2)
            ax[i][j].text(0, -20, food_dir, size=10, rotation=10, ha="left", va="top",
                          bbox=dict(ec=ec, fc=fc))
    plt.setp(ax, xticks=[], yticks=[])
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def get_augmented_exemples():
    class_to_ix = {}
    ix_to_class = {}
    with open('res/food-101/meta/classes.txt', 'r') as txt:
        classes = [l.strip() for l in txt.readlines()]
        class_to_ix = dict(zip(classes, range(len(classes))))
        ix_to_class = dict(zip(range(len(classes)), classes))
        class_to_ix = {v: k for k, v in ix_to_class.items()}

    img_width = 299
    img_height = 299
    nb_classes = 101
    train_data_dir = 'res/food-101/train'
    test_data_dir = 'res/food-101/test'

    no_train_samples = 75750
    no_test_samples = 25250

    epochs = 100
    batch_size = 32

    # ---------Image Augmentation--------------#

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        vertical_flip=False,
        rotation_range=45,
        horizontal_flip=True,
        zca_whitening=True,
        zca_epsilon=1e-4,
        shear_range=0.2,
        zoom_range=0.2,
        width_shift_range=0.125,
        height_shift_range=0.125,
        fill_mode='nearest'
    )

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode='categorical',
        classes=class_to_ix
    )
    for j in range (0, 10):
        x, y = train_generator.next()
        for i in range(0, 1):
            image = x[i]
            plt.imshow(image)
            plt.show()
        time.sleep(3)


if __name__ == '__main__':
    # get_random_imgs()
    get_augmented_exemples()
