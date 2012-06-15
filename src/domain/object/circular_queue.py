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

'''循环队列
'''

import sys
import os

from util import g_logger
from error import ErrorCode as ECODE

class CircularQueue(object):

    CAPACITY = 10000 
    POP_COUNT = 0

    def __init__(self, capacity=10000):
        self.__list = []
        self.size = 0
        self.front = 0
        self.rear = 0
        self.__update_capacity(capacity)
        pass

    def __update_capacity(self, capacity):
        if capacity:
            CircularQueue.CAPACITY = capacity
        for i in xrange(CircularQueue.CAPACITY):
            self.__list.append('')

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        if (self.rear + 1) % CircularQueue.CAPACITY == self.front:
            return True 
        else:
            return False 
        pass

    def push(self, value):
        if self.is_full():
            return ECODE.Q_FULL 
        else:
            self.__list[self.rear] = value
            self.rear = (self.rear + 1) % CircularQueue.CAPACITY
            self.size += 1
            return ECODE.Q_OK

    def pop(self):
        if self.is_empty():
            return ECODE.Q_EMPTY
        value = self.__list[self.front]
        self.__list[self.front] = ''
        self.front = (self.front + 1) % CircularQueue.CAPACITY
        self.size -= 1
        CircularQueue.POP_COUNT += 1
        return value
        pass

    def head(self):
        if self.is_empty():
            return ECODE.Q_EMPTY
        value = self.__list[self.front]
        return value
        pass

    def status(self):
        return {
                'front': self.front,
                'rear': self.rear,
                'size': self.size,
                'capacity': CircularQueue.CAPACITY,
                'popcount': CircularQueue.POP_COUNT,
                }

    def clean(self):
        del self.__list[:]
        g_logger.info('CircularQueue::Clean()')
        pass

    @staticmethod
    def instance():
        if not hasattr(CircularQueue, '_instance'):
            CircularQueue._instance = CircularQueue()
        return CircularQueue._instance
    pass

if __name__ == '__main__':
    print ECODE.Q_OK
