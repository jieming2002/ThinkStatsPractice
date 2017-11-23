__author__ = 'Skye 2017-11-23'
# coding=utf-8

from practice import practice002

def ComputeRelativeRisk(table):
    ''' 计算各个时间区间出生的婴儿所占的比例
    延后出生
    :param pmf:
    :return:
    '''
    early = 0
    onTime = 0
    late = 0
    for week in table.lengths:
        if week > 40:
            late += 1
        elif week < 38:
            early += 1
        else:
            onTime += 1

    table.early = early / table.n
    table.onTime = onTime / table.n
    table.late = late / table.n

def main(data_dir=''):
    pool, firsts, others =  practice002.MakeTables(data_dir)

    ComputeRelativeRisk(pool)
    ComputeRelativeRisk(firsts)
    ComputeRelativeRisk(others)

    # 计算延后出生和提前出生的相对风险
    lateRiskPool = pool.late / pool.early
    print('lateRiskPool = ', lateRiskPool)

    lateRiskFirsts = firsts.late / firsts.early
    print('lateRiskFirsts = ', lateRiskFirsts)

    lateRiskOthers = others.late / others.early
    print('lateRiskOthers = ', lateRiskOthers)

if __name__ == '__main__':
    main('../data/')
