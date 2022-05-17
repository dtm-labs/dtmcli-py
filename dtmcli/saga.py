#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from dtmcli import transbase, dtmimp


class Saga(object):
    def __init__(self, dtmUrl, gid):
        self.dtm = dtmUrl
        self.trans_base = transbase.TransBase(gid, "saga")

    def add(self, body, actionUrl, compensateUrl):
        self.trans_base.steps.append({
            "action": actionUrl,
            "compensate": compensateUrl,
        })
        self.trans_base.payloads.append(json.dumps(body))
        return self

    def add_branch_order(self, branch, pre_branches):
        self.orders[branch] = pre_branches
        return self

    def set_concurrent(self):
        self.trans_base.concurrent = True
        return self

    def build_custom_options(self):
        if self.trans_base.concurrent:
            self.trans_base.custom_data = json.dumps(
                {"orders": self.orders, "concurrent": self.concurrent})

    def submit(self):
        self.build_custom_options()
        dtmimp.trans_call_dtm(
            self.dtm, self.trans_base.__dict__, "submit", self.trans_base.request_timeout)
