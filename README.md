[![PyPI - latest](https://img.shields.io/pypi/v/iconconsole?label=latest&logo=pypi)](https://pypi.org/project/iconconsole)
[![PyPI - Python](https://img.shields.io/pypi/pyversions/iconconsole?logo=pypi)](https://pypi.org/project/iconconsole)

# iconconsole
Python package to interact with the ICON network

## Requirements

- Python 3.7 or later.

## Installation

Setup a virtual environment first, and install iconconsole via pypi.

## Usage

You can use `iconconsole` interactively on the python console.

``` shell
$ python
Python 3.7.7 (v3.7.7:d7c567b08f, Mar 10 2020, 02:56:16)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from iconconsole import *
>>>
```

## Features

### Network
`Network` allows you to specify your target ICON network. <br>
You can get the network instance with `Network(uri: str, nid: int = 0)`.<br>
You can use predefined strings as an `uri`. You can get list of predefined network via `ic.Network.PREDEFINED`
```python
>>> net = Network('berlin')
>>> net.uri
'https://berlin.net.solidwallet.io'
>>> Network.PREDEFINED
{'mainnet': {'uri': 'https://ctz.solidwallet.io', 'nid': 3},
 'sejong': {'uri': 'https://sejong.net.solidwallet.io',
            'nid': 83,
            'faucets': 'cx6434bfdcb6b3ad4a4f5ced0075c73b9fea2a172c'},
 'lisbon': {'uri': 'https://lisbon.net.solidwallet.io',
            'nid': 2,
            'faucets': 'cxcbece91fb181b754f906640a9746f361a3113641'},
 'berlin': {'uri': 'https://berlin.net.solidwallet.io',
            'nid': 7,
            'faucets': 'cx760787ff9b4b337ac1f2bacd2bfe2ec42ef88c0d'}}
```

### Account
`Account` allow you to sign the TX and to do actions such as querying a balance or transfer ICX.

#### Create and load an Account
You can create new `Account` and load from keystore file.
```python
>>> account1 = Account()    # create new
>>> account2 = Account(keystore=./path/to/keystore, password="password")    # load from keystore file
```

#### Methods
The `Account.address()` is used to get the address of account.
```python
>>> account1.address()
'hx83d0056c46a36d623c42be5769f30210c34400bd'
```
The `Account.network()` and `Account.get_network()` are used to set and get the target network of an account.<br>
```python
>>> net.uri
'https://berlin.net.solidwallet.io'
>>> account1.network(net=net)
>>> account1.get_network().uri
'https://berlin.net.solidwallet.io'
```
The `Account.balance()` is used to query the balance of an account in the network specified by `Account.network()`.
```python
>>> account1.balance()
0
```
The `Account.transfer()` is used to transfer ICX to another account in the network specified by `Account.network()`.
```python
>>> txr = account2.transfer(account1, 10)
>>> account1.balance()
10
```

### Score
`Score` allows you to deploy and update the SCORE and call the external method of SCORE

#### Deploy, update and load a SCORE
```python
>>> score, txr = Score.deploy(net, account1, "./hello-world-0.1.0-optimized.jar", {"name": "Alice"})    # deploy SCORE
>>> score.address()
'cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af'
>>> score.apis()
['writable setName(name: str):',
 'readonly name() -> str:',
 'readonly getGreeting() -> str:']
>>> score.name()
{'jsonrpc': '2.0', 'result': 'Alice', 'id': 1648466089}
>>> score.update("./hello-world-0.1.0-optimized.jar", {"name": "Bob"})  # update SCORE
>>> score.address()
'cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af'
>>> score.name()
{'jsonrpc': '2.0', 'result': 'Alice', 'id': 1648466091}
>>> load_score = Score(net, "cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af")   # load SCORE
>>> load_score.address()
'cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af'
>>> load_score.name()
{'jsonrpc': '2.0', 'result': 'Alice', 'id': 1648466093}
```

#### Methods
The `Score.address()` is used to get an address of SCORE. <br>
The `Score.account()` and `Score.get_account()` is used to set and get the signer account of SCORE.

#### Call external methods of SCORE
You can query the external methods of SCORE and call with `Score` object
```python
>>> score.apis()
['writable setName(name: str):',
 'readonly name() -> str:',
 'readonly getGreeting() -> str:']
>>> txr = score.account(account1).setName("ICON")
```


### TransactionResult
`TransactionResult` allows you to query transaction, transaction result and trace of transaction.
* `hash()` is used to get hash of transaction
* `transaction()` is used to get the transaction
* `result()` is used to get the result of transaction
* `trace()` is used to get the trace log of transaction execution
```python
>>> txr = score.account(account1).setName("ICON")
>> txr.hash()
'0x9499fc3ce8a21039b3951dc08cb1f2e4098f46f2b8e5f7e518c378ebe7569539'
>>> txr.transaction()
{'jsonrpc': '2.0',
 'result': {'blockHash': '0x70319f44901cf9e3af472bb22573b91fdb70b335e1e64b0cea256a5ad0849dd5',
            'blockHeight': '0xe5f',
            'data': {'method': 'setName', 'params': {'name': 'ICON'}},
            'dataType': 'call',
            'from': 'hxa8df82e93e8a9cd5325e37289bcd0fbc0a8b4e5e',
            'nid': '0x7',
            'signature': 'M5c88PehWFkpr83AOtVIH4zJKTEdPVe41EzckXhIufo6XSBUtLqpUy5pthlMWKvBg+eQBLoaRMifD3uc7Kq1SQA=',
            'stepLimit': '0x989680',
            'timestamp': '0x5db45c316fe0b',
            'to': 'cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af',
            'txHash': '0x9499fc3ce8a21039b3951dc08cb1f2e4098f46f2b8e5f7e518c378ebe7569539',
            'txIndex': '0x1',
            'value': '0x0',
            'version': '0x3'},
 'id': 1648467564}
>>> txr.result()
{'jsonrpc': '2.0',
 'result': {'blockHash': '0x70319f44901cf9e3af472bb22573b91fdb70b335e1e64b0cea256a5ad0849dd5',
            'blockHeight': '0xe5f',
            'cumulativeStepUsed': '0x23fc5',
            'eventLogs': [],
            'logsBloom': '0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
            'status': '0x1',
            'stepPrice': '0x2540be400',
            'stepUsed': '0x23fc5',
            'to': 'cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af',
            'txHash': '0x9499fc3ce8a21039b3951dc08cb1f2e4098f46f2b8e5f7e518c378ebe7569539',
            'txIndex': '0x1'},
 'id': 1648467626}
>>> txr.trace()
{'failure': {'code': 1, 'message': 'Calculator(height=3701,exp=3661)'},
 'logs': [{'level': 2,
           'msg': 'FRAME[1] TRANSACTION start from=hxa8df82e93e8a9cd5325e37289bcd0fbc0a8b4e5e to=cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af id=0x9499fc3ce8a21039b3951dc08cb1f2e4098f46f2b8e5f7e518c378ebe7569539',
           'ts': 0},
          {'level': 2,
           'msg': 'FRAME[1] STEP apply type=default count=1 cost=100000 total=100000',
           'ts': 80},
          {'level': 2,
           'msg': 'FRAME[1] STEP apply type=input count=45 cost=9000 total=109000',
           'ts': 84},
          {'level': 2, 'msg': 'FRAME[2] START parent=FRAME[1]', 'ts': 92},
          {'level': 2,
           'msg': 'FRAME[2] INVOKE start score=cxf0a8e3aad24bad5f41444e76b865ca4aaeef84af method=setName',
           'ts': 95},
          {'level': 2,
           'msg': 'FRAME[2] STEP apply type=contractCall count=1 cost=25000 total=25000',
           'ts': 99},
          {'level': 2,
           'msg': 'FRAME[2] INVOKE done status=Success steps=13397 result=null',
           'ts': 6755},
          {'level': 2,
           'msg': 'FRAME[2] STEP apply cost=13397 total=38397',
           'ts': 6775},
          {'level': 2, 'msg': 'FRAME[2] END success=true steps=38397', 'ts': 6777},
          {'level': 2,
           'msg': 'FRAME[1] STEP apply cost=38397 total=147397',
           'ts': 6783},
          {'level': 2,
           'msg': 'FRAME[1] TRANSACTION charge fee=1473970000000000 steps=147397 price=10000000000',
           'ts': 6791},
          {'level': 2,
           'msg': 'FRAME[1] TRANSACTION done status=Success steps=147397 price=10000000000',
           'ts': 6797}],
 'status': '0x0'}
```


## License

This project is available under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
