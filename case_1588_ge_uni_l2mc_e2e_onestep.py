#!/usr/bin/env python
# coding: utf-8
######################################################################
#导入需要的库、模块、函数
######################################################################
from ptp_uni_l2mc_basecase import *

class TestCase (PtpUniL2McTestBaseCase) :
    """
    TestCase
    """


if __name__ == "__main__" :
    case = TestCase('ne1', "PTP_INTERFACE_GE", 'ne2', "PTP_INTERFACE_GE")
    # case.init_redirection()
    case.execute()


