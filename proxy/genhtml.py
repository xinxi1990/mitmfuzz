#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Author  : xinxi
@Time    : 2018/12/5 18:34
@describe: 创建报告
"""

import os,re,time,subprocess,sys,json
sys.path.append('..')
from jinja2 import Environment, PackageLoader
from deepdiff import DeepDiff



class Create():

    def __init__(self,report_path,log_path):
        self.report_path = report_path
        self.log_path = log_path

    def create_html(self):
        '''
        生成html报告
        '''
        report_folder = os.path.join(self.report_path, 'reports')
        if not os.path.exists(report_folder):
            os.makedirs(report_folder)
            print("创建报告存储文件夹:{}".format(report_folder))
        report_path = os.path.join(report_folder, "report_{}.html".format(time.strftime("%Y%m%d%H%M%S")))
        try:
            env = Environment(loader=PackageLoader('proxy', 'templates'))
            template = env.get_template("template.html")
            records = Create.gen_data(self.log_path)
            html_content = template.render(html_report_name="测试报告",records=records)
            with open(report_path, "wb") as f:
                f.write(html_content.encode("utf-8"))
                print('报告地址:\n{}'.format(report_path))
        except Exception as e:
            print('生成报告异常!{}'.format(e))
        finally:
            return report_path


    @staticmethod
    def gen_data(file_path):
        '''
        组装数据
        :return:
        '''
        records = []
        with open(file_path) as f_r:
            for line in f_r.readlines():
                item = line.split('|')
                data = {}
                data['name'] = item[0]
                data['method'] = item[1]
                data['status'] = item[2]
                data['response_time_ms'] = item[3]
                data['original'] =  json.dumps(eval(item[4]),indent=4)
                data['intercept'] = json.dumps(eval(item[5]),indent=4)
                # diff_data = diff(eval(item[2]),eval(item[3]))
                diff_data = DeepDiff(eval(item[4]), eval(item[5]), ignore_order=True)
                data['diff'] = diff_data
                records.append(data)
        return records



if __name__ == '__main__':
    save_path  = sys.argv[1]
    request_log_path = sys.argv[2]
    Create(save_path,request_log_path).create_html()


