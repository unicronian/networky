#!/usr/bin/env python2.7

#  ftp://ftp.ripe.net/pub/stats/arin/delegated-arin-extended-latest
#format:
#registry|cc|type|start|value|date|status|reg-id
__author__ = "Ryan Hendrickson (github@unicronian.net)"

import re
from urllib.request import urlopen
from ipaddress import IPv4Address

MYURL = "ftp://ftp.ripe.net/pub/stats/arin/delegated-arin-extended-latest"
COUNTRIES = ["US"]

def pullURLData(url, iplist):
  html = urlopen(url).read().splitlines()
  for line in html:
    linestr = str(line)
    datalist = linestr.split('|')
    if 'ipv4' in datalist[2]:
      for country in COUNTRIES:
        if country in datalist:
          #print("%s,%s,%s" % (datalist[1], datalist[3], datalist[4]))
          ipstart = IPv4Address(datalist[3])
          ipend = ipstart + (int(datalist[4]) - 1)
          iplist[str(ipstart)] = str(ipend)
  return iplist


def combineIPs(ipdict):
  combos = 1
  while combos > 0:
    combos = 0
    for key in sorted(ipdict.keys()):
      if key in ipdict.keys():
        ipstart = key
        ipend = ipdict[key]
        nextnetwork = str(IPv4Address(ipdict[key]) + 1)
    
        if nextnetwork in ipdict.keys():
          ipdict[key] = ipdict[nextnetwork]
          del ipdict[nextnetwork]
          combos = combos + 1
    #print(combos)

  return ipdict


def main():
  ipdict = {}
  ipdict = pullURLData(MYURL, ipdict)
  ipdict = combineIPs(ipdict)
  for key in sorted(ipdict.keys()):
    print("start:%s  end:%s -j ACCEPT" \
          % (key, ipdict[key]))


if __name__ == '__main__':
  main()