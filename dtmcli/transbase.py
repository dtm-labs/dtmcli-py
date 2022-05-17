#!/usr/bin/python
# -*- coding: UTF-8 -*-


class TransBase(object):
    def __init__(self, gid, trans_type):
        self.gid = gid
        self.trans_type = trans_type
        self.custom_data = None
        self.steps = []
        self.payloads = []
        self.query_prepared = None
        self.protocol = None

        self.wait_result = False
        self.timeout_to_fail = 0
        self.request_timeout = 8
        self.retry_interval = 0
        self.passthrough_headers = []
        self.branch_headers = {}
        self.concurrent = False
