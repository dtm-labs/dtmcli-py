# dtmcli [![Version][version-badge]][version-link] ![MIT License][license-badge]


a client for distributed transaction manager [dtm](https://github.com/yedf/dtm)


`dtmcli` 是分布式事务管理器dtm的客户端sdk


### 使用方式

```python
from dtmcli import tcc

def fire_tcc():
    gid = tcc.tcc_global_transaction(dtm, tcc_trans)
    return {"gid": gid}

def tcc_trans(t):
    req = {"amount": 30}
    t.call_branch(req, svc + "/TransOutTry", svc + "/TransOutConfirm", svc + "/TransOutCancel")
    t.call_branch(req, svc + "/TransInTry", svc + "/TransInConfirm", svc + "/TransInCancel")

```


### 安装

```
$ pip install dtmcli
```


### License

[MIT](https://github.com/yedf/dtmcli/blob/master/LICENSE)


[version-badge]:   https://img.shields.io/pypi/v/dtmcli
[version-link]:    https://pypi.python.org/yedf/dtmcli-py/
[license-badge]:   https://img.shields.io/github/license/yedf/dtmcli-py