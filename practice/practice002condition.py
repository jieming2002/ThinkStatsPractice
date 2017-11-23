__author__ = 'Skye 2017-11-23'
# coding=utf-8

from src import descriptive

def RemoveRange(pmf, low, high):
    ''' 将指定区间的值从分布中删除，包括两端。然后重新将数据归一化。
    :param pmf: Pmf 对象
    :param low: 区间下限
    :param high: 区间上限
    '''
    print('RemoveRange 前 total = ', pmf.Total())

    for week in range(low, high):
        prob = pmf.Prob(week)
        if prob > 0:
            pmf.Remove(week)

    print('RemoveRange 后 total = ', pmf.Total())
    pmf.Normalize()
    print('重新归一化后 total = ', pmf.Total())

def ComputeConditionalProbability(pmf, week):
    ''' 计算条件概率
    :param pmf: Pmf 对象，含有计算好的概率
    :param week: 当前是第几周
    :return:
    '''
    RemoveRange(pmf, 0, week - 1)
    return pmf.Prob(week)

def main():
    pool, firsts, others = descriptive.MakeTables('../data/')
    week = 39
    # 计算宝宝在第 39 周出生的概率（ 假设宝宝没有在 39 周前出生）
    # 第一胎
    prob = ComputeConditionalProbability(firsts.pmf, week)
    print('第一胎：', prob)

    # 其他
    prob = ComputeConditionalProbability(others.pmf, week)
    print('其他：', prob)

    # 不知道第几胎
    prob = ComputeConditionalProbability(pool.pmf, week)
    print('不知道第几胎：', prob)

if __name__ == "__main__":
    main()
