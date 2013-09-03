poorly documented cli and jsonrpc wrappers for pycoin.

provides:
 + pycoincli — cli interface to pycoin
 + pycoinrpc — jsonrpc interface to pycoin

output of both cli (stdin/out) and jsonrpc (http) servers
are JSON-RPC compatible: 

```
→{method: mmm, params: ppp, id: iii|null}
←{result: xxx|null, error: yyy|null, id: iii}
```

with one exception — now, to define the end of output, cli
server uses string "COMMIT\n". because.
