__author__ = 'Skye 2017-11-20'
# coding=utf-8

''' 习题1-3 第一胎婴儿出生较晚
习题1-4 思考自己感兴趣的问题，转换成统计学问题。
共享单车，外卖订单
周末骑车的人比平时少？
周末骑行距离比平时长？
周末骑行人群分布和平时不同？

结论不可靠的原因：（数据或分析的）缺陷、误差、错误
数据：不同的数据来源。对数据预处理，或寻找更好的。数据要尽可能地可靠。
分析：不同的分析方法。改进分析方法，或寻找更好的。方法要尽可能地精确。
'''
import survey
import thinkstats
import math
import Pmf
from matplotlib import pyplot

def outcomeLive(table):
    ''' 计算其中活婴的数量
    :param table: 怀孕调查统计表
    :return:活婴的数量
    '''
    count = 0
    for p in table.records:
        if p.outcome == 1:
            count += 1
    print('活婴的数量：', count)
    return count

def Mean(t):
    ''' 计算数字序列的平均数
    :param t: 数字序列
    :return:平均数
    '''
    return float(sum(t) / len(t))

def PartitionRecords(table):
    ''' 把总表分成两个表：第一胎、其他
    :param table: 怀孕调查数据表
    :return: 分开的两个表：第一胎、其他
    '''
    firsts = survey.Pregnancies() #创建类实例
    others = survey.Pregnancies()

    for p in table.records: #遍历数据表 p 是一条记录
        if p.outcome != 1: # 跳过没有存活的婴儿
            continue

        if p.birthord == 1:  # 第一胎
            firsts.AddRecord(p)
        else:
            others.AddRecord(p)

    return firsts, others

def Process(table):
    '''返回 table 的分析结果
    参数： table 对象
    '''
    # 遍历数据表的所有记录，读取其中的妊娠期字段 prglength
    table.lengths = [p.prglength for p in table.records]
    table.n = len(table.records)
    table.mu = Mean(table.lengths)
    mv = thinkstats.MeanVar(table.lengths)
    table.sd = math.sqrt(mv[1])

def MakeTables(data_dir='.'):
    '''根据目录，读取数据，返回处理好的数据表元组
    '''
    table = survey.Pregnancies() #创建 Pregnancies 这个类的实例
    table.ReadRecords(data_dir) #读取数据
    print(len(table.records), '条怀孕记录')
    outcomeLive(table)

    # 把总表分成两个表：第一胎、其他
    firsts, others = PartitionRecords(table)

    return table, firsts, others

def ProcessTables(*tables):
    ''' 处理数据表的所有记录
    参数：处理好的数据元组，可接受多个参数
    '''
    for table in tables: #遍历多个参数
        Process(table) #处理每个参数

def Summarize(data_dir):
    '''输出第一个婴儿的统计结果。
    返回数据表的元组
    '''
    table, firsts, others = MakeTables(data_dir)
    ProcessTables(firsts, others)

    print('第一个婴儿的数量：', firsts.n)
    print('其他婴儿的数量：', others.n)

    mu1, mu2 = firsts.mu, others.mu
    print('平均妊娠期（周）：')
    print('第一胎：', mu1)
    print('其他：', mu2)
    print('妊娠期差异(天)：', (mu1 - mu2) / 7.0)

    sd1, sd2 = firsts.sd, others.sd
    print('妊娠期的标准差：')
    print('第一胎：', sd1)
    print('其他：', sd2)

    plotHist(firsts)
    plotHist(others)
    pyplot.show()

def plotHist(table):
    ''' 绘制直方图
    :param firsts:
    :param others:
    :return:
    '''
    hist = Pmf.MakeHistFromList(table.lengths)
    vals, freqs = hist.Render()
    rect = pyplot.bar(vals, freqs)


def main(name, data_dir='.'):
    Summarize(data_dir)

# 上面都是函数，下面才是执行
if __name__ == '__main__': # 只有当前文件时，才执行，被引用时，不执行
    import sys
    main(*sys.argv, '../data/')
