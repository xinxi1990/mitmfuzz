#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
使用mitmproxy代理工具篡改请求
"""

import mitmproxy.http
from mitmproxy import ctx
import json,time,os
from proxyrule import ProxyRule
from mathrandom import MathRandom
from filetools import *


project_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
now = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_intercept.log"
save_log_file = os.path.join(project_path, now)

def request(flow: mitmproxy.http.HTTPFlow):
    request = flow.request
    ctx.log.info("========================== intercept request start ==========================")
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

    black_list = ["png", "jpg", "js", "css", "html",'img','cdn']

    for balck_str in black_list:
        if balck_str in flow.request.url:
            ctx.log.info("========================== not intercept response ==========================")
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
            content = str(flow.request.url) + '|' + str(flow.request.method) + '|' + str(flow.response.status_code) + '|' \
                      + str(spend_time) + '|' +  str(original_data) + '|' + str(get_mock_data)
            write_file(save_log_file,content,is_cover=False)






