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

'''
@feature: Config Options
'''

import sys
import os

import assembly

import pyutil.lib.tornado as tornado
from pyutil.lib.tornado.options import define, options

DEFAULT_OPTIONS_PORT              = 8000 
DEFAULT_OPTIONS_LOG_ROOT_PATH     = \
    os.path.realpath(os.path.join(assembly.PROJECT_PATH, 'log'))
DEFAULT_QUEUE_CAPACITY            = 10 * 1000
DEFAULT_QUEUE_DELAYTIME           = 5 

def define_options():
    # 日志
    define("log_level", default = 'DEBUG', 
            help = "Set Log Level")

    define('log_root_path', default = DEFAULT_OPTIONS_LOG_ROOT_PATH, 
            help = 'Log file stored root path')

    define("app_name", default = 'TQUEUE_SERVICE', 
            help = "Set Log Level")

    define("port", default = DEFAULT_OPTIONS_PORT, 
            help = "Run server on a specific port, Default: %d" % DEFAULT_OPTIONS_PORT, type = int)

    define("env", default="dev", help="Service Run Environment")

    define("capacity", default = DEFAULT_QUEUE_CAPACITY,
            help = "Queue Capacity, Default: %d" % DEFAULT_QUEUE_CAPACITY, type = int)

    define("delay_time", default = DEFAULT_QUEUE_DELAYTIME,
            help = "Queue Pop Delay Time, Default: %d" % DEFAULT_QUEUE_DELAYTIME, type = int)

def _usage():
    print 'Usage: ./service -log_root_path=SpecifiedFile -port=SpecifiedPort'
    os._exit()
    pass

def _check_dir_tail(dir_name):
    if not dir_name or '' == dir_name:
        return dir_name
    _len = len(dir_name) - 1
    if '/' == dir_name[_len:]:
        dir_name = dir_name[0:_len]

    return dir_name
    pass

def _mkdir(file_dir):
    real_path = os.path.realpath(file_dir)
    if not os.path.exists(real_path):
        os.makedirs(real_path)
        pass
    pass

def init_options():
    define_options()
    # maybe some options will be use before load config file
    tornado.options.parse_command_line()
    if not options.log_root_path or not options.port:
        _usage()
    options.log_root_path = _check_dir_tail(options.log_root_path)
    options.log_path = '%s/%d' % (options.log_root_path, options.port)
    _mkdir(options.log_path)

init_options()
