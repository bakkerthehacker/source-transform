# -*- coding: utf-8 -*-


def impossible():
    if not 'DEADBEEF' == 'REALBEEF':
        raise ValueError()
