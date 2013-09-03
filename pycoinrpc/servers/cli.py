#!/bin/env python

import sys 
import json

def main():
  while 1:
    line = sys.stdin.readline()
    if not line: break

    response = "{}\n" + \
               "COMMIT\n"

    sys.stdout.write(response)

    sys.stdout.flush()

if __name__ == '__main__':
      main()
