#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 13:53
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ce_uni_l3uc_e2e_onestep.py
# @Software: PyCharm

from ptp_uni_l3uc_basecase import *

class TestCase (PtpUniL3UcTestBaseCase) :
    """
    TestCase
    使用拓扑ats2
    216(master)[8/1]----------[13/1]214(slave)
    """

if __name__ == "__main__" :
    case = TestCase('ne3', "L3_INTERFACE", 'L3_IP', 'NEXT_HOP', 'ne2', "L3_INTERFACE_2_100G", 'L3_IP_2', 'NEXT_HOP_2')  #ats2
    # case = TestCase('ne2', 'L3_INTERFACE_1', 'L3_IP_1', 'NEXT_HOP_1', 'ne1', 'L3_INTERFACE', 'L3_IP', 'NEXT_HOP')  # ats6
    # case.init_redirection()
    case.execute()