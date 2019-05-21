#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy的rule的规则
@author:xinxi
"""

import json,time
from mathrandom import MathRandom
from parserjson import *
import random
import logger
logger.setup_logger('INFO')

class ProxyRule():

    def __init__(self,rep_json):
        self.rep_json = eval(rep_json)



    def get_defult_data(self):
        return  '{"h":{"c":0,"e":"","t":0.004232388,"s":1558015779},"c":{"data":{"status":1,"online_num":0,"reservation_num":0,"title":"直播测试22222","room_id":205,"intro":"test","starttime":1554972060,"starttime_desc":"周四16:41","duration":110,"endtime":1554978660,"id":205,"type":0,"log_id":205,"log_type":"igettv"}}}'


    def get_edit_str(self):
        '''
        修改后的字典
        :return:
        '''
        json_path_list = get_jsonpath_list(self.rep_json)
        logger.log_debug("{}".format(json_path_list))
        expr = MathRandom().get_random_list(json_path_list)
        logger.log_debug("{}".format(expr))
        new_json_data = edit_dict(expr=expr, new_value=self.get_random_string(), json_data=self.rep_json)
        logger.log_debug("{}".format(new_json_data))
        return json.dumps(new_json_data)


    def get_del_str(self):
        '''
        删除后的字典
        :return:
        '''
        json_path_list = get_jsonpath_list(self.rep_json)
        logger.log_debug("{}".format(json_path_list))
        expr = MathRandom().get_random_list(json_path_list)
        logger.log_debug("{}".format(expr))
        new_json_data = del_dict(expr=expr, json_data=self.rep_json)
        logger.log_debug("{}".format(new_json_data))
        return json.dumps(new_json_data)



    def not_intercept(self):
        '''
        不篡改响应,直接返回结果
        :return:
        '''
        logger.log_info("not_intercept")
        return json.dumps(self.rep_json)


    def intercept_respones_json(self):
        '''
        对返回的json数据做随机做增删操作
        :return:
        '''
        logger.log_info("intercept_respones_json")
        return json.dumps(self.rep_json)



    def intercept_respones_str(self):
        '''
        对返回结果中的某个字段所增删改操作
        :return:
        '''
        logger.log_info("intercept_respones_str")
        event_list = [self.get_edit_str(), self.get_del_str()]
        event = MathRandom().get_random_list(event_list)
        return event


    def intercept_respones_list(self):
        '''
        多返回结果中的数组做增删改操作
        :return:
        '''
        path_list = []
        logger.log_debug("replace_respones_list")
        json_path_list = get_jsonpath_list(self.rep_json)
        logger.log_debug("{}".format(json_path_list))
        for line in json_path_list:
            if "[" and  "]"  in str(line):
                #logger.log_info("intercept line is:{}".format(line))
                path_list.append(line)
        if path_list.__len__() != 0:
           expr = MathRandom().get_random_list(path_list)
           expr = str(expr).split('[')[0]
           logger.log_debug("{}".format(expr))
           new_json_data = drop_list(expr=expr, json_data=self.rep_json)
           logger.log_debug("{}".format(new_json_data))
           return json.dumps(new_json_data)
        else:
            return json.dumps(self.rep_json)





    def delay_respones_time(self):
        '''
        对返回数据做延迟返回
        :return:
        '''
        random_time = random.randint(100,1000)
        time.sleep(random_time/1000)
        logger.log_info("delay_respones_time:{}ms".format(random_time))
        return json.dumps(self.rep_json)



    @staticmethod
    def intercept_status_code():
        '''
        对返回的状态码做随机修改
        :return:
        '''
        code_list = [404,500,503,302,301]
        random_code = MathRandom().get_random_list(code_list)
        logger.log_info("replace_status_code:{}".format(random_code))
        return random_code


    def get_random_string(self):
        '''
        获取随机字符串
        :return:
        '''
        string_list = ['','超长字符串' * 100, self.special_string()]
        string = MathRandom().get_random_list(string_list)
        return string


    def special_string(self):
        '''
        随机10位特殊字符
        :return:
        '''
        list = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)] + ['.','-','~','_']
        # 大写字母+小写字母+数字 +特殊字符.-_~
        num = random.sample(list, 10)
        str1 = ''
        value = str1.join(num)
        logger.log_info("special_string is:{}".format(value))
        return value



    def get_random_event(self):
        '''
        获取随机事件
        :param num:
        :return:
        '''
        num = MathRandom().PercentageRandom()
        for case in switch(num):
            if case(0):
                self.not_intercept()
                break
            if case(1):
                self.intercept_respones_json()
                break
            if case(2):
                self.intercept_respones_str()
                break
            if case(3):
                self.intercept_respones_list()
                break
            if case(4):
                self.delay_respones_time()
                break
            if case(4):
                self.intercept_status_code()
                break
            if case():
               self.not_intercept()



class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False


