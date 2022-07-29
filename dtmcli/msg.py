#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import requests
from dtmcli import transbase, dtmimp, barrier,utils

class Msg(object):
    def __init__(self, dtmUrl, gid):
        self.dtm = dtmUrl
        self.trans_base = transbase.TransBase(gid, "msg")

    def add(self, body, actionUrl):
        self.trans_base.steps.append({
            "action": actionUrl,
        })
        self.trans_base.payloads.append(json.dumps(body))
        return self

    def set_wait_result(self):
        self.trans_base.wait_result= True
        return self

    def prepare(self,query_prepared):
        if query_prepared:
            self.trans_base.query_prepared = query_prepared
        dtmimp.trans_call_dtm(
            self.dtm, self.trans_base.__dict__, "prepare", self.trans_base.request_timeout)

    def submit(self):
        dtmimp.trans_call_dtm(
            self.dtm, self.trans_base.__dict__, "submit", self.trans_base.request_timeout)

    def do_and_submit_db(self,query_prepared, conn, busi_call):
        return self.do_and_submit(query_prepared,lambda barrier: barrier.call(conn,busi_call))

    def do_and_submit(self,query_prepared,busi_call):
        bb =  barrier.BranchBarrier(self.trans_base.trans_type, self.trans_base.gid, "00", "msg")
        self.prepare(query_prepared)
        err = None
        errb = None
        try:
            busi_call(bb)
        except Exception as e:
            errb = e
        if errb is not None and not isinstance(errb,utils.DTMFailureError):
            try:
                r = requests.get(query_prepared, params={
                            "dtm": self.dtm,
                            "gid": self.trans_base.gid,
                            "trans_type": self.trans_base.trans_type,
                            "branch_id": bb.branch_id,
                            "op": bb.op,
                })
                utils.check_result(r)
            except Exception as e:
                err = e
        if isinstance(errb,utils.DTMFailureError) or isinstance(err,utils.DTMFailureError):
            dtmimp.trans_call_dtm(self.dtm, self.trans_base.__dict__, "abort", self.trans_base.request_timeout)
        elif err is None:
            self.submit()
        if errb is not None:
            raise errb

