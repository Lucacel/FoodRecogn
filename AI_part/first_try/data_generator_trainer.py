from keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.client import device_lib
from model_creaton import class_to_ix, model, create_architecture, model_compliation
import tensorflow as tf

img_width = 299
img_height = 299

train_data_dir = 'res/food-101/train'
test_data_dir = 'res/food-101/test'

no_train_samples = 75750
no_test_samples = 25250

epochs = 50
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1. / 255
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

if __name__ == '__main__':

    print(device_lib.list_local_devices())

    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))

    create_architecture((299, 299, 3))
    model_compliation()
    model.summary()

    model.fit_generator(
        train_generator,
        steps_per_epoch=no_train_samples // batch_size,
        epochs=epochs,
        validation_data=test_generator,
        validation_steps=no_test_samples // batch_size)

    model.save_weights('first_learning.h5')

