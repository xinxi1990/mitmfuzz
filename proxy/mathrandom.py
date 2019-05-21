#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
随机数类
"""
import random


""" generated source for module MathRandomBACK """
class MathRandom(object):
    """ generated source for class MathRandomBACK """
    NOT_REPLACE = 0.35
    REPLACE_RESPONSE_JSON = 0.25
    REPLACE_RESPONSE_STR = 0.1
    REPLACE_RESPONSE_LIST = 0.05
    DELAY_RESPONES_TIME = 0.30
    REPLACE_STATUS_CODE = 0.04

    def PercentageRandom(self):
        """ generated source for method PercentageRandom """
        randomNumber = float()
        randomNumber = random.random()
        if randomNumber >= 0 and randomNumber <= self.NOT_REPLACE:
            return 0
        elif randomNumber >= self.NOT_REPLACE / 100 and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON:
            return 1
        elif randomNumber >= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR:
            return 2
        elif randomNumber >= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST:
            return 3
        elif randomNumber >= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST + self.DELAY_RESPONES_TIME:
            return 4
        elif randomNumber >= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST + self.DELAY_RESPONES_TIME and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST + self.DELAY_RESPONES_TIME + self.REPLACE_STATUS_CODE:
            return 5
        elif randomNumber >= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST + self.DELAY_RESPONES_TIME + self.REPLACE_STATUS_CODE and randomNumber <= self.NOT_REPLACE + self.REPLACE_RESPONSE_JSON + self.REPLACE_RESPONSE_STR + self.REPLACE_RESPONSE_LIST + self.DELAY_RESPONES_TIME + self.REPLACE_STATUS_CODE:
            return 6
        return -1

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        from collections import Counter
        a_list = []
        for line in range(100):
            a_list.append(MathRandom().PercentageRandom())
        result = Counter(a_list)
        print(result)



    def get_random_list(self,list):
        '''
        列表中随机返回一个
        :param list:
        :return:
        '''
        return random.choice(list)




if __name__ == '__main__':
    import sys
    MathRandom.main(sys.argv)


