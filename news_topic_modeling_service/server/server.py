import news_classes
import numpy as np
import os
import pandas as pd
import pickle
import sys
import tensorflow as tf
import time

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from tensorflow.contrib.learn.python.learn.estimators import model_fn
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# import packages in trainer
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'trainer'))
import news_cnn_model
learn = tf.contrib.learn

SERVER_HOST = 'localhost'
SERVER_PORT = 6060

MODEL_DIR = '../model'
MODEL_UPDATE_LAG_IN_SECONDS = 10

N_CLASSES = 5

VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'

n_words = 0

MAX_DOCUMENT_LENGTH = 500
TRAIN_TEST_SPLIT = 0.8
vocab_processor = None

classifier = None

CLASS_ENCODING = {
    'World': 1,
    'U.S.': 2,
    'Sports': 3,
    'Entertainment': 4,
    'Technology': 5 
}

def restoreVars():
    with open(VARS_FILE, 'rb') as f:
        global n_words
        n_words = pickle.load(f)

    global vocab_processor
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(
        VOCAB_PROCESSOR_SAVE_FILE)


def loadModel():
    global classifier
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_DIR)

    # TODO: fix this until https://github.com/tensorflow/tensorflow/issues/5548 is solved.
    # We have to call evaluate or predict at least once to make the restored Estimator work.
    # the below is just a dummy evaluate
    df = pd.read_csv('../data/labeled_news1.csv')
    df['class'] = df['class'].map(CLASS_ENCODING)
    df['title'].fillna('Untitled', inplace = True)
    num_train = int(len(df) * TRAIN_TEST_SPLIT)
    train_df = df[0:num_train]
    x_train = train_df['title']
    y_train = train_df['class']
    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    classifier.evaluate(x_train, y_train)
    print("Model update.")

class ReloadModelHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Reload model
        print("Model update detected. Loading new model.")
        time.sleep(MODEL_UPDATE_LAG_IN_SECONDS)
        retoreVars()
        loadModel()


def classify(text):
    text_series = pd.Series([text])
    predict_x = np.array(list(vocab_processor.transform(text_series)))
    print(predict_x)

    y_predicted = [
        p['class'] for p in classifier.predict(
            predict_x, as_iterable=True)
    ]
    print(y_predicted[0])
    topic = news_classes.class_map[str(y_predicted[0])]
    return topic



restoreVars()
loadModel()
print("Model loaded.")

# Setup watchdog
# Any file change in this model dir will trigger a ReloadModelHandler event
observer = Observer()
observer.schedule(ReloadModelHandler(), path=MODEL_DIR, recursive=False)
observer.start()

# Threading RPC Server
RPC_SERVER = SimpleJSONRPCServer((SERVER_HOST, SERVER_PORT))
RPC_SERVER.register_function(classify, 'classify')
print(("Starting RPC server on %s:%d" % (SERVER_HOST, SERVER_PORT)))
RPC_SERVER.serve_forever()