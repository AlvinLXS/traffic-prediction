import tensorflow as tf


def mean_square_error(y_true, y_pred):
    return tf.metrics.mean_squared_error(y_true, y_pred, weights=None)


def root_mean_square_error(y_true, y_pred):
    return tf.metrics.root_mean_squared_error(y_true, y_pred, weights=None)
