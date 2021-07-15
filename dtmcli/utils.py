#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests

class IdGenerator(object):
  def __init__(self, parent_id = ""):
    self.parent_id = parent_id
    self.branch_id = 0
  def new_branch_id(self):
    if self.branch_id >= 99:
      raise Exception("branch_id should not larger than 99")
    if len(self.parent_id) >= 20:
      raise Exception("parent_id length should not larger than 20")
    self.branch_id += 1
    return "%s%02d" % (self.parent_id, self.branch_id)

def check_status(status_code):
  if status_code != 200:
    raise Exception("bad result")

def gen_gid(dtm):
  r = requests.get(dtm + "/newGid")
  check_status(r.status_code)
  return r.json()["gid"]

