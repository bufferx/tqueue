#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import httplib
import json

def test_post():
    '''test http post
    '''
    conn = httplib.HTTPConnection('localhost', 8000)
    params = {}
    for i in xrange(5):
        params['key_%d' % i] = {
                's': 'BJ',
                'd': 'SH',
                'tid': '999999'
                } 
        pass
    conn.request('POST', '/queue/push', json.dumps(params))
    response = conn.getresponse()
    print response.status, response.reason
    print response.read()
    pass

def main():
    test_post()

if __name__ == '__main__':
    main()
