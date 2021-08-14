#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import traceback
import sys
import json
from dtmcli import utils

class Saga(object):
  def __init__(self, dtmUrl, gid):
    self.dtm = dtmUrl
    self.gid = gid
    self.steps = []
  def add(self, body, actionUrl, compensateUrl):
    self.steps.append({
      "data": json.dumps(body),
      "action": actionUrl,
      "compensate": compensateUrl,
    })
    return self
  def submit(self):
    r = requests.post(self.dtm + "/submit", json={
      "gid": self.gid,
      "trans_type": "saga",
      "steps": self.steps,
    })
    utils.check_result(r)

