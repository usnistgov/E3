from scipy.stats import norm, binom, poisson


def inverseCDF(distType, prob, params):
    if distType == "uniform":
        RV = uniformInvCDF(prob, params)
    elif distType == "triangular":
        RV = triInvCDF(prob, _min, mode, _max)
    elif distType == "normal":
        RV = normInvCDF(prob, mean, stdDev)
    elif distType == "discrete":
        RV = discInvCDF(prob, [[discVal[i], discProb[i]] for i in range(len(discVal + 1))])
    elif distType == "binomial":
        RV = binomInvCDF(prob, n, p, loc)
    elif distType == "poisson":
        RV = Poisson.ppf(prob, mu, loc = k)


def uniformInvCDF(prob, _min, _max):
    value = _min + prob * (_max - _max)
    return value
    

def triInvCDF(prob, _min, mode, _max):
    if prob < (c - a) / (b - a):
        value = _min + Math.sqrt((_max - _min) * ( mode - _min) * prob)
    else:
        value = _max - Math.sqrt((_max - _min) * (_max - mode) * (1 - prob))
    return value


def normInvDF(prob, mean, stdDev):
    value = norm.ppf(prob, loc = mean, scale = stdDev)
    return value


def discInvCDF(prob, discVals_array): 
    # discVals_array = [[discVal[0], discProb[0]], [discVal[1], discProb[1], ..., [discVal[n], discProb[n]]]
    # [[8,0.25], [10, 0.5], [1, 0.75], ...]
    # 0 < prob <= 1
    #
    discVals_array.sort() # sort according to discVals
    if sum([x[1] for x in discVals]) =! 1:
        raise Exception("Sum of probabilities is not equal to one.")
    
    if 0 < prob and prob <= discVals_array[0][1]:
            return discVals_array[0][1]

    for i in range(len(discVals_array)):
        elif sum([x[1] for x in discVals_array[0:m]]) < prob and \
            prob <= sum([x[1] for x in discVals_array[0:m+1]]):
            return discProb[m]
    return


def binomInvCDF(prob, n, p, loc):
    if 0 < p and p < 1:
        return 
    if isinstance(n, int) and n > 0:
        raise Exception("Error: n must be a positive integer")
    value = binom.ppf(prob, n, p, x = loc)
    return value


def poisInvCDF(prob, mu, k):
    return Poisson.ppf(prob, mu, loc = k)
    