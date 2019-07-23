#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy代理工具篡改请求
"""

import mitmproxy.http
from mitmproxy import ctx
import json, time, os

from constant import split_joint
from proxyrule import ProxyRule
from mathrandom import MathRandom
from filetools import *

project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_intercept.log"
save_log_file = os.path.join(project_path, now)


def request(flow: mitmproxy.http.HTTPFlow):
    request = flow.request
    ctx.log.info("========================== intercept request start ==========================")
    ctx.log.info("========================== host is:{} ========================== ".format(request.host))
    ctx.log.info("========================== url is:{} ========================== ".format(request.pretty_url))
    ctx.log.info("========================== method is:{} ========================== ".format(request.method))
    ctx.log.info("========================== body is:{} ========================== ".format(request.get_text()))
    ctx.log.info("========================== intercept request end ==========================")


def response(flow: mitmproxy.http.HTTPFlow):
    '''
    篡改response返回数据
    :param flow:
    :return:
    '''
    is_mock = True

    black_list = ["png", "jpg", "js", "css", "html", 'img', 'cdn']

    for black_str in black_list:
        if black_str in flow.request.url:
            ctx.log.info("========================== not necessary intercept response ==========================")
            is_mock = False
            break

    if int(flow.response.status_code) == 200 and is_mock == True:

        original_data = (flow.response.text)

        if original_data.startswith("{") and original_data.endswith("}"):
            # get_mock_data = ProxyRule(original_data).get_random_event()
            get_mock_data = ProxyRule(original_data).intercept_respones_str()
            ctx.log.info("========================== intercept response start ==========================")
            # ctx.log.info("========================== mock after data:{} ==========================".format(original_data))
            # ctx.log.info("========================== mock before data:{} ==========================".format(get_mock_data))
            flow.response.set_text(get_mock_data)
            ctx.log.info(flow.response.text)
            ctx.log.info("========================== intercept response end ==========================")
            spend_time = int((flow.response.timestamp_end - flow.request.timestamp_start) * 1000)
            req_url = str(flow.request.url)

            req_method = str(flow.request.method)
            resp_status_code = str(flow.response.status_code)
            spend_time_str = str(spend_time)
            original_data_str = str(original_data)
            get_mock_data_str = str(get_mock_data)
            content={"param_len":" ","param_value":" "}
            param_value = req_url + split_joint + req_method + split_joint + resp_status_code + split_joint \
                      + spend_time_str + split_joint + original_data_str + split_joint + get_mock_data_str
            req_url_len = len(req_url)
            req_method_len = len(req_method)
            resp_status_code_len = len(resp_status_code)
            spend_time_str_len = len(spend_time_str)
            original_data_str_len = len(original_data_str)
            get_mock_data_str_len = len(get_mock_data_str)
            content["param_len"] = [req_url_len, req_method_len, resp_status_code_len, spend_time_str_len,
                                        original_data_str_len, get_mock_data_str_len]
            content["param_value"]=param_value

            ctx.log.info("========================== write data to file==========================")

            write_file(save_log_file, str(content), is_cover=False)
