#!/usr/bin/env python
# -*- coding: utf-8 -*-



def request(flow):
    flow.request.headers['User-Agent'] = 'MitmProxy'
    print(flow.request.headers)