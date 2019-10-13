#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:15
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ge_nni_l2mc_e2e_onestep.py
# @Software: PyCharm

from ptp_nni_l2mc_basecase import *

class TestCase (PtpNniL2McTestBaseCase) :
    """
    TestCase
    """


if __name__ == "__main__" :
    case = TestCase('ne1', "PTP_INTERFACE_GE", 'ne2', "PTP_INTERFACE_GE")
    # case.init_redirection()
    case.execute()