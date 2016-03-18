#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
It returns the italian Procince given a CAP Comune.

Usage:

    import cap
    ...
    ...
    print cap.get('47122')

A _CapNotFound_ exception is raised if cap not found.


Luca Bacchi <bacchilu@gmail.com> - http://www.lucabacchi.it
"""

import urllib2
import StringIO
import zipfile


class CapNotFound(Exception):

    pass


capDict = None


def getListaComuni():
    global capDict
    if capDict is not None:
        return capDict

    url = 'http://lab.comuni-italiani.it/files/listacomuni.zip'
    c = StringIO.StringIO(urllib2.urlopen(urllib2.Request(url)).read())
    with zipfile.ZipFile(c, 'r') as myzip:
        lines = (l for l in myzip.open('listacomuni.txt'))
        res = [l.split(';') for l in lines][1:]
        capDict = dict([(l[5], l[2]) for l in res])
        return capDict


def get(cap):
    data = getListaComuni()
    try:
        return data[cap]
    except KeyError:
        cap = cap[:-1] + 'x'
        try:
            return data[cap]
        except KeyError:
            cap = cap[:-2] + 'xx'
            try:
                return data[cap]
            except KeyError:
                raise CapNotFound()


if __name__ == '__main__':
    print get('35031')
    print get('47122')
    print get('37111')
    print get('99999')
