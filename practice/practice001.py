__author__ = 'Skye 2017-11-20'
# coding=utf-8
import survey
table = survey.Pregnancies()
table.ReadRecords('../data/')
print(len(table.records), '条怀孕记录')


