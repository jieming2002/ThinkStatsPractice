__author__ = 'Skye 2017-11-23'
# coding=utf-8
from practice import practice001
from practice import practice002

def ProbEarly(pmf):
    '''
    提前出生
    :param pmf:
    :return:
    '''
    w < 38
    pass

def ProbOnTime(pmf):
    '''
    准时出生
    :param pmf:
    :return:
    '''
    38 <= w <= 40
    pass

def ProbLate(pmf):
    '''
    延后出生
    :param pmf:
    :return:
    '''
    w > 40
    pass

def MakePmfs(data_dir):
    table, firsts, others = practice001.MakeTables(data_dir)
    pool = practice002.PoolRecords(firsts, others)
    practice002.Process(pool, '所有活婴')
    practice002.Process(firsts, '第一胎')
    practice002.Process(others, '其他胎')
    return pool, firsts, others

def main(data_dir=''):
    pool, firsts, others =  MakePmfs(data_dir)
    prob
    pass

if __name__ == '__main__':
    main('../data/')
