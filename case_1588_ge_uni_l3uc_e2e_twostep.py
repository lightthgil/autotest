#!/usr/bin/env python
# coding: utf-8
######################################################################
# 导入需要的库、模块、函数
######################################################################

from ptp_uni_l3uc_basecase import *

class TestCase (PtpUniL3UcTestBaseCase) :
    """
    TestCase
    """

    def add_cfg(self):
        errornum = super(TestCase, self).add_cfg()
        errornum += self.change_to_twostep()
        return errornum

if __name__ == "__main__" :
    case = TestCase('ne1', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP', 'ne2', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP')
    # case.init_redirection()
    case.execute()


