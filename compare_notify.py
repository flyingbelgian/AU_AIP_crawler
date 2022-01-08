import pandas


class Comparison:
    def __init__(self, csv_previous, csv_current):
        panda_previous = pandas.read_csv(csv_previous)
        del panda_previous['File']
        panda_previous.set_index('Title', inplace=True)
        # print(panda_previous)
        panda_current = pandas.read_csv(csv_current)
        del panda_current['File']
        panda_current.set_index('Title', inplace=True)
        # print(panda_current)
        self.panda_difference = panda_current.compare(panda_previous, keep_shape=False)

    def getDifference(self):
        return self.panda_difference
