#!/usr/bin/python
# coding: utf-8
# Copyright (c) 2013 Jan Lübbe - see LICENSE file

import re

from exceptions import Exception

offset = re.compile(r"(CONTROL_PADCONF_.*?)\s+(0x\w+)")
offsets = {}
for line in open('mux.h').readlines():
  m = offset.search(line)
  if m:
    offsets[m.group(1)] = int(m.group(2), 16) - 0x800

mux = re.compile(r"(CONTROL_PADCONF_.*?), \((\w+) \| (\w+) \| (\w+) \)\) /\* ([\w\[\]]+) \*/")
for line in open('pinmux.h').readlines():
  #print line
  m = mux.search(line)
  if m:
    off = offsets[m.group(1)]
    reg = 0
    comment = m.group(1)[16:].lower()
    if comment != m.group(5).lower():
      comment += '.'+m.group(5).lower()
    if m.group(2) == 'IEN':
      reg |= (1<<5)
      comment += ', INPUT'
    elif m.group(2) == 'IDIS':
      comment += ', OUTPUT'
    else:
      raise Exception("bad field 2: %s" % m.group(2))
    if m.group(3) == 'PD':
      comment += '_PULLDOWN'
    elif m.group(3) == 'PU':
      reg |= (2<<3)
      comment += '_PULLUP'
    elif m.group(3) == 'OFF':
      reg |= (1<<3)
    else:
      raise Exception("bad field 3: %s" % m.group(3))
    if m.group(4).startswith('MODE'):
      reg |= int(m.group(4)[4:])
      comment += ' | ' + m.group(4)
    else:
      raise Exception("bad field 4: %s" % m.group(4))
    print 4*'\t' + '0x%03x 0x%02x' % (off, reg) + '\t' + '/* %s */' % comment
