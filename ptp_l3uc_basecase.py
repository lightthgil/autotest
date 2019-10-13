#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 14:59
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_l3uc_basecase.py
# @Software: PyCharm

#!/usr/bin/env python
# coding: utf-8
######################################################################
# 导入需要的库、模块、函数
######################################################################
from ptp_basecase import *
from abc import ABCMeta, abstractmethod

class PtpL3UcTestBaseCase (PtpBaseCase) :
    """
    PtpL3UcTestBaseCase
    """
    __metaclass__ = ABCMeta

    @log_func_name()
    def __init__(self, master_ne = None, master_if = None, master_ip = None, master_next_ip = None, slave_ne = None, slave_if = None, slave_ip = None, slave_next_ip = None):
        super(PtpL3UcTestBaseCase, self).__init__(master_ne,  master_if, slave_ne, slave_if)
        if not hasattr(self, "master_ip"):
            if master_ip:
                self.master_ip = master_ip
            else:
                exit("no initialization master_ip")
        if not hasattr(self, "master_next_ip"):
            if master_next_ip:
                self.master_next_ip = master_next_ip
            else:
                exit("no initialization master_ip")

        if not hasattr(self, "slave_ip"):
            if slave_ip:
                self.slave_ip = slave_ip
            else:
                exit("no initialization slave_ip")
        if not hasattr(self, "slave_next_ip"):
            if slave_next_ip:
                self.slave_next_ip = slave_next_ip
            else:
                exit("no initialization slave_next_ip")

    @abstractmethod
    def get_cmd_master_ip_set(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    @abstractmethod
    def get_cmd_master_ip_no(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    @abstractmethod
    def get_cmd_slave_ip_set(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    @abstractmethod
    def get_cmd_slave_ip_no(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    def get_cmd_master_ptp_set(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.master_cmd_list.enter_configure_terminal()
                + self.master_cmd_list.enter_ptp_terminal()
                + self.master_cmd_list.set_ptp_port_uc(self.master_if, self.master_next_ip)
                + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.set_ptp_port_uc(self.master_if, self.master_next_ip), master_dic, self.master_ne, CLI_PORT],
            # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
        ]


    def get_cmd_slave_ptp_set(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return [
            [self.slave_cmd_list.enter_configure_terminal()
                + self.slave_cmd_list.enter_ptp_terminal()
                + self.slave_cmd_list.set_ptp_port_uc(self.slave_if, self.slave_next_ip)
                + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.set_ptp_port_uc(self.slave_if, self.slave_next_ip), slave_dic, self.slave_ne, CLI_PORT],
            # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
        ]



