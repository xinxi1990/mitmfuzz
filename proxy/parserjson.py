#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
解析json数据
"""

from __future__ import print_function
from mathrandom import MathRandom
from jsonpath_rw import jsonpath, parse
import json,re
import logger
logger.setup_logger('DEBUG')

JSON_DATA_VARNAME = 'json_data'  # 存在json数据的变量名称
data_struct_list = []  # 用于存放所有 json 元素路径，形如 json_data[0]["data"][0]["components"][0]["enabled"]
data_struct_link = 'json_data'  # 用于临时存放单条json 元素路径(的一部分)

def modify_deep_dict(new_value, json_path, json_dict):
    if "." in json_path:
        json_path_list = []
        for path in str(json_path).split("."):
            if "[" and "]" in path:
                value_1 = path.split('[')[0]
                value_2 = path.split('[')[1].replace(']', '')
                json_path_list.append(value_1)
                json_path_list.append(int(value_2))
            else:
                json_path_list.append(path)
        for path_str in json_path_list:
            get_dict(path_str, json_dict)
    else:
        json_dict[json_path] = new_value
        dict(json_dict).update()
    return json_dict


def get_dict_value(new_value, json_path_list, json_dict):
    for path_str in json_path_list:
        if type(json_dict) == dict or type(json_dict) == list:
            new_dict = json_dict[path_str]
            print(new_dict)
            if type(new_dict) == dict or type(new_dict) == list:
                json_path_list.remove(path_str)
                print("current list size:{}".format(json_path_list.__len__()))
                print("current list :{}".format(json_path_list))
                if json_path_list.__len__() > 0:
                    get_dict_value(new_value, json_path_list, new_dict)
                else:
                    break
        else:
            print(json_dict)
            json_dict = new_value
            dict(json_dict).update()
            break


def dict_generator(indict, pre=None):
    '''
    递归生成所有的jsonpath路径
    :param indict:
    :param pre:
    :return:
    '''
    pre = pre[:] if pre else []
    if isinstance(indict, dict):
        for key, value in indict.items():
            if isinstance(value, dict):
                if len(value) == 0:
                    yield pre + [key, '{}']
                else:
                    for d in dict_generator(value, pre + [key]):
                        yield d
            elif isinstance(value, list):
                if len(value) == 0:
                    yield pre + [key, '[]']
                else:
                    for index,v in enumerate(value):
                        for d in dict_generator(v, pre + [key + "[{}]".format(index)]):
                            yield d
            elif isinstance(value, tuple):
                if len(value) == 0:
                    yield pre + [key, '()']
                else:
                    for v in value:
                        for d in dict_generator(v, pre + [key]):
                            yield d
            else:
                yield pre + [key, value]
    else:
        yield indict



def get_jsonpath_list(sJOSN):
    '''
    生成递归jsonpath列表
    :return:
    '''
    jsonpath_list = []
    sValue = json.dumps(sJOSN)
    for i in dict_generator(sJOSN):
        get_json_path = '.'.join(i[0:-1])
        json_path_value = i[-1]
        logger.log_debug("get json path is:{}".format(get_json_path))
        logger.log_debug("get json path value:{}".format(json_path_value))
        jsonpath_list.append(get_json_path)
    return jsonpath_list




def parse_sub_expr(sub_expr):
    '''
    解析字表达式-元素路径的组成部分
    :param sub_expr:
    :return:
    '''
    RIGHT_INDEX_DEFAULT = '200000000' # 右侧索引的默认值 未指定右侧索引时使用，形如 key[2:]、key[:]
    result = re.findall('\[.+\]', sub_expr)
    if result: # 如果子表达式为数组，形如 [1]、key[1]、 key[1:2]、 key[2:]、 key[:3]、key[:]
        array_part = result[0]
        array_part = array_part.lstrip('[').rstrip(']')
        key_part = sub_expr[:sub_expr.index('[')]
        if key_part == '$':  # 如果key为 $ ，为根，替换为数据变量 json_data
            key_part = JSON_DATA_VARNAME
        elif key_part == '*':
            key_part == '\[.+\]' # 如果key为 * ，替换为 \[\.+\] 以便匹配 ["key1"]、["key2"]、……
        else:
            key_part = '\["%s"\]' % key_part
        if array_part == '*': # 如果数组索引为 * ，替换为 \[\d+\] 以便匹配 [0]、[1]、……
            array_part = '\[\d+\]'
        else:
            array_part_list = array_part.replace(' ', '').split(':')
            left_index = array_part_list[0:1]
            right_index = array_part_list[1:]
            if left_index:
                left_index = left_index[0]
                if not (left_index or left_index.isdigit()): # 为空字符串、非数字
                    left_index = '0'
            else:
                left_index = '0'
            if right_index:
                right_index = right_index[0]
                if not (right_index or right_index.isdigit()):
                    right_index = RIGHT_INDEX_DEFAULT # 一个比较大的值，
                array_part = left_index + '-' + right_index
            else:
                array_part = left_index
            array_part = '\[[%s]\]' % array_part  # 数组索引设置为 \[[n-m]\],以便匹配[n],[n+1], ……，[m-1]
        return key_part + array_part
    elif sub_expr == '*':
        sub_expr = '\[.+\]'
    elif sub_expr == '$':
        sub_expr = JSON_DATA_VARNAME
    else:
        sub_expr = '\["%s"\]' % sub_expr
    return sub_expr




def parse_json(json_data, data_struct_link):
    '''
    递归解析json数据结构，存储元素的路径
    :param json_data:
    :param data_struct_link:
    :return:
    '''
    if type(json_data) == type({}): # 字典类型
        keys_list = json_data.keys()
        for key in keys_list:
            temp_data_struct_link =  data_struct_link + '["%s"]' % key
            if type(json_data[key]) not in [type({}), type([])]: # key对应的value值既不是数组，也不是字典
                data_struct_list.append(temp_data_struct_link)
            else:
                parse_json(json_data[key], temp_data_struct_link)
    elif type(json_data) == type([]): # 数组类型
        array_length = len(json_data)
        for index in range(0, array_length):
            temp_json_data = json_data[index]
            keys_list = temp_json_data.keys()
            for key in keys_list:
                temp_data_struct_link =  data_struct_link + '[%s]["%s"]' % (str(index), key)
                if type(temp_json_data[key]) not in [type({}), type([])]: # key对应的value值既不是数组，也不是字典
                    data_struct_list.append(temp_data_struct_link)
                else:
                    parse_json(temp_json_data[key], temp_data_struct_link)



def edit_dict(expr,new_value,json_data):
    '''
    修改更改键的值
    :return:
    '''
    expr_path = expr.split(".")
    edit_key = expr_path[-1]
    expr = expr.replace("." + edit_key,'')
    # 解析表达式为正则表达式
    parse_json(json_data, data_struct_link)
    re_pattern = ''

    for sub_expr in expr.split('.'):
        re_pattern += parse_sub_expr(sub_expr)
    logger.log_debug('\n元素路径jsonpath表达式为：%s' % expr)
    logger.log_debug('元素路径正则表达式re pattern为：%s' % re_pattern)
    logger.log_debug('\njsonpath 匹配结果如下：')
    re_pattern = re.compile(re_pattern)
    target_set = set()  # 匹配结果会有重复值，所以采用集合
    for item in data_struct_list:
        results = re.findall(re_pattern, item)
        for result in results:
            target = item[0:item.index(result) + len(result)]
            target_set.add(target)

    # 通过匹配提取的目标结果，操作json串
    for item in target_set:
        target = eval(item)
        if type(target) == type({}):  # 如果为字典
            # 更改键的值
            logger.log_debug("更改键:" + edit_key)
            target[edit_key] = new_value
        elif type(target) == type([]):
            # 暂不实现
            pass
    logger.log_debug('重新生成的新json数据:\n{}'.format(json_data))
    return json_data



def del_dict(expr,json_data):
    '''
    删除键的值
    :return:
    '''
    expr_path = expr.split(".")
    del_key = expr_path[-1]
    expr = expr.replace("." + del_key,'')
    # 解析表达式为正则表达式
    parse_json(json_data, data_struct_link)
    re_pattern = ''
    for sub_expr in expr.split('.'):
        re_pattern += parse_sub_expr(sub_expr)
    logger.log_debug('\n元素路径jsonpath表达式为：%s' % expr)
    logger.log_debug('元素路径正则表达式re pattern为：%s' % re_pattern)
    logger.log_debug('\njsonpath 匹配结果如下：')
    re_pattern = re.compile(re_pattern)
    target_set = set()  # 匹配结果会有重复值，所以采用集合
    for item in data_struct_list:
        results = re.findall(re_pattern, item)
        for result in results:
            target = item[0:item.index(result) + len(result)]
            target_set.add(target)
    # 通过匹配提取的目标结果，操作json串
    for item in target_set:
        target = eval(item)
        if type(target) == type({}):  # 如果为字典
           logger.log_debug("删除键:" + del_key)
           del target[del_key]
        elif type(target) == type([]):
            # 暂不实现
            pass
    logger.log_debug('重新生成的新json数据:\n{}'.format(json_data))
    return json_data




def drop_list(expr,json_data):
    '''
    改成空列表
    :return:
    '''
    # 解析表达式为正则表达式
    expr_path = expr.split(".")
    del_key = expr_path[-1]
    expr = expr.replace("." + del_key, '')
    parse_json(json_data, data_struct_link)
    re_pattern = ''
    for sub_expr in expr.split('.'):
        re_pattern += parse_sub_expr(sub_expr)
    logger.log_debug('\n元素路径jsonpath表达式为：%s' % expr)
    logger.log_debug('元素路径正则表达式re pattern为：%s' % re_pattern)
    logger.log_debug('\njsonpath 匹配结果如下：')
    re_pattern = re.compile(re_pattern)
    target_set = set()  # 匹配结果会有重复值，所以采用集合
    for item in data_struct_list:
        results = re.findall(re_pattern, item)
        for result in results:
            target = item[0:item.index(result) + len(result)]
            target_set.add(target)
    # 通过匹配提取的目标结果，操作json串
    for item in target_set:
        target = eval(item)
        print(target)
        if type(target) == type({}):  # 如果为字典
            if '[*]' in del_key:
                target[del_key.replace('[*]','')] = []
            else:
                target[del_key] = []
        elif type(target) == type([]):
            # 暂不实现
            pass
    logger.log_debug('重新生成的新json数据:\n{}'.format(json_data))
    return json_data





if __name__ == "__main__":
    json_data =  {
                "base_config":{
                    "enforce":{
                        "value":"0",
                        "inherit":"0",
                        "global":"0"
                    },
                    "modify":{
                        "value":"0",
                        "inherit":"0",
                        "global":"0"
                    }
                },
                "safe_control_list":{
                    "list":[
                        {
                            "gid":"0",
                            "gname":"全网计算机",
                            "isactive":"1",
                            "rule_id":"0",
                            "rule_name":"请选择规则",
                            "time_range":"所有时间",
                            "time_range_id":"1",
                            "policy_tpl":"33",
                            "policy_tpl_id":"17",
                            "isonline":"3",
                            "priority":"88888"
                        },
                        {
                            "gid": "1",
                            "gname": "全网计算机",
                            "isactive": "1",
                            "rule_id": "0",
                            "rule_name": "请选择规则",
                            "time_range": "所有时间",
                            "time_range_id": "1",
                            "policy_tpl": "33",
                            "policy_tpl_id": "17",
                            "isonline": "3",
                            "priority": "99999"
                        }
                    ]
                }
    }
    #       drop         }                                                  _list(expr=expr, json_data=self.rep_json)
    #                ]
    #            }
    #
    # expr = 'safe_control_list.list[*]'
    # new_data = drop_list(expr=expr,json_data=json_data)
    #
    # print(new_data)




    # del_dict(expr=expr,json_data=json_data)

    # for index in range(1):
    #     json_path_list = get_jsonpath_list(json_data)
    #     expr = (MathRandom().get_random_list(json_path_list))
    #     print(expr)
    #     print(edit_dict(expr=expr,new_value="555555555555",json_data=json_data))















