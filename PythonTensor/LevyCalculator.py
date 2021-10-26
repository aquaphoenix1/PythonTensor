from scipy.stats import levy

class LevyCalculator(object):
    @staticmethod
    def calculate(x, loc=0, scale=1):
        return levy.cdf(x, loc, scale)


