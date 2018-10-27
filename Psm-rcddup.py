#!/usr/bin/env python3
# -*- coding=utf-8 -*-

# @Time    : 2018-10-18
# @Author  : J.sky
# @Mail    : bosichong@qq.com
# @Site    : www.17python.com
# @Title   : Python实现小学生加减乘除速算考试题卷。
# @Url     : http://www.17python.com/blog/29
# @Details : Python实现小学生加减乘除速算考试题卷。
# @Other   : OS X 10.11.6
#            Python 3.6.1
#            PyCharm
###################################
# 用Python自动生成小学生加减乘除口算考试题卷。
###################################


'''
孩子上小学一年级了，加减乘除的口算就要开始练习了，估计老题肯定会让家长出题，所以提前准备一下，利用Python开发了一套自动生成小学生口算题的小应用。而且今天是程序员节，撸200行代码庆祝一下。：）
程序核心功能：1.根据条件生成相关的口算题，2.保存为排版好的网页用来打印。

其实一开始以为很简单的一个小应用了，结果发现编写起来好多的条件需要判断，不过这也算是一份不错的python复习案例了，几乎把一些常用的python语法都用到了。
目前只实现了单步加减法口算题的生成，配置项实现了口算题的数值范围取向，比如0-20之间的加减法，还可以过滤不需要的数字，判断加法进位减法退位，以及一些配置上错误时的判断：
比如设置0-5范围内，要生成进位加法20道，这是不可能实现的。
比如有意思的是加减法进退位的判断，程序中我写了一个简单方法。
开始以为单步和多步计算可以使同一方法，现在看来还得需要分开来写，如果要硬挤到一起方法就会太复杂了，不易梳理。
后续会把功能上分成 单步 二步 三步（加减乘除）法，乘除法相对来说简单些，除法要判断是否有余，有求余数口算？
而且原以为打印这个功能很简单的，其实如果做起来排版也是挺麻烦的，后继会慢慢更新程序并制作出适合的排版方式。
'''

import random

class Generator(object):
    '''
    - @sigunm   int     
        运算符 (1: 加, 2: 减, 3: 乘, 4: 除)
    - @range    tuple
        随机范围, 默认: (0, 10)
    - @need_carry    int
        进位, 退位运算(1: 随机, 2: 进位, 3: 退位), 默认: 1
    - @step int
        生成几步运算, 默认: 1
    - @filter tuple
        需要过滤的值
    - @same boolean
        是否相同
    '''

    signum = None
    range = None
    need_carry = None
    step = None
    filter = None
    same = None

    def __init__(self, signum=None, range=(0, 10), need_carry=1, step=1, filter=(0, 10), same=True):
        self.__init(signum, range, need_carry, step, filter)
    
    def __init(self, signum=None, range=(0, 10), need_carry=1, step=1, filter=None):
        '''初始化参数配置'''
        if signum is None:
            raise Exception("required param signum is missing or signum is None")
        if signum not in (1,2,3,4):
            raise Exception("param signum must be 1 or 2 or 3 or 4")
        if range is None:
            raise Exception("required param range is missing or range is None")

        if signum == 1:
            self.signum = "+"
        elif signum == 2:
            self.signum = "-"
        elif signum == 3:
            self.signum = "×"
        elif signum == 4:
            self.signum = "÷"

        self.range = range
        self.need_carry = need_carry
        self.step = step
        self.filter = filter
        
        self.min = min(range)
        self.max = max(range)
        self.__data_list = []
    
    def __is_valid(self, data):
        pass
        
    def __get_num(self, number):
        '''反回一个整数的个位数'''
        value0 = number / 10
        value0 = int(value0)
        return number - value0 * 10

    def __is_carry(self, a, b):
        '''判断加法是否存在进位'''
        if (self.__get_num(a) + self.__get_num(b) < 10):
            return False
        else:
            return True

    def __get_topic(self, a, b):
        '''根据两个数字返回一道单步口算加法题'''
        # 判断两个随机生成的数字不能相同， 不能为过滤列表中的数字，如果条件符合，即可生成算式

        if a != b and not (a in self.filter) and not (b in self.filter):
            if (self.need_carry == 1):  # 随机的不论是否进位
                return "{}{}{}=".format(a, self.signum, b)
            elif (self.need_carry == 2):  # 如果需要进位
                if (self.__is_carry(a, b)):  # 判断是必须为进位
                    return "{}{}{}=".format(a, self.signum, b)
            elif (self.need_carry == 3):  # 如果需要不进位subtractlist['abdication']
                if (not self.__is_carry(a, b)):  # 判断是必须为不进位
                    return "{}{}{}=".format(a, self.signum, b)
        else:
            return False

    def __generate_data(self, number):
        '''根据条件生成所需数据列表'''
        # 循环生成所有加法口算题
        for i in range(self.min, self.max):
            for j in range(self.min, self.max):
                addt = self.__get_topic(i, j)
                if addt:
                    self.__data_list.append(addt)
        if (len(self.__data_list) >= number):
            random.shuffle(self.__data_list)  # 洗牌，先打乱list中的排序
            self.__data_list = random.sample(self.__data_list, number)  # 随机取需要的口算题量。
        elif(len(self.__data_list) == 0):
            raise Exception('此数字范围内生成的加法口算题未能达到您要求的数目，请检查配置以适合程序的生成，请修改数值符合加法进位')
        else:
            if self.same:
                for i in range(number - len(self.__data_list)):
                    k = random.randint(0, len(self.__data_list) - 1)
                    self.__data_list.append(self.__data_list[k])
            else:
                raise Exception('此数字范围内生成的加法口算题未能达到您要求的数目，请检查配置以适合程序的生成，比如设置可以生成相同的题')

    def produce(self, number):
        self.__generate_data(number)
        print(self.__data_list)


def main():
    g = Generator(signum=1, range=(0, 20), need_carry=2, step=1, filter=(0, 10), same=True)
    g.produce(20)


if __name__ == '__main__':
    main()  # 程序入口
