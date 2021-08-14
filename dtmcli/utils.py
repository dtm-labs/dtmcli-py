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

def check_result(http_result):
  if http_result.status_code != 200:
    raise Exception("bad result")
  # print("http_result text is: ", http_result.text)
  if http_result.text.find("FAILURE") != -1:
    raise Exception("FAILURE")


def gen_gid(dtm):
  r = requests.get(dtm + "/newGid")
  check_result(r)
  return r.json()["gid"]

def sqlexec(cursor, sql):
  affected = cursor.execute(sql)
  print("affected %d for sql: %s" %(affected, sql))
  return affected
