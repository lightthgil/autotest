#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/12 13:10
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_nni_l3uc_basecase.py.py
# @Software: PyCharm

from ptp_l3uc_basecase import *

class PtpNniL3UcTestBaseCase (PtpL3UcTestBaseCase) :
    """
    PtpNniL3UcTestBaseCase
    """

    def get_cmd_master_ip_set(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.master_cmd_list.enter_configure_terminal()
                + self.master_cmd_list.enter_ethernet_interface(self.master_if)
                + self.master_cmd_list.set_ipaddr(self.master_ip + '/24')
                + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.enter_ethernet_interface(self.master_if), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.set_ipaddr(self.master_ip + '/24'), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
        ]

    def get_cmd_master_ip_no(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.master_cmd_list.enter_configure_terminal()
                + self.master_cmd_list.enter_ethernet_interface(self.master_if)
                + self.master_cmd_list.no_ipaddr(self.master_ip)
                + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.enter_ethernet_interface(self.master_if), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.no_ipaddr(self.master_ip), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
        ]

    def get_cmd_slave_ip_set(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.slave_cmd_list.enter_configure_terminal()
                + self.slave_cmd_list.enter_ethernet_interface(self.slave_if)
                + self.slave_cmd_list.set_ipaddr(self.slave_ip + '/24')
                + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.enter_ethernet_interface(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.set_ipaddr(self.slave_ip + '/24'), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
        ]

    def get_cmd_slave_ip_no(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.slave_cmd_list.enter_configure_terminal()
                + self.slave_cmd_list.enter_ethernet_interface(self.slave_if)
                + self.slave_cmd_list.no_ipaddr(self.slave_ip)
                + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.enter_ethernet_interface(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.no_ipaddr(self.slave_ip), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
        ]

    def change_interface_mode(self):
        return self._change_interface_mode('nni')

    def change_interface_mode_resume(self):
        return self._change_interface_mode_resume('nni')


if __name__ == "__main__" :
    case = PtpNniL3UcTestBaseCase('ne1', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP', 'ne2', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP')
    case.init_redirection()
    case.execute()