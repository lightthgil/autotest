#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 11:42
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_xe_uni_l2mc_e2e_onestep.py
# @Software: PyCharm

from ptp_uni_l2mc_basecase import *

class TestCase (PtpUniL2McTestBaseCase) :
    """
    TestCase
    使用拓扑ats5
    216(master)[1/12]----------[1/3]28(slave)
    """


if __name__ == "__main__" :
    case = TestCase('ne1', "L3_INTERFACE_2", 'ne3', "L3_INTERFACE_2")
    # case.init_redirection()
    case.execute()
