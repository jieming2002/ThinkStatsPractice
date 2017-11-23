__author__ = 'Skye 2017-11-23'
# coding=utf-8
# practice002risk 的优化版本
from practice import practice002

def ProbRange(pmf, low, high):
    '''
    计算指定范围内的概率总数
    :param pmf: 概率质量函数，里面有计算好的妊娠期的概率
    :param low: 最小妊娠周数
    :param high: 最大妊娠周数
    :return:
    '''
    total = 0.0
    for week in range(low, high+1): #为什么 high 要 +1
        total = pmf.Prob(week) #这里就是算好的概率，加起来即可
    return total

def ProbEarly(pmf):
    return ProbRange(pmf, 0, 37)

def ProbOnTime(pmf):
    return ProbRange(pmf, 38, 40)

def ProbLate(pmf):
    return ProbRange(pmf, 41, 50)

def ComputeRelativeRisk(first_pmf, other_pmf):
    ''' 计算相对风险
    '''
    print('计算相对风险：')
    funcs = [ProbEarly, ProbOnTime, ProbLate]
    risks = {}
    for func in funcs:
        for pmf in [first_pmf, other_pmf]:
            prob = func(pmf)
            risks[func.__name__, pmf.name] = prob
            print(func.__name__, pmf.name, prob)

    print()
    print('相对风险：第一胎 / 其他')
    for func in  funcs:
        try:
            ratio = (risks[func.__name__, '第一胎'] /
                     risks[func.__name__, '其他'])
            print(func.__name__, ratio)
        except ZeroDivisionError:
            pass

def main(data_dir=''):
    pool, firsts, others =  practice002.MakeTables(data_dir)
    ComputeRelativeRisk(firsts.pmf, others.pmf)

if __name__ == '__main__':
    main('../data/')



