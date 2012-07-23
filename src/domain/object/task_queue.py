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

'''带有延迟时间的任务队列
'''

import sys
import os
import time

from util import g_logger
from error import ErrorCode as ECODE
from circular_queue import CircularQueue

class TDCQueue(object):
    '''Time Delay Circular Queue
    '''
    def __init__(self, capacity=10000, delay_time=10):
        self.__queue = CircularQueue(capacity=capacity)
        self.__set = set()
        self.__delay_time = delay_time
        g_logger.info('Capacity: %d, DelayTime: %d', capacity,
                self.__delay_time)
        pass

    def push(self, q_data):
        assert isinstance(q_data, dict), '%s is not DictType' % q_data
        assert q_data and 'k' in q_data and 'v' in q_data
        key = q_data['k']
        if key in self.__set:
            return ECODE.Q_EXISTS 
        else:
            self.__set.add(key)
            q_data = (q_data, int(time.time()) + self.__delay_time)
            return self.__queue.push(q_data)
        pass

    def pop(self):
        pop_items = {} 
        wait_time = self.__delay_time 
        current_time = int(time.time())

        while 1:
            q_item = self.__queue.head()
            if ECODE.Q_EMPTY == q_item:
                break

            g_logger.debug(q_item)

            q_data, expire_time = q_item

            if current_time >= expire_time:
                assert isinstance(q_data, dict)
                pop_items[q_data['k']] = q_data['v']
                self.__queue.pop()
                self.__set.remove(q_data['k'])
                pass
            else:
                wait_time = expire_time - current_time
                break
            pass
        return {'data': pop_items, 'wait_time': wait_time}

    def status(self):
        wait_time = self.__delay_time 
        current_time = int(time.time())

        result = self.__queue.status()

        q_item = self.__queue.head()
        if ECODE.Q_EMPTY != q_item:
            q_data, expire_time = q_item
            wait_time = expire_time - current_time

        result['wait_time'] = wait_time

        return result 
