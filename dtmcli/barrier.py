
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
  def __init__(self, trans_type, gid, branch_id, op):
    self.trans_type = trans_type
    self.gid = gid
    self.branch_id = branch_id
    self.op = op
    self.barrier_id = 0
  def call(self, cursor, busi_callback):
    self.barrier_id = self.barrier_id + 1
    bid = "%02d" % self.barrier_id
    try:
      orgin_branch = {
        "cancel": "try",
        "compensate": "action",
      }.get(self.op, "")
      origin_affected = insert_barrier(cursor, self.trans_type, self.gid, self.branch_id, orgin_branch, bid, self.op)
      current_affected = insert_barrier(cursor, self.trans_type, self.gid, self.branch_id, self.op, bid, self.op)
      print("origin_affected: %d, current_affected: %d" % (origin_affected, current_affected))

      # for msg's DoAndSubmit, repeated insert should be rejected
      if self.op == "msg" and current_affected == 0:
        cursor.connection.commit()
        raise Exception("msg duplicate error")
      # origin_affected > 0 这个是空补偿; current_affected == 0 这个是重复请求或悬挂
      if (self.op == "cancel" or self.op == "compensate") and origin_affected > 0 or current_affected == 0:
        cursor.connection.commit()
        return None
      busi_callback(cursor)
      cursor.connection.commit()
    except :
      cursor.connection.rollback()
      raise
  def query_prepared(self, cursor):
      affected_rows = insert_barrier(cursor, self.trans_type, self.gid, "00", "msg", "01", "rollback")
      cursor.connection.commit()
      sql = 'select reason from dtm_barrier.barrier where gid = "%s" and branch_id = "%s" and op= "%s" and barrier_id= "%s" '%(self.gid,"00","msg","01")
      cursor.execute(sql)
      data = cursor.fetchone()
      print("query_prepared_sql: %s\t query_prepared_data: %s"%(sql,data))
      if data[0] == "rollback":
        raise utils.DTMFailureError('msg rollback')


# return affected_rows
def insert_barrier(cursor, trans_type, gid, branch_id, op, barrier_id, reason):
  if op == "":
    return 0
  return utils.sqlexec(cursor, "insert ignore into dtm_barrier.barrier(trans_type, gid, branch_id, op, barrier_id, reason) values('%s','%s','%s','%s','%s','%s')" % (trans_type, gid, branch_id, op, barrier_id, reason))
