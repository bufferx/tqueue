#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Zhang ZY<http://idupx.blogspot.com/> 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''/task/push, 任务队列入口 
'''

import os
import time
try:
    import json
except ImportError:
    import simplejson as json

import tornado.web
import tornado.escape

import assembly 

from util import options
from util import g_logger
from util import decorator as util_decorator

from base import BaseHandler
from domain.object.error import ErrorCode as ECODE
from domain.object.error import BaseError

class QueuePopHandler(BaseHandler):
    @property
    def queue(self):
        return self.application.queue

    @tornado.web.asynchronous
    def post(self):
        self.get()

    @tornado.web.asynchronous
    @util_decorator.validate_ip(g_logger)
    def get(self):
        try:
            result = {}
            result['e_code'] = ECODE.SUCCESS
            result['e_msg'] = 'SUCCESS'

            pop_result = self.queue.pop()
            result['data'] = pop_result['data']
            result['wait_time'] = pop_result['wait_time']

            self.api_response(result)
        except BaseError, e:
            g_logger.error(e, ext_info=True)
            return self.api_response({'e_code':e.e_code, 'e_msg': '%s' %
                    e, 'data': {}})
