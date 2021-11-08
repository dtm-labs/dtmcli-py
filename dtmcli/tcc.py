#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import traceback
import sys
import json
from dtmcli import utils

class Tcc(object):
  def __init__(self, dtmUrl, gid):
    self.dtm = dtmUrl
    self.gid = gid
    self.id_generator = utils.IdGenerator()
  def call_branch(self, body, tryUrl, confirmUrl, cancalUrl):
      branch_id = self.id_generator.new_branch_id()
      r = requests.post(self.dtm + "/registerBranch", json={
          "gid": self.gid,
          "branch_id": branch_id,
          "trans_type": "tcc",
          "status": "prepared",
          "data": json.dumps(body),
          "confirm": confirmUrl,
          "cancel": cancalUrl,
      })
      utils.check_result(r)
      r = requests.post(tryUrl, json=body, params={
          "gid": self.gid,
          "trans_type": "tcc",
          "branch_id": branch_id,
          "op": "try",
      })
      utils.check_result(r)
      return r

def tcc_global_transaction(dtmUrl, gid, tcc_cb):
    tcc = Tcc(dtmUrl, gid)
    tbody = {
        "gid": tcc.gid,
        "trans_type": "tcc",
    }
    try:
        r = requests.post(tcc.dtm + "/prepare", json=tbody)
        utils.check_result(r)
        tcc_cb(tcc)
        r = requests.post(tcc.dtm + "/submit", json=tbody)
        utils.check_result(r)
    except:
        traceback.print_exception(*sys.exc_info())
        r = requests.post(tcc.dtm + "/abort", json=tbody)
        utils.check_result(r)
        return ""
    return tcc.gid

def tcc_from_req(dtmUrl, gid, branch_id):
    if dtmUrl == "" or gid == "" or branch_id == "":
        raise Exception("bad tcc req info: dtm %s gid %s branch_id %s" % (dtmUrl, gid, branch_id))
    tcc = Tcc(dtmUrl, gid)
    tcc.id_generator = utils.IdGenerator(branch_id)
    return tcc
