#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 14:13
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ce_nni_l2mc_e2e_onestep.py
# @Software: PyCharm

from ptp_nni_l2mc_basecase import *

class TestCase (PtpNniL2McTestBaseCase) :
    """
    TestCase
    使用拓扑ats5
    216(master)[3/1]----------[4/1]27(slave)
    """


if __name__ == "__main__" :
    case = TestCase('ne1', "L3_INTERFACE", 'ne2', "L3_INTERFACE_1")
    # case.init_redirection()
    case.execute()