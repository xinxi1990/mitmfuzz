#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
批量生成httprunner
"""

import json
import urllib.parse
from casetmp import *

class CaseFactory():


    @staticmethod
    def gen_case(file_path):
        '''
        组装数据
        :return:
        '''
        records = []
        with open(file_path) as f_r:
            for line in f_r.readlines():
                item = line.split('|')
                url = item[0]
                method = item[1]
                header = CaseFactory.gen_header(item[2])[0]
                content_type = CaseFactory.gen_header(item[2])[1]
                data = CaseFactory.gen_data(item[3])
                if method == "GET":
                    # print(url)
                    # print(method)
                    # print(header)
                    # print(content_type)
                    # print(data)
                    get_tmp['test']['request']['url'] = url
                    get_tmp['test']['request']['headers'] = header
                    test_case_tmp.append(get_tmp)
                elif method == "POST":
                    post_tmp['test']['request']['url'] = url
                    post_tmp['test']['request']['headers'] = header
                    post_tmp['test']['request']['json'] = data
                    test_case_tmp.append(post_tmp)

        with open('hrun_case.json', 'w') as f_w:
            f_w.write(json.dumps(test_case_tmp, indent=4))



    # @staticmethod
    # def gen_header(headers):
    #     content_type = ""
    #     itmes = str((headers.replace('Headers[','')).replace(']','')).split(',')
    #     key_list = []
    #     value_list = []
    #     for item in itmes[::2]:
    #         # print(item)
    #         key_list.append(item.replace("('","").replace(")'","").replace("(b","").replace("'","").replace("'","").strip())
    #     for item in itmes[1::2]:
    #         # print(item)
    #         value_list.append(item.replace("('","").replace(")'","").replace("(b","").replace("'","").strip())
    #     dictionary = dict(zip(key_list, value_list))
    #     if ('Content-Type' in dictionary):
    #         content_type = (dictionary["Content-Type"])
    #     return dictionary,content_type

    # @staticmethod
    # def gen_data(data):
    #     print(data)
    #     s_data = urllib.parse.unquote(data).replace("b'", '').replace("'", '').replace("\n", "")
    #     key_list = []
    #     value_list = []
    #     for s in s_data.split("&"):
    #         if "=" in s:
    #             key_list.append(s.split("=")[0])
    #             value_list.append(s.split("=")[1])
    #     dictionary = dict(zip(key_list, value_list))
    #     return dictionary


    @staticmethod
    def gen_header(headers):
        content_type = ""
        dictionary = eval(headers)
        if ('Content-Type' in dictionary):
            content_type = (dictionary["Content-Type"])
        return dictionary, content_type


    @staticmethod
    def gen_data(data):
        dictionary = {}
        try:
            dictionary = eval(data)
        except Exception as e:
            print(e)
        return dictionary



if __name__ == '__main__':
    print("==================== start gen ====================")
    CaseFactory.gen_case('20190521234042_intercept.log')
    print("==================== end gen ====================")