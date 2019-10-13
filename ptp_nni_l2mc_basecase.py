#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:03
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_nni_l2mc_basecase.py
# @Software: PyCharm

from ptp_l2mc_basecase import *

class PtpNniL2McTestBaseCase (PtpL2McTestBaseCase) :
    """
    PtpNniL2McTestBaseCase
    """

    def change_interface_mode(self):
        return self._change_interface_mode('nni')

    def change_interface_mode_resume(self):
        return self._change_interface_mode_resume('nni')


if __name__ == "__main__" :
    case = PtpNniL2McTestBaseCase('ne1', "PTP_INTERFACE_GE", 'ne2', "PTP_INTERFACE_GE")
    case.init_redirection()
    case.execute()