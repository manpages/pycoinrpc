#!/bin/env python

import sys 
import json
#sys.path.append('../')
#from wrapper import rpc
from pycoinrpc.wrapper import Wrapper

def main():
  while 1:
    line = sys.stdin.readline()
    if not line: break

    wrapper = Wrapper()
    response = wrapper.rpc(line) + "\n" + \
               "COMMIT\n"

    sys.stdout.write(response)

    sys.stdout.flush()

if __name__ == '__main__':
      main()
