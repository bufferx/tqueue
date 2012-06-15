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

''' tornado web server
'''

import os
import sys
import time
import signal
import socket

import tornado.web
import tornado.httpserver

import assembly

import config.options

from util import options
from util import g_logger
from domain.object.task_queue import TDCQueue

import action

class TApplication(tornado.web.Application):

    def __init__(self):
        self.queue = TDCQueue(capacity=options.capacity,
                                delay_time=options.delay_time)
        self.whitesites_info = {
                'mtime' : 0,
                'data': {}
                }

        debug = options.env == "debug"
        app_settings = { 
                'gzip': 'on',
                'static_path': assembly.STATIC_PATH,
                'debug':debug,
                }

        handlers = [
            (r'/sayhi', action.HelloHandler),
            (r'/queue/push', action.QueuePushHandler),
            (r'/queue/pop', action.QueuePopHandler),
            (r'/queue/status', action.QueueStatusHandler),
        ]
        
        tornado.web.Application.__init__(self, handlers, **app_settings)

def handle_signal_kill(sig, frame):
    tornado.ioloop.IOLoop.instance().stop()
    g_logger.warning( 'Catch SIG: %d' % sig )

def main():
    ''' main function
    '''
    # 忽略Broken Pipe信号
    signal.signal(signal.SIGPIPE, signal.SIG_IGN);
                        
    # 处理kill信号
    signal.signal(signal.SIGINT, handle_signal_kill)
    signal.signal(signal.SIGQUIT, handle_signal_kill)
    signal.signal(signal.SIGTERM, handle_signal_kill)
    signal.signal(signal.SIGHUP, handle_signal_kill)

    g_logger.info('START TORNADO WEB SERVER ...')

    try:
        http_server =  \
            tornado.httpserver.HTTPServer(request_callback=TApplication())
        http_server.listen(options.port)

        tornado.ioloop.IOLoop.instance().start()

        g_logger.info('STOP TORNADO WEB SERVER ...')
    except socket.error, e:
        g_logger.warning('Socket Error: %s' % str(e))
    except KeyboardInterrupt, e:
        g_logger.warning('Gently Quit')
    except Exception, msg:
        g_logger.error('UnCaught Exception: %s' % msg)
        raise 

if __name__ == '__main__':
    main()
