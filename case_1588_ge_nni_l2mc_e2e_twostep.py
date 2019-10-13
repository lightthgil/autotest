#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:15
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ge_nni_l2mc_e2e_onestep.py
# @Software: PyCharm
from workspace.suites.ats_ptp.ptp_nni_l2mc_basecase import PtpNniL2McTestBaseCase

class TestCase (PtpNniL2McTestBaseCase) :
    """
    TestCase
    """

    def add_cfg(self):
        errornum = super(TestCase, self).add_cfg()
        errornum += self.change_to_twostep()
        return errornum


if __name__ == "__main__" :
    case = TestCase('ne1', "PTP_INTERFACE_GE", 'ne2', "PTP_INTERFACE_GE")
    # case.init_redirection()
    case.execute()