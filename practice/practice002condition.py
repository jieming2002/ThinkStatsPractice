__author__ = 'Skye 2017-11-23'
# coding=utf-8

import descriptive

def ProbRange(pmf, low, high):
    ''' 计算执行区间的总概率，包括两端
    :param pmf: Pmf 对象
    :param low: 区间下限
    :param high: 区间上限
    :return: 概率，浮点数
    '''
    total = 0.0
    for week in range(low, high+1):
        total += pmf.Prob(week)
    return total

def ProbEarly(pmf):
    ''' 计算提前出生的概率 小于等于 37 周
    :param pmf: Pmf 对象
    :return:浮点数，概率
    '''
    return ProbRange(pmf, 0, 37)

def ProbOnTime(pmf):
    ''' 计算 38 周到 40 周出生的概率
    :param pmf: Pmf object
    :return: float probability
    '''
    return ProbRange(pmf, 38, 40)

def ProbLate(pmf):
    ''' Computes the probability of a birth in Week 41 or later.
    :param pmf: Pmf object
    :return: float probability
    '''
    return ProbRange(pmf, 41, 50)

def ComputeRelativeRisk(first_pmf, other_pmf):
    ''' Computes relative risks for two PMFs.
    :param first_pmf:  Pmf object
    :param other_pmf: Pmf object
    :return:
    '''
    print( '风险计算:')
    funcs = [ProbEarly, ProbOnTime, ProbLate]
    risks = {}
    for func in funcs:
        for pmf in [first_pmf, other_pmf]:
            prob = func(pmf)
            risks[func.__name__, pmf.name] = prob
            print(func.__name__, pmf.name, prob)

    print()
    print('风险比例 (第一胎 / 其他):')
    for func in funcs:
        try:
            ratio = (risks[func.__name__, 'first babies'] /
                     risks[func.__name__, 'others'])
            print(func.__name__, ratio)
        except ZeroDivisionError:
            pass

def main():
    pool, firsts, others = descriptive.MakeTables('../data/')
    ComputeRelativeRisk(firsts.pmf, others.pmf)

if __name__ == "__main__":
    main()
