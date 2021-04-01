from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import tensorflow as tf

# # gpu utilization
no_gpu = 1
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    tf.config.experimental.set_visible_devices(gpus[no_gpu],'GPU')
    tf.config.experimental.set_memory_growth(gpus[no_gpu],True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "physical GPUs, ", len(logical_gpus), "logical GPUs")
  except RuntimeError as e:
    print(e)


class Trainer:
    def __init__(self, lr, epochs=5, batch_size=32, n_layers=2, n_width=32):
        self.lr = lr
        self.epochs = epochs
        self.batch_size = batch_size
        self.n_layers = n_layers
        self.n_width = n_width
        self.model = self.build_model()

    def build_model(self):
        inputs = keras.Input(shape=(784,))
        x = layers.Dense(self.n_width, activation='relu')(inputs)
        for _ in range(self.n_layers - 1):
            x = layers.Dense(self.n_width, activation='relu')(x)

        out = layers.Dense(10, activation='softmax')(x)
        model = keras.Model(inputs=inputs, outputs=out, name='DNN_model')

        opt = keras.optimizers.Adam(learning_rate=self.lr)
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        return model

    def train(self):
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
        x_train = x_train.reshape(60000, 784)
        x_test = x_test.reshape(10000, 784)
        x_train = x_train.astype('float32')
        x_test = x_test.astype('float32')
        x_train /= 255
        x_test /= 255

        # convert class vectors to binary class matrices
        y_train = keras.utils.to_categorical(y_train, 10)
        y_test = keras.utils.to_categorical(y_test, 10)

        history = self.model.fit(x_train, y_train,
                    batch_size=self.batch_size,
                    epochs=self.epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

        score = self.model.evaluate(x_test, y_test, verbose=0)

        print("Evaluated accuracy : ", score[1])
        return int(score[1] * 10000)

if __name__=='__main__':
    t = Trainer(0.001)
    t.train()