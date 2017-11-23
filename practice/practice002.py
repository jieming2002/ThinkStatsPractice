__author__ = 'Skye 2017-11-20'
# coding=utf-8

""" 第 2 章：描述性统计量
汇总统计量：简单明了，但风险也大，因为它们很有可能会掩盖数据的真相。
    均值：值的总和除以值的数量
        均值（mean）和平均值（average）的区别：
        样本的“均值”是根据上述公式计算出来的一个汇总统计量；
        “平均值”是若干种可以用于描述样本的典型值的汇总统计量
    切尾均值（Trimmed Mean）：切掉数据大小两端的若干数值计算中间数据的均值
    方差：σ2 = Σi((xi - μ)**2) / n
        其中 μ 是均值， (xi - μ) 叫做离均差。因此方差为该偏差的方均值。
        方差的平方根 σ 叫做标准差。
        均值是为了描述集中趋势，而方差则是描述分散情况。方差越大越分散，方差越小越集中。
    中位数：代表一个样本、种群或概率分布中的一个数值，其可将数值集合划分为相等的上下两部分。
数据的分布：各个值出现的频繁程度
    频数：指的是数据集中一个值出现的次数。
    概率：就是频数除以样本数量 n 归一化 直方图 PMF=概率质量函数
    众数：一组数据中出现次数最多的数值。众数可能没有或有多个。
直方图：用于展示各个值出现的频数或概率。
    直方图可以非常直观地展现数据的：众数、形状、异常值。
    直方图中某些明显差异是由样本数量造成的。可以用 PMF 来解决这个问题。
PMF（Probability Mass Function，概率质量函数）：归一化之后的直方图
    把频数/n 转换成概率，这称为归一化。
"""
import thinkstats
import math
from practice import practice001
import Pmf
import operator
from matplotlib import pyplot
import myplot
import survey

def Process(table, name):
    '''  对数据表进行各种分析处理 '''
    practice001.Process(table)
    table.name = name

    # 计算方差：根据序列、均值
    table.var = thinkstats.Var(table.lengths, table.mu)
    # 计算切尾均值：根据序列
    table.trim = thinkstats.TrimmedMean(table.lengths)

    table.hist = Pmf.MakeHistFromList(table.lengths, name=name)
    table.pmf = Pmf.MakePmfFromList(table.lengths)

def PoolRecords(*tables):
    ''' 合并数据表 '''
    pool = survey.Pregnancies()
    for table in tables:
        pool.ExtendRecords(table.records)
    return pool

def MakeTables(data_dir):
    '''
    读取调查数据，返回一个数据表元组
    :param data_dir:
    :return:
    '''
    table, firsts, others = practice001.MakeTables(data_dir)
    pool = PoolRecords(firsts, others)

    Process(pool, '所有活婴')
    Process(firsts, '第一胎')
    Process(others, '其他胎')

    return pool, firsts, others

def Summarize(pool, firsts, others):
    ''' 输出各种汇总统计量 '''
    print('')
    print('方差')
    print('第一胎：', firsts.var)
    print('其他：', others.var)

    diff_mu = firsts.mu - others.mu
    print('均值的差异：', diff_mu)

    sigma = math.sqrt(pool.var)
    print('总的均值：', pool.mu)
    print('总的方差：', pool.var)
    print('总的标准差', sigma)

    print('第一胎均值：', firsts.mu)
    print('其他均值：', others.mu)

    print('切尾均值：')
    print('第一胎：', firsts.trim)
    print('其他：', others.trim)

    # 获取妊娠期序列
    live_lengths = pool.hist.GetDict().items()
    live_lengths = list(live_lengths)
    live_lengths.sort()
    print('最短长度：')
    for weeks, count in live_lengths[:9]: #只遍历前面 10 个元素
        print(weeks, count)

    print('最长长度：')
    for weeks, count in live_lengths[-9:]:  #只遍历最后 10 个元素
        print(weeks, count)

def MakeFigures(firsts, others):
    ''' 为妊娠期绘制直方图 和 PMF 图 '''
    # 字典列表，用于传递给绘图函数，设置颜色
    bar_options = [dict(color='0.9'), dict(color='blue')]

    # 绘制直方图：这个列表干嘛用的？定义绘图的坐标轴
    axis = [23, 46, 0, 2700]
    Hists([firsts.hist, others.hist])
    myplot.Save(root='nsfg_hist',
                title='Histogram',
                xlabel='weeks',
                ylabel='frequency',
                axis=axis)

    # 绘制 PMF 图
    axis = [23, 46, 0, 0.6]
    Hists([firsts.pmf, others.pmf])
    myplot.Save(root='nsfg_pmf',
                title='PMF',
                xlabel='weeks',
                ylabel='probability',
                axis=axis)

def Hists(hists):
    ''' 在同一个轴上绘制两个直方图：我看你怎么实现的 '''
    width = 0.4 #图的宽度，不是默认的 1
    shifts = [-width, 0.0] #图的偏移量
    option_list = [dict(color='0.9'), dict(color='blue')]

    pyplot.clf()
    for i, hist in enumerate(hists):
        xs, fs = hist.Render()
        xs = Shift(xs, shifts[i]) #关键在这里，让图偏移，错开
        # 参数：数值序列，频数序列，标签，柱状图宽度，柱状图颜色
        pyplot.bar(xs, fs, label=hist.name, width=width, **option_list[i])

def Shift(xs, shift):
    '''
    这个偏移是如何实现的？
    :param xs: 数值序列
    :param shift: 偏移量
    :return:数值序列
    '''
    return [x+shift for x in xs]

def MakeDiffFigure(firsts, others):
    '''
    绘制两个 PMF 的不同之处
    '''
    weeks = range(35, 46) # 只绘制这个范围的，我们关注这个范围
    diffs = []
    for week in weeks:
        p1 = firsts.pmf.Prob(week)
        p2 = others.pmf.Prob(week)
        diff = 100 * (p1 - p2) #计算两种概率的差异
        diffs.append(diff)

    # 要开始绘图了
    pyplot.clf()
    # 数值序列，概率差异序列，对其方式
    pyplot.bar(weeks, diffs, align='center')
    myplot.Save(root='nsfg_diffs',
                title='Difference in PMFs',
                xlabel='weeks',
                ylabel='100 (PMF$_{first}$ - PMF$_{other}$)',
                legend=False)

def MakePregnancyFigures(data_dir='../data/'):
    '''
    绘制调查数据直方图、PMF 图
    :return:
    '''
    pool, firsts, others = MakeTables(data_dir)
    Summarize(pool, firsts, others)
    MakeFigures(firsts, others)
    MakeDiffFigure(firsts, others)

def PmfVar(pmf):
    '''
    计算 pmf 的方差：不用再 / n
    :param pmf:
    :return:
    '''
    mu = PmfMean(pmf)
    return sum([prob * ((val - mu) ** 2) for val, prob in pmf.Items()])

def PmfMean(pmf):
    '''
    计算 pmf 的均值：不用再 / n
    :param pmf:
    :return:
    '''
    #一行代码，解决问题，哈哈哈~~~
    return sum([val*prob for val,prob in pmf.Items()])
    # pmfSum = 0
    # for val, prob in pmf.Items():
    #     pmfSum += val * prob
    # return pmfSum

def pmfMeanVar():
    pmf = Pmf.MakePmfFromList([1,2,2,3,5])
    mu = PmfMean(pmf)
    print('PmfMean() 均值 = ', mu)
    mu = pmf.Mean()
    print('Pmf 均值 = ', mu)

    sigma = PmfVar(pmf)
    print('PmfVar() 方差 = ', sigma)
    sigma = pmf.Var()
    print('Pmf 方差 = ', sigma)

def RemainingLifetime():
    '''
    参数是表示使用寿命的Pmf 对象和使用时间，返回一个表示剩余使用寿命分布的Pmf 对象。
    :return:
    '''
    pmf = Pmf.MakePmfFromList([720, 360, 450, 300, 600])
    used = 120

def testPmf():
    pmf = Pmf.MakePmfFromList([1,2,2,3,5])

    for val in pmf.Values():
        print(val, '的概率 = ', pmf.Prob(val))

    tt = pmf.Total()
    print('概率的总和 = ', tt)

    # 增加某个值的概率
    val = 2
    pmf.Incr(val, 0.2)
    prob = pmf.Prob(val)
    print(val, ' 的概率 = ', prob)

    tt = pmf.Total()
    print('概率的总和 = ', tt)

    # 将概率扩大若干倍
    val = 5
    pmf.Mult(val, 2)
    prob = pmf.Prob(val)
    print(val, ' 的概率 = ', prob)

    # 如果修改 Pmf，有可能导致整个 PMF 不再是归一化的，也就是说所有概率的总和不再等于 1
    tt = pmf.Total()
    print('概率的总和 = ', tt)

    # 要重新归一化，调用Normalize：
    pmf.Normalize()
    tt = pmf.Total()
    print('概率的总和 = ', tt)

    vals, freqs = pmf.Render()
    rect = pyplot.bar(vals, freqs)
    pyplot.show()

def pregnancyHist():
    ''' 怀孕周期直方图
    :return:
    '''
    practice001.main(__name__, '../data/')

def plotHist():
    ''' 绘制直方图
    :return:
    '''
    hist = Pmf.MakeHistFromList([3,3,4,4,1,1,2,3])
    vals, freqs = hist.Render()
    rect = pyplot.bar(vals, freqs)
    pyplot.show()

def plotPie():
    pyplot.pie([1,2,3])
    pyplot.show()

def AllModes():
    ''' 习题2 - 3
    按频数降序排列的值—频数对
    :return:
    '''
    hist = Pmf.MakeHistFromList([3,3,4,4,1,1,2,3])

    for val, freq in hist.Items():
        print(val, '的频数 = ', freq)

    operator.itemgetter(hist)

    for val, freq in hist.Items():
        print(val, '的频数 = ', freq)

def Mode():
    '''习题2 - 3
    众数
    :return:
    '''
    hist = Pmf.MakeHistFromList([3,3,4,4,1,1,2,3])
    m = 0
    f = 0

    for val, freq in hist.Items():
        if (freq > f):
            m = val
            f = freq
    print(m, '是众数，频数 = ', f)

def histPmf(): #直方图与概率质量函数
    hist = Pmf.MakeHistFromList([3,3,4,4,1,1,2,3])
    print('hist = ', hist)

    for val, freq in hist.Items():
        print(val, '的频数 = ', freq)

    for val in sorted(hist.Values()): #按序遍历这些值
        print(val, '的频数 = ', hist.Freq(val))

def pregnancy():
    '''习题2 - 2
    计算妊娠期的 标准差。
    :return:
    '''
    print('计算妊娠期的 标准差。')
    practice001.main(__name__, '../data/')

def Pumpkin():
    '''习题2 - 1
    计算南瓜重量的均值、方差和标准差。
    :return:
    '''
    tp = (1, 1, 1, 3, 3, 591)
    print('计算南瓜重量的均值、方差和标准差')
    mv = thinkstats.MeanVar(tp)
    print('均值 = ', mv[0])
    print('方差 = ', mv[1])
    σ = math.sqrt(mv[1])
    print('标准差 = ', σ)

def main():
    # Pumpkin()
    # pregnancy()
    # histPmf()
    # Mode()
    # AllModes()
    # plotPie()
    # plotHist()
    # pregnancyHist()
    # testPmf()
    # pmfMeanVar()
    MakePregnancyFigures()

if __name__ == '__main__':
    main()
