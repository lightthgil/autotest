#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 12:53
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_l2mc_basecase.py.py
# @Software: PyCharm

from ptp_basecase import *

class PtpL2McTestBaseCase (PtpBaseCase) :
    """
    PtpL3UcTestBaseCase
    """

    @log_func_name()
    def __init__(self, master_ne = None, master_if = None, slave_ne = None, slave_if = None):
        super(PtpL2McTestBaseCase, self).__init__(master_ne, master_if, slave_ne, slave_if)


    def get_cmd_master_ptp_set(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.master_cmd_list.enter_configure_terminal()
                + self.master_cmd_list.enter_ptp_terminal()
                + self.master_cmd_list.set_ptp_port_mc(self.master_if)
                + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.set_ptp_port_mc(self.master_if), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
        ]


    def get_cmd_slave_ptp_set(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.slave_cmd_list.enter_configure_terminal()
                + self.slave_cmd_list.enter_ptp_terminal()
                + self.slave_cmd_list.set_ptp_port_mc(self.slave_if)
                + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.set_ptp_port_mc(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
        ]

if __name__ == "__main__" :
    case = PtpL2McTestBaseCase('ne1', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'ne2', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP')
    case.init_redirection()
    case.execute()