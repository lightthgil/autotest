#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 14:15
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ce_uni_l2mc_e2e_onestep.py
# @Software: PyCharm

from ptp_uni_l2mc_basecase import *

class TestCase (PtpUniL2McTestBaseCase) :
    """
    TestCase
    使用拓扑ats2
    216(master)[8/1]----------[13/1]214(slave)
    """


if __name__ == "__main__" :
    case = TestCase('ne3', "L3_INTERFACE", 'ne2', "L3_INTERFACE_2_100G")    #ats2
    # case = TestCase('ne2', 'L3_INTERFACE_1', 'ne1','L3_INTERFACE')  #ats6
    # case.init_redirection()
    case.execute()