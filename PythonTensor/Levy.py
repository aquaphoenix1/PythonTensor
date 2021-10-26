from scipy.stats import levy

class Levy(object):
    @staticmethod
    def levyCalculate(x, loc=0, scale=1):
        return levy.cdf(x, loc, scale)

    @staticmethod
    def restoreLevy(x, loc=0, scale=1):
        return levy.isf(1-x, loc, scale) + 1


