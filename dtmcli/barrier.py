
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from dtmcli import utils

class AutoCursor:
  def __init__(self, cursor):
    self.cursor = cursor
  def __enter__(self):
    return self.cursor
  def __exit__(self, type, value, trace):
    self.cursor.connection.close()
    self.cursor.close()


class BranchBarrier(object):
  def __init__(self, trans_type, gid, branch_id, branch_type):
    self.trans_type = trans_type
    self.gid = gid
    self.branch_id = branch_id
    self.branch_type = branch_type
    self.barrier_id = 0
  def call(self, cursor, busi_callback):
    self.barrier_id = self.barrier_id + 1
    bid = "%02d" % self.barrier_id
    try:
      orgin_branch = {
        "cancel": "try",
        "compensate": "action",
      }.get(self.branch_type, "")
      origin_affected = insert_barrier(cursor, self.trans_type, self.gid, self.branch_id, orgin_branch, bid, self.branch_type)
      current_affected = insert_barrier(cursor, self.trans_type, self.gid, self.branch_id, self.branch_type, bid, self.branch_type)
      print("origin_affected: %d, current_affected: %d" % (origin_affected, current_affected))
      if (self.branch_type == "cancel" or self.branch_type == "compensate") and origin_affected > 0: # 这是空补偿
        return None
      elif current_affected == 0: # 插入不成功
        affected = cursor.fetchall("select 1 from dtm_barrier.barrier where trans_type='%s' and gid='%s' and branch_id='%s' and branch_type='%s' and barrier_id='%s' and reason='%s'" % (self.trans_type, self.gid, self.branch_id, self.branch_type, self.barrier_id, self.branch_type))
        if affected == 0: # 不是当前分支类型插入，说明这是悬挂操作，因此走回滚逻辑
          raise Exception("FAILURE")
      busi_callback(cursor)
      cursor.connection.commit()
    except :
      cursor.connection.rollback()
      raise

# return affected_rows
def insert_barrier(cursor, trans_type, gid, branch_id, branch_type, barrier_id, reason):
  if branch_type == "":
    return 0
  return utils.sqlexec(cursor, "insert ignore into dtm_barrier.barrier(trans_type, gid, branch_id, branch_type, barrier_id, reason) values('%s','%s','%s','%s','%s','%s')" % (trans_type, gid, branch_id, branch_type, barrier_id, reason))
