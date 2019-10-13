#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21 11:39
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_xe_nni_l2mc_e2e_onestep.py
# @Software: PyCharm

from ptp_nni_l2mc_basecase import *

class TestCase (PtpNniL2McTestBaseCase) :
    """
    TestCase
    使用拓扑ats5
    216(master)[1/9]----------[1/9]28(slave)
    """


if __name__ == "__main__" :
    case = TestCase('ne1', "L3_INTERFACE_4", 'ne3', "L3_INTERFACE_4")
    # case.init_redirection()
    case.execute()