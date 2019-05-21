# -*- encoding:utf-8 -*-


# author:授客


import re


def parse_sub_expr(sub_expr):
    '''

    解析字表达式-元素路径的组成部分

    :param sub_expr:

    :return:

    '''

    RIGHT_INDEX_DEFAULT = '200000000'  # 右侧索引的默认值 未指定右侧索引时使用，形如 key[2:]、key[:]

    result = re.findall('\[.+\]', sub_expr)

    if result:  # 如果子表达式为数组，形如 [1]、key[1]、 key[1:2]、 key[2:]、 key[:3]、key[:]

        array_part = result[0]

        array_part = array_part.lstrip('[').rstrip(']')

        key_part = sub_expr[:sub_expr.index('[')]

        if key_part == '$':  # 如果key为 $ ，为根，替换为数据变量 json_data

            key_part = JSON_DATA_VARNAME

        elif key_part == '*':

            key_part == '\[.+\]'  # 如果key为 * ，替换为 \[\.+\] 以便匹配 ["key1"]、["key2"]、……

        else:

            key_part = '\["%s"\]' % key_part

        if array_part == '*':  # 如果数组索引为 * ，替换为 \[\d+\] 以便匹配 [0]、[1]、……

            array_part = '\[\d+\]'

        else:

            array_part_list = array_part.replace(' ', '').split(':')

            left_index = array_part_list[0:1]

            right_index = array_part_list[1:]

            if left_index:

                left_index = left_index[0]

                if not (left_index or left_index.isdigit()):  # 为空字符串、非数字

                    left_index = '0'

            else:

                left_index = '0'

            if right_index:

                right_index = right_index[0]

                if not (right_index or right_index.isdigit()):
                    right_index = RIGHT_INDEX_DEFAULT  # 一个比较大的值，

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

    if type(json_data) == type({}):  # 字典类型

        keys_list = json_data.keys()

        for key in keys_list:

            temp_data_struct_link = data_struct_link + '["%s"]' % key

            if type(json_data[key]) not in [type({}), type([])]:  # key对应的value值既不是数组，也不是字典

                data_struct_list.append(temp_data_struct_link)

            else:

                parse_json(json_data[key], temp_data_struct_link)

    elif type(json_data) == type([]):  # 数组类型

        array_length = len(json_data)

        for index in range(0, array_length):

            temp_json_data = json_data[index]

            keys_list = temp_json_data.keys()

            for key in keys_list:

                temp_data_struct_link = data_struct_link + '[%s]["%s"]' % (str(index), key)

                if type(temp_json_data[key]) not in [type({}), type([])]:  # key对应的value值既不是数组，也不是字典

                    data_struct_list.append(temp_data_struct_link)

                else:

                    parse_json(temp_json_data[key], temp_data_struct_link)


if __name__ == '__main__':

    json_data = [{"data": [{

        "admin": "string|集群负责人|||",

        "components": [

            {

                "clusterId": "integer|组件所属的集群 id|||",

                "createTime": "string|组件创建时间|||",

                "description": "string|组件描述|||",

                "enabled": "boolean|组件是否开启||false|",

            },

            {

                "clusterId": "integer|组件所属的集群 id|||",

                "createTime": "string|组件创建时间|||",

                "description": "string|组件描述|||",

                "enabled": "boolean|组件是否开启||false|",

            }

        ],

        "createTime": "string|集群创建时间|||",

        "description": "string|集群描述|||",

        "enabled": "boolean|集群是否开启||false|",

        "id": "integer|集群 id|||",

        "modifyTime": "string|集群修改时间|||",

        "name": "string|集群名|||"

    }],

        "errMsg": "string||||",

        "ok": "boolean||||",

        "status": "integer||||"

    }]

    JSON_DATA_VARNAME = 'json_data'  # 存在json数据的变量名称

    data_struct_list = []  # 用于存放所有 json 元素路径，形如 json_data[0]["data"][0]["components"][0]["enabled"]

    data_struct_link = 'json_data'  # 用于临时存放单条json 元素路径(的一部分)

    parse_json(json_data, data_struct_link)

    print('获取的json元素路径,元素值如下：')

    for item in data_struct_list:
        print(item, '\t', eval(item))

    # 测试用表达式

    # expr = '$.data[*].components[0]' # json数据为字典 形如 {……}

    # expr = '$[*].data[0:1].components[*]'  # json数据为数组 形如 [{……}]

    expr = 'data[0:1].components[*]'

    # expr = 'data[0:1].components'

    # 解析表达式为正则表达式

    re_pattern = ''

    for sub_expr in expr.split('.'):
        re_pattern += parse_sub_expr(sub_expr)

    print('\n元素路径jsonpath表达式为：%s' % expr)

    print('元素路径正则表达式re pattern为：%s' % re_pattern)

    print('\njsonpath 匹配结果如下：')

    re_pattern = re.compile(re_pattern)

    target_set = set()  # 匹配结果会有重复值，所以采用集合

    for item in data_struct_list:

        results = re.findall(re_pattern, item)

        for result in results:
            print('匹配的元素路径jsonpath为：%s' % item)

            print('正则匹配结果为：%s' % result)

            target = item[0:item.index(result) + len(result)]

            print('供提取数据使用的jsonpath为：%s' % target)

            print('提取的结果值为：%s \n' % eval(target))

            target_set.add(target)

    # 通过匹配提取的目标结果，操作json串

    for item in target_set:
        print("target item:" + item)
        target = eval(item)
        print("target value:{}".format(target))
        print("target type:{}".format(type(target)))

        if type(target) == type({}):  # 如果为字典

            # 更改键的值
            print("更改键的值")
            target['clusterId'] = 10

            # 新增键值对

            target['new_key'] = 'key_value'

            # 更改键的名称，可以考虑先复制旧的键值，赋值给新的键，然后删除旧的键

            target['description_new'] = target['description']

            # 删除键值对

            del target['description']



        elif type(target) == type([]):

            # 暂不实现

            pass

    print(json_data)