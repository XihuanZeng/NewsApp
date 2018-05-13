import news_cnn_model
import numpy as np
import os
import pandas as pd
import pickle
import shutil
import tensorflow as tf

from sklearn import metrics

learn = tf.contrib.learn

REMOVE_PREVIOUS_MODEL = True

MODEL_OUTPUT_DIR = '../model/'
DATA_SET_FILE = '../data/labeled_news1.csv'
VARS_FILE = '../model/vars'
VOCAB_PROCESSOR_SAVE_FILE = '../model/vocab_procesor_save_file'
MAX_DOCUMENT_LENGTH = 100
CLASS_ENCODING = {
    'World': 1,
    'U.S.': 2,
    'Sports': 3,
    'Entertainment': 4,
    'Technology': 5 
}
N_CLASSES = 5
TRAIN_TEST_SPLIT = 0.8

# Training parms
STEPS = 200

def main(unused_argv):
    print ('hello')
    if REMOVE_PREVIOUS_MODEL:
        # Remove old model
        shutil.rmtree(MODEL_OUTPUT_DIR)
        os.mkdir(MODEL_OUTPUT_DIR)

    # Prepare training and testing data
    df = pd.read_csv(DATA_SET_FILE)
    df['class'] = df['class'].map(CLASS_ENCODING)
    df['title'].fillna('Untitled', inplace = True)
    num_train = int(len(df) * TRAIN_TEST_SPLIT)
    train_df = df[0:num_train]
    test_df = df.drop(train_df.index)

    # x - news title, y - class
    # use only title to train the topic model
    x_train = train_df['title']
    y_train = train_df['class']
    x_test = test_df['title']
    y_test = test_df['class']

    # Process vocabulary
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))

    n_words = len(vocab_processor.vocabulary_)
    print('Total words: %d' % n_words)

    # Saving n_words and vocab_processor:
    with open(VARS_FILE, 'wb') as f:  # needs to be opened in binary mode.
        pickle.dump(n_words, f)

    vocab_processor.save(VOCAB_PROCESSOR_SAVE_FILE)

    # Build model
    # This is to create customized estimator
    classifier = learn.Estimator(
        model_fn=news_cnn_model.generate_cnn_model(N_CLASSES, n_words),
        model_dir=MODEL_OUTPUT_DIR)

    # Train and predict
    classifier.fit(x_train, y_train, steps=STEPS)

    # Evaluate model
    y_predicted = [
        p['class'] for p in classifier.predict(x_test, as_iterable=True)
    ]

    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))

if __name__ == '__main__':
    tf.app.run(main=main)
