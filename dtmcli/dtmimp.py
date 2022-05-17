#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from dtmcli import utils


def trans_call_dtm(dtm, body, operation, request_timeout):
    url = "%s/%s" % (dtm, operation)
    r = requests.post(url, json=body, timeout=request_timeout)
    utils.check_result(r)
