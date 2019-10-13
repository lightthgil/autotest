#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/14 15:03
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_uni_l2mc_basecase.py.py
# @Software: PyCharm

from ptp_l2mc_basecase import *

class PtpUniL2McTestBaseCase (PtpL2McTestBaseCase) :
    """
    PtpUniL2McTestBaseCase
    """

    def change_interface_mode(self):
        return self._change_interface_mode('uni')

    def change_interface_mode_resume(self):
        return self._change_interface_mode_resume('uni')


if __name__ == "__main__" :
    case = PtpUniL2McTestBaseCase('ne1', "PTP_INTERFACE_GE", 'ne2', "PTP_INTERFACE_GE")
    case.init_redirection()
    case.execute()