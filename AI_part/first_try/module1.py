import h5py
import keras.backend as kB
from keras import Input, Model
from keras.applications import InceptionV3
from keras.callbacks import ModelCheckpoint, CSVLogger
from keras.layers import GlobalAveragePooling2D, Dense, BatchNormalization, Activation, Dropout
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical
import numpy as np
from sklearn.model_selection import train_test_split

print("Loading metadata...")
class_to_ix = {}
ix_to_class = {}
with open('res/food-101/meta/classes.txt', 'r') as txt:
    classes = [l.strip() for l in txt.readlines()]
    class_to_ix = dict(zip(classes, range(len(classes))))
    ix_to_class = dict(zip(range(len(classes)), classes))
    class_to_ix = {v: k for k, v in ix_to_class.items()}




# ---------------Load concatenated data from disk --------------------
print('Loading X_all.hdf5')
h = h5py.File('X_all.hdf5', 'r')
X_all = np.array(h.get('data'))
Y_all = np.array(h.get('classes'))
h.close()


# ---------------Create train/val/test split -------------------------
print('Creating train/val/test/split')
n_classes = len(np.unique(Y_all))

X_train, X_val_test, Y_train, Y_val_test = train_test_split(X_all,
                                                            Y_all,
                                                            test_size=.20,
                                                            stratify=Y_all)

X_val, X_test, Y_val, Y_test = train_test_split(X_val_test,
                                                Y_val_test,
                                                test_size=.5,
                                                stratify=Y_val_test)

Y_train_cat = to_categorical(Y_train, num_classes=n_classes)
Y_val_cat = to_categorical(Y_val, num_classes=n_classes)
Y_test_cat = to_categorical(Y_test, num_classes=n_classes)

X_all = None
X_val_test = None
Y_val_test = None

print("Writing X_test.hdf5")
h = h5py.File('X_test.hdf5', 'w')
h.create_dataset('data', data=X_test)
h.create_dataset('classes', data=Y_test_cat)
h.close()

# --------------------Setup the image augmentation --------------------
print("Setting up image data generator")

datagen = ImageDataGenerator(
    featurewise_center=False,
    samplewise_center=False,
    featurewise_std_normalization=False,
    samplewise_std_normalization=False,
    zca_whitening=False,
    rotation_range=45,
    width_shift_range=0.125,
    height_shift_range=0.125,
    horizontal_flip=True,
    vertical_flip=False,
    rescale=1. / 255,
    fill_mode='nearest')

datagen.fit(X_train)
generator = datagen.flow(X_train, Y_train_cat, batch_size=32)
val_generator = datagen.flow(X_val, Y_val_cat, batch_size=32)

# Fine tuning. 70% with image augmentation.
# 83% with pre processing (14 mins).
# 84.5% with rmsprop/img.aug/dropout
# 86.09% with batchnorm/dropout/img.aug/adam(10)/rmsprop(140)
# InceptionV3

kB.clear_session()

base_model = InceptionV3(weights='imagenet', include_top=False, input_tensor=Input(shape=(299, 299, 3)))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(4096)(x)
x = BatchNormalization()(x)
x = Activation('relu')(x)
x = Dropout(.5)(x)

predictions = Dense(n_classes, activation='softmax')(x)

model = Model(input=base_model.input, output=predictions)

for layer in base_model.layers:
    layer.trainable = False

model.compile(optimizer='rmsprop', loss='categorical_crossentropy',
              metrics=['accuracy'])

print("First pass")
checkpointer = ModelCheckpoint(filepath='res/first.3.{epoch:02d}-{val_loss:.2f}.hdf5',
                               verbose=1,
                               save_best_only=True)
csv_logger = CSVLogger('first.3.log')
model.fit_generator(
    generator,
    validation_data=val_generator,
    nb_val_samples=10000,
    samples_per_epoch=X_train.shape[0],
    nb_epoch=10,
    verbose=1,
    callbacks=[csv_logger, checkpointer])

for layer in model.layers[:172]:
    layer.trainable = False
for layer in model.layers[172:]:
    layer.trainable = True

print("Second pass")

model.compile(optimizer=SGD(lr=0.0001, momentum=0.9),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
checkpointer = ModelCheckpoint(
    filepath='res/second.3.{epoch:02d}-{val_loss:.2f}.hdf5',
    verbose=1,
    save_best_only=True)

csv_logger = CSVLogger('second.3.log')

model.fit_generator(generator,
                    validation_data=val_generator,
                    nb_val_samples=10000,
                    samples_per_epoch=X_train.shape[0],
                    nb_epoch=100,
                    verbose=1,
                    callbacks=[csv_logger, checkpointer])
