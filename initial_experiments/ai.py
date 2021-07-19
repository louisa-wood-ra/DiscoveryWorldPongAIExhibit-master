import numpy as np
from tensorflow.keras.layers import Dense, Convolution2D, Reshape, Flatten
from tensorflow.keras.models import Sequential
from exhibit.game.pong import Pong
import cv2
import os
from exhibit.shared.utils import normalize_states, discount_rewards

from tensorflow.keras.optimizers import Adam


class DQN:
    def __init__(self, gamma=0.99, epsilon=0.5, resume=True):
        self.gamma = gamma
        # creates a generic neural network architecture
        self.model = Sequential()
        self.epsilon = epsilon
        self.learning_rate = 0.001
        print("Constructing CNN")

        # hidden layer takes a pre-processed frame as input, and has 200 units

        self.model.add(Reshape((1, Pong.HEIGHT//2, Pong.WIDTH//2), input_shape=(Pong.HEIGHT//2 * Pong.WIDTH//2,)))
        self.model.add(Convolution2D(32, kernel_size=(6, 6), strides=(3, 3), padding='same', activation='relu', kernel_initializer='he_uniform'))
        self.model.add(Flatten())
        self.model.add(Dense(64, activation='relu', kernel_initializer='he_uniform'))
        self.model.add(Dense(32, activation='relu', kernel_initializer='he_uniform'))
        self.model.add(Dense(2, activation='softmax'))

        # compile the model using traditional Machine Learning losses and optimizers
        opt = Adam(learning_rate=self.learning_rate)
        self.model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        temp_file = './models/temp.h5'
        if resume:
            if os.path.exists(temp_file):
                self.load_model(temp_file)

    def load_model(self, path):
        try:
            print("Loading " + path)
            self.model.load_weights(path)
            print("Successfully loaded")
        except Exception as e:
            print("Error loading model")
            print(e)
            raise(e)

    def show_weights(self, neuron, layer=0):
        weights = self.model.get_weights()[layer][:, neuron]
        weights = weights.reshape(Pong.HEIGHT // 2, Pong.WIDTH // 2)

        weights = cv2.resize(weights, (Pong.WIDTH, Pong.HEIGHT)) + 0.5
        print(weights)
        cv2.imshow(f"DQN neuron weights {neuron}", weights)
        cv2.waitKey(0)

    def infer(self, state):
        state = state.flatten()
        state = np.expand_dims(state, axis=0)
        predictions = self.model.predict(state)[0]
        return predictions

    def retrain(self, games, epochs=20):
        states, actions, rewards = games
        rewards = rewards[:, 1]
        states = np.stack([state.flatten().astype("float32") for state in states], axis=0)
        actions = actions[:, 1]

        rewards = discount_rewards(rewards, gamma=self.gamma)
        actions[:, 0] *= rewards
        actions[:, 1] *= rewards
        Y = actions
        X = normalize_states(states)
        self.model.fit(x=X, y=Y, epochs=epochs)

    def save(self, name):
        if not os.path.exists('./models'):
            os.makedirs('./models')
        print('saving to ' + name)
        self.model.save('./models/' + name)
