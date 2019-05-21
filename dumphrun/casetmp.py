#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
生成httprunner测试用例模版
"""

import json

#
# get_tmp = \
# [
#     {
#         "config": {
#             "name": "testcase description",
#             "variables": {}
#         }
#     },
#     {
#         "test": {
#             "name": "casname",
#             "request": {
#                 "url": "",
#                 "method": "GET",
#                 "headers": {
#                 },
#             },
#             "validate": [
#                 {"eq": ["status_code", 200]}
#             ]
#         }
#     }
# ]
#
#
#
# post_tmp = \
# [
#     {
#         "config": {
#             "name": "testcase description",
#             "variables": {}
#         }
#     },
#     {
#         "test": {
#             "name": "casname",
#             "request": {
#                 "url": "",
#                 "method": "POST",
#                 "headers": {
#                 },
#                 "json": {
#                 }
#             },
#             "validate": [
#                 {"eq": ["status_code", 200]}
#             ]
#         }
#     }
# ]
#
#
#
#
# get_tmp = \
# [
#     {
#         "config": {
#             "name": "testcase description",
#             "variables": {}
#         }
#     },
#     {
#         "test": {
#             "name": "casname",
#             "request": {
#                 "url": "",
#                 "method": "GET",
#                 "headers": {
#                 },
#             },
#             "validate": [
#                 {"eq": ["status_code", 200]}
#             ]
#         }
#     }
# ]


test_case_tmp = [{
        "config": {
            "name": "testcase description",
            "variables": {}
        }
    }
    ]




post_tmp = \
    {
        "test": {
            "name": "casname",
            "request": {
                "url": "",
                "method": "POST",
                "headers": {
                },
                "json": {
                }
            },
            "validate": [
                {"eq": ["status_code", 200]}
            ]
        }
    }

get_tmp =  \
    {
        "test": {
            "name": "casname",
            "request": {
                "url": "",
                "method": "GET",
                "headers": {
                },
            },
            "validate": [
                {"eq": ["status_code", 200]}
            ]
        }
    }



# get_tmp[1]['test']['request']['headers'] = headers
# get_tmp[1]['test']['request']['url'] = url


# print(json.dumps(get_tmp,indent=4))
#
# with open('hrun_case.json','w') as f_w:
#     f_w.write(json.dumps(get_tmp,indent=4))