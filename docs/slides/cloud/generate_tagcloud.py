#! /usr/bin/env python
# -*- coding: utf-8 -*

import re
import sys
from collections import Counter

MAGIC = 1000

def main():
  cnt = Counter()
  denum = 0

  for line in sys.stdin:
    lst = line.strip().split()
    for elem in lst:
      exp = re.compile(ur'[\W\d]', re.UNICODE)
      key = exp.sub('', elem.decode('utf8').lower())
      if key and len(key) > 3:
        cnt[key] += 1
        denum += 1

  print '<tags>'
  for elem in sorted(cnt, key = lambda x: cnt[x], reverse = True):
    print '<a href="#" style="font-size:%dpt;">%s</a>' % (int(MAGIC * cnt[elem] / denum), elem.encode('utf8'))
  print '</tags>'

if __name__ == "__main__":
  main()
