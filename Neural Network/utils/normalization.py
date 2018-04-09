class MinMaxNormalization(object):
    """
    MinMaxNormalization is a linear transformation of the original data, making the result fall to the [0, 1]
    """
    def __init__(self):
        pass

    def fit(self, data):
        self._min = data.min()
        self._max = data.max()
        print('max = ', self._max, 'min = ', self._min)

    def transform(self, data):
        # change to float
        data = 1. * (data - self._min) / (self._max - self._min)
        return data
