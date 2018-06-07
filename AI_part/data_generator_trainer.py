from keras import Sequential, Input, Model
from keras.applications import InceptionV3
from keras.callbacks import ModelCheckpoint, CSVLogger
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, GlobalAveragePooling2D, BatchNormalization, Activation, \
    Dropout
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.client import device_lib
import tensorflow as tf

'''
---------------- Architecture ------------------
'''

#
# def create_architecture(inp_shape):
#     input_shape = inp_shape
#
#     model.add(Conv2D(64, (3, 3), input_shape=input_shape, padding='same', activation='relu'))
#     model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
#
#     model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
#
#     model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(256, (3, 3), padding='same', activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
#
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
#
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(Conv2D(512, (3, 3), padding='same', activation='relu'))
#     model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
#
#     model.add(GlobalAveragePooling2D())
#     # model.add(Flatten())
#     model.add(Dense(4096))
#     model.add(BatchNormalization())
#     model.add(Activation('relu'))
#     model.add(Dropout(0.5))
#     model.add(Dense(nb_classes, activation='softmax'))
#
#
# def model_compliation():
#     sgd = SGD(lr=0.0001, decay=1e-6, momentum=0.9, nesterov=True)
#     model.compile(optimizer=sgd,
#                   loss='categorical_crossentropy',
#                   metrics=['accuracy'])
#

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
    shear_range=0.2,
    zoom_range=0.2,
    width_shift_range=0.125,
    height_shift_range=0.125,
    vertical_flip=False,
    rotation_range=45,
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.1,
    zoom_range=0.1,
    width_shift_range=0.120,
    height_shift_range=0.120,
    vertical_flip=False,
    rotation_range=40,
    horizontal_flip=True,
    fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    classes=class_to_ix
)

test_generator = test_datagen.flow_from_directory(
    test_data_dir,
    target_size=(img_width, img_height),
    batch_size=batch_size,
    class_mode='categorical',
    classes=class_to_ix
)


def create_new_model(inp_shape):
    base_model = InceptionV3(weights='imagenet', include_top=False, input_tensor=Input(shape=inp_shape))
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(4096)(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(nb_classes, activation='softmax')(x)

    model = Model(input=base_model.input, output=predictions)
    for layer in base_model.layers:
        layer.trainable = False
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


'''
---------------- Model Part ------------------
Creating architecture
Compiling model
'''


if __name__ == '__main__':
    print(device_lib.list_local_devices())

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

    model = create_new_model((299, 299, 3))

    print("First pass")
    checkpointer = ModelCheckpoint(filepath='check_points/first.3.{epoch:02d}-{val_loss:.2f}.hdf5',
                                   verbose=1, save_best_only=True)
    csv_logger = CSVLogger('first.3.log')

    model.fit_generator(
        train_generator,
        epochs=10,
        validation_data=test_generator,
        verbose=1,
        steps_per_epoch=no_train_samples // batch_size,
        validation_steps=no_test_samples // batch_size,
        callbacks=[csv_logger, checkpointer])

    for layer in model.layers[:172]:
        layer.trainable = False
    for layer in model.layers[172:]:
        layer.trainable = True

    print("Second Pass")

    model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy', metrics=['accuracy'])
    checkpointer = ModelCheckpoint(
        filepath='check_points/second.3.{epoch:02d}-{val_loss:.2f}.hdf5', verbose=1,
        save_best_only=True)
    csv_logger = CSVLogger('second.3.log')
    model.fit_generator(
        train_generator,
        epochs=epochs,
        validation_data=test_generator,
        verbose=1,
        steps_per_epoch=no_train_samples // batch_size,
        validation_steps=no_test_samples // batch_size,
        callbacks=[csv_logger, checkpointer])

    model.save_weights('learningV4.h5')
    model.save('FoodRecognModel.h5')
