import keras
import numpy as np

from keras.layers import Embedding, LSTM
from keras.optimizers import SGD
from keras.models import Model
from keras.layers import Input, Dense
from config import m_config


class LanguageModel(object):
    def __init__(self):
        self.config = m_config

    def build_lm_model(self, inputs_x, targets):
        inputs = Input(tensor=inputs_x.get_next())
        embedding_layer = Embedding(m_config.nb_words + 1,
                                    m_config.EMBEDDING_DIM,
                                    input_length=m_config.MAX_SEQUENCE_LENGTH)
        x = embedding_layer(inputs)
        x = LSTM(
            m_config.units,
            activation='tanh',
            recurrent_activation='hard_sigmoid',
            use_bias=True,
            kernel_initializer='glorot_uniform',
            recurrent_initializer='orthogonal',
            bias_initializer='zeros',
            return_sequences=True)(x)
        x = LSTM(
            m_config.units,
            activation='tanh',
            recurrent_activation='hard_sigmoid',
            use_bias=True,
            kernel_initializer='glorot_uniform',
            recurrent_initializer='orthogonal',
            bias_initializer='zeros',
            return_sequences=True)(x)
        predictions = Dense(m_config.nb_words + 1, activation='softmax')(x)
        sgd = SGD(
            lr=m_config.sgd_lr,
            momentum=m_config.sgd_momentum,
            decay=m_config.sgd_decay,
            nesterov=False)
        model = Model(inputs=inputs, outputs=predictions)
        model.compile(
            loss='categorical_crossentropy',
            optimizer=sgd,
            metrics=['accuracy'],
            target_tensors=[
                targets.get_next()])
        history = model.fit(
            epochs=m_config.nb_epoch,
            steps_per_epoch=m_config.steps_per_epoch)
        ppl = np.exp(np.array(history.history["loss"]))
        return ppl
