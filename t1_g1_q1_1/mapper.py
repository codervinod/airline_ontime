#!/usr/bin/env python

import sys

def main():
  for line in sys.stdin:
    line = line.strip().split("\t")
    if len(line) > 2:
      print "{0}\t{1}".format(line[0], 1)

if __name__ == '__main__':
  main()
