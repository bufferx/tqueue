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

'''/queue/push, 任务队列入口 
'''

import os
import time

import tornado.web
import tornado.escape

import assembly 

from util import options
from util import g_logger
from util import CommonUtil
from util import HttpUtil
from util import decorator as util_decorator

from base import BaseHandler
from domain.object.error import ErrorCode as ECODE
from domain.object.error import ErrorMessage as EMSG

class QueuePushHandler(BaseHandler):
    @property
    def queue(self):
        return self.application.queue

    @tornado.web.asynchronous
    def get(self):
        self.post()

    @util_decorator.time_it
    @tornado.web.asynchronous
    def post(self):
        HttpUtil.validate_ip(self.request)
        try:
            if not self.request.body:
                return self.api_response({'e_code': ECODE.Q_ERROR, 'e_msg':
                    EMSG.Q_ERROR})

            json_obj = tornado.escape.json_decode(self.request.body)
            g_logger.info(json_obj)

            if not isinstance(json_obj, dict):
                return self.api_response({'e_code': ECODE.Q_TYPE_ERROR, 'e_msg':
                    EMSG.Q_TYPE_ERROR})

            for k, v in json_obj.iteritems():
                result = self.queue.push({'k': k, 'v': v})
                if ECODE.Q_FULL == result:
                    break
                pass

            self.api_response({'e_code':ECODE.SUCCESS, 'e_msg': 'SUCCESS'})
        except HTTPError, e:
            g_logger.error(e)
            return self.api_response({'e_code':ECODE.HTTP, 'e_msg': '%s' % e})
        except ValueError, e:
            g_logger.error(e)
            return self.api_response({'e_code': ECODE.Q_TYPE_ERROR, 'e_msg':
                EMSG.Q_TYPE_ERROR})
        except Exception, e:
            g_logger.error(e)
            return self.api_response({'e_code':ECODE.DEFAULT, 'e_msg':
                'Unknown'})
