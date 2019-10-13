#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 17:19
# @Author  : Jiang Bo
# @Site    : 
# @File    : ptp_basecase.py.py
# @Software: PyCharm

######################################################################
# 导入需要的库、模块、函数
######################################################################
import os
import sys
import re
from abc import ABCMeta, abstractmethod
from workspace.suites.ats_ptp.cmd_list_clk import cmd_list_clk

sys.path.append(os.path.abspath('../../..')) #将heavysmoker的路径加进来
from workspace.suites.ats_common.case_task_check import *
from cmd_list_ptp import cmd_list_ptp

ne_id_1     = 216
ne_id_2     = 27
ne_id_3     = 28

#以下为递增值，不是拓扑里的字典值
param_dic_p1_topo = {}
param_dic_p2_topo = {}
param_dic_p3_topo = {}
param_dic_smb_topo = {}

class PtpBaseCase (TnxxxCfg_BaseCase) :
    """
    PtpBaseCase
    """
    __metaclass__ = ABCMeta

    OPTIONS = [
        {
           'opt' : '--cfgfile',
           'dest': 'cfgfile',
           'metavar' : 'PATH',
           'help' : 'the file of netring configuration',
           'required' : False,
           'default' : "../ats_topo/tnxxx.xml"
        },
        {
           'opt' : '--topology',
           'dest': 'topology',
           'metavar' : 'TOPOLOGY',
           'help' : 'the topology for test',
           'required' : True,
           'default' : "ats_ons"
        },
        {
           'opt' : '--action',
           'dest': 'action',
           'metavar' : 'action',
           'help' : 'action',
           'required' : False,
           'default' : "add_check_del",
        },
        {
           'opt' : '--index',
           'dest': 'index',
           'metavar' : 'index',
           'help' : 'index',
           'required' : False,
           'default' : "0",
        },
        {
            'opt': '--master',
            'dest': 'master',
            'metavar': 'master',
            'help': 'master, eg:ne1\INTERFACE  or ne1\INTERFACE\IP\NEXTIP or 46\1/9. you can use dic in topo or immediate value',
            'required': False,
            'default': "",
        },
        {
            'opt': '--slave',
            'dest': 'slave',
            'metavar': 'slave',
            'help': 'slave, eg:ne2\INTERFACE  or ne2\INTERFACE\IP\NEXTIP or 49\1/5. you can use dic in topo or immediate value',
            'required': False,
            'default': "",
        }
    ]

    @log_func_name()
    def __init__(self, master_ne=None,  master_if=None, slave_ne=None, slave_if=None):

        super(PtpBaseCase, self).__init__()

        self.__topo = topology.load(self.options.topology)
        self.__topo.param_dic_p1.update(param_dic_p1_topo)
        self.__topo.param_dic_p2.update(param_dic_p2_topo)
        self.__topo.param_dic_p3.update(param_dic_p3_topo)
        self.__topo.param_dic_smartbit.update(param_dic_smb_topo)

        param_list = param_dic_p2_topo.keys() + param_dic_p3_topo.keys() + param_dic_smb_topo.keys()
        index_num = self.get_index_num(self.options.index)
        self.__action = self.options.action

        # 从option获取节点信息
        master = re.split("[\\\\,.\-;:`~|<>]", self.options.master)
        slave = re.split("[\\\\,.\-;:`~|<>]", self.options.slave)

        if len(master) >= 2:
            master_ne = master[0]
            master_if = master[1]
            if len(master) == 4:
                self.master_ip = master[2]
                self.master_next_ip = master[3]
        elif not (master_ne and master_if):
            exit("no initialization master, options.master = " + self.options.master + ", master_ne = " + str(master_ne) + ", master_if = " + str(master_if))

        if len(slave) >= 2:
            slave_ne = slave[0]
            slave_if = slave[1]
            if len(slave) == 4:
                self.slave_ip = slave[2]
                self.slave_next_ip = slave[3]
        elif not (slave_ne and slave_if):
            exit("no initialization slave, options.master = " + self.options.slave + ", master_ne = " + str(slave_ne) + ", master_if = " + str(slave_if))

        master_ne_index = re.findall(r'\d+\.?\d*', str(master_ne))[0]
        if master_ne_index == master_ne:
            self.master_ne = int(master_ne)
            master_param_dic_base = {}
        else:
            if hasattr(self.__topo, 'ne_id_' + master_ne_index):
                self.master_ne = getattr(self.__topo, 'ne_id_' + master_ne_index)
            else:
                exit('topo:' + str(self.__topo) + 'has no attr:' + 'ne_id_' + master_ne_index)
            if hasattr(self.__topo, 'param_dic_p' + master_ne_index):
                master_param_dic_base = getattr(self.__topo, 'param_dic_p' + master_ne_index)
            else:
                master_param_dic_base = {}
                exit('topo:' + str(self.__topo) + 'has no attr:' + 'param_dic_p' + master_ne_index)
        slave_ne_index = re.findall(r'\d+\.?\d*', str(slave_ne))[0]
        if slave_ne_index == slave_ne:
            self.slave_ne = int(slave_ne)
            slave_param_dic_base = {}
        else:
            if hasattr(self.__topo, 'ne_id_' + slave_ne_index):
                self.slave_ne = getattr(self.__topo, 'ne_id_' + slave_ne_index)
            else:
                exit('topo:' + str(self.__topo) + 'has no attr:' + 'ne_id_' + slave_ne_index)
            if hasattr(self.__topo, 'param_dic_p' + slave_ne_index):
                slave_param_dic_base = getattr(self.__topo, 'param_dic_p' + slave_ne_index)
            else:
                slave_param_dic_base = {}
                exit('topo:' + str(self.__topo) + 'has no attr:' + 'param_dic_p' + slave_ne_index)

        self.param_dic = []
        ''' PTP字典，格式为[(master_dic1, slave_dic1), (master_dic2, slave_dic2) ...] '''

        for i in range(index_num[0], index_num[1]):
            master_param_dic = self.gen_new_param_dic(master_param_dic_base, param_list, i)
            slave_param_dic = self.gen_new_param_dic(slave_param_dic_base, param_list, i)
            self.param_dic.append((master_param_dic, slave_param_dic))

        self.master_if = str(master_if)
        self.slave_if = str(slave_if)

        #创建PTP命令行类
        self.master_cmd_list = cmd_list_ptp(self.get_ne_type(self.master_ne))
        self.slave_cmd_list = cmd_list_ptp(self.get_ne_type(self.slave_ne))
        self.master_clk_cmd_list = cmd_list_clk(self.get_ne_type(self.master_ne))
        self.slave_clk_cmd_list = cmd_list_clk(self.get_ne_type(self.slave_ne))

        self.__master_need_to_resume =  []
        self.__slave_need_to_resume = []

    @log_func_name()
    def cleardb(self):
        errornum = 0

        cfg_info_list = [
            [cmd_list_factory_mode + dic_cmd_list_set_lgcard[self.master_ne], {}, self.master_ne, CLI_PORT, "system init"],
            [cmd_list_factory_mode + dic_cmd_list_set_lgcard[self.slave_ne], {}, self.slave_ne, CLI_PORT, "system init"],
            [self.__topo.cmd_list_p1_port_upgrade, self.__topo.param_dic_p1, self.master_ne, CLI_PORT],
            [self.__topo.cmd_list_p2_port_upgrade, self.__topo.param_dic_p2, self.slave_ne, CLI_PORT],
        ]

        if not self.run(cfg_info_list): errornum += 1
        time.sleep(10) #缓冲时间

        return errornum

    def get_cmd_master_ip_set(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    def get_cmd_master_ip_no(self, master_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    def get_cmd_slave_ip_set(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    def get_cmd_slave_ip_no(self, slave_dic):
        '''返回值类型为None或者[[cmd, dic, ne, port]]'''
        return None

    @abstractmethod
    def get_cmd_master_ptp_set(self, master_dic):
        '''返回值类型为[[cmd, dic, ne, port]]'''
        pass

    @abstractmethod
    def get_cmd_slave_ptp_set(self, slave_dic):
        '''返回值类型为[[cmd, dic, ne, port]]'''
        pass

    def __get_if_mode_expect_and_cmd(self, mode):
        if mode == 'uni':
            if_expect_mod = 'eth-l2-if'
            chmode_cmd = self.master_cmd_list.interface_switchport()
            resumemode_cmd = self.master_cmd_list.interface_no_switchport()
        else:
            if_expect_mod = 'eth-l3-if'
            chmode_cmd = self.master_cmd_list.interface_no_switchport()
            resumemode_cmd = self.master_cmd_list.interface_switchport()
        return if_expect_mod, chmode_cmd, resumemode_cmd


    @log_func_name()
    def _change_interface_mode(self, mode):
        errornum = 0
        if_expect_mod, chmode_cmd, resumemode_cmd = self.__get_if_mode_expect_and_cmd(mode)
        for master_dic, slave_dic in self.param_dic:
            cmd_list = self.master_cmd_list.enter_configure_terminal() + self.master_cmd_list.enter_ethernet_interface(self.master_if)
            rtn_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(cmd_list, master_dic), self.get_ne_ip(self.master_ne), 0, CLI_PORT)
            ret_str = self.tnxxx.send_rtn_str("?", self.get_ne_ip(self.master_ne), 0, CLI_PORT)
            if if_expect_mod not in ret_str:
                self.__master_need_to_resume.append(True)
                ret_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(chmode_cmd, master_dic), self.get_ne_ip(self.master_ne), 0, CLI_PORT)
            else:
                self.__master_need_to_resume.append(False)
            rtn_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(self.master_cmd_list.exit(2), master_dic), self.get_ne_ip(self.master_ne), 0, CLI_PORT)

            cmd_list = self.slave_cmd_list.enter_configure_terminal() + self.slave_cmd_list.enter_ethernet_interface(self.slave_if)
            rtn_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(cmd_list, slave_dic), self.get_ne_ip(self.slave_ne), 0, CLI_PORT)
            ret_str = self.tnxxx.send_rtn_str("?", self.get_ne_ip(self.slave_ne), 0, CLI_PORT)
            if if_expect_mod not in ret_str:
                self.__slave_need_to_resume.append(True)
                ret_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(chmode_cmd, slave_dic), self.get_ne_ip(self.slave_ne), 0, CLI_PORT)
            else:
                self.__slave_need_to_resume.append(False)
            rtn_str = self.tnxxx.send_rtn_str(self.get_parse_cmd_str(self.slave_cmd_list.exit(2), slave_dic),
                                              self.get_ne_ip(self.slave_ne), 0, CLI_PORT)
        return errornum

    @log_func_name()
    def _change_interface_mode_resume(self, mode):
        errornum = 0
        if len(self.__master_need_to_resume)>0 and len(self.__slave_need_to_resume)>0:
            if_expect_mod, chmode_cmd, resumemode_cmd = self.__get_if_mode_expect_and_cmd(mode)
            for (master_dic, slave_dic), master_need_to_resume, slave_need_to_resume in zip(self.param_dic, self.__master_need_to_resume, self.__slave_need_to_resume):
                if master_need_to_resume:
                    cmd_info_list = [
                        [self.master_cmd_list.enter_configure_terminal()
                            + self.master_cmd_list.enter_ethernet_interface(self.master_if)
                            + resumemode_cmd
                            + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                        # [self.master_cmd_list.enter_ethernet_interface(self.master_if), master_dic, self.master_ne, CLI_PORT],
                        # [resumemode_cmd, master_dic, self.master_ne, CLI_PORT],
                        # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
                    ]
                    if not self.run(cmd_info_list): errornum += 1
                if slave_need_to_resume:
                    cmd_info_list = [
                        [self.slave_cmd_list.enter_configure_terminal()
                            + self.slave_cmd_list.enter_ethernet_interface(self.slave_if)
                            + resumemode_cmd
                            + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                        # [self.slave_cmd_list.enter_ethernet_interface(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
                        # [resumemode_cmd, slave_dic, self.slave_ne, CLI_PORT],
                        # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
                    ]
                    if not self.run(cmd_info_list): errornum += 1
        return errornum

    @abstractmethod
    def change_interface_mode(self):
        '''调用_change_interface_mode(self, mode)实现'''
        return 0

    @abstractmethod
    def change_interface_mode_resume(self):
        '''调用_change_interface_mode_resume(self, mode)实现'''
        return 0

    @log_func_name()
    def add_cfg(self):
        errornum = self.change_interface_mode()

        for master_dic, slave_dic in self.param_dic:
            cmd_info_list = []
            cmd_set_ip = self.get_cmd_master_ip_set(master_dic)
            if cmd_set_ip:
                cmd_info_list.extend(cmd_set_ip)
            cmd_ptp_set = self.get_cmd_master_ptp_set(master_dic)
            if cmd_ptp_set:
                cmd_info_list.extend(cmd_ptp_set)
            cmd_info_list.extend([
                [self.master_cmd_list.enter_configure_terminal()
                    + self.master_clk_cmd_list.enter_clk_terminal()
                    + self.master_clk_cmd_list.set_ssmmode('on')
                    + self.master_clk_cmd_list.set_freerunlevel('ssua')
                    + self.master_clk_cmd_list.exit(1)
                    + self.master_cmd_list.enter_ptp_terminal()
                    + self.master_cmd_list.set_ptp_cmm_to_master()
                    + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.enter_clk_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.set_ssmmode('on'), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.set_freerunlevel('ssua'), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.exit(1), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.set_ptp_cmm_to_master(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
            ])
            cmd_set_ip = self.get_cmd_slave_ip_set(slave_dic)
            if cmd_set_ip:
                cmd_info_list.extend(cmd_set_ip)
            cmd_ptp_set = self.get_cmd_slave_ptp_set(slave_dic)
            if cmd_ptp_set:
                cmd_info_list.extend(cmd_ptp_set)
            cmd_info_list.extend([
                [self.slave_cmd_list.enter_configure_terminal()
                    + self.slave_clk_cmd_list.enter_clk_terminal()
                    + self.slave_clk_cmd_list.set_ssmmode('on')
                    + self.slave_clk_cmd_list.set_scs_wtrtime(0)
                    + self.slave_clk_cmd_list.set_scs_priority(self.slave_if)
                    + self.slave_clk_cmd_list.exit(1)
                    + self.slave_cmd_list.enter_ptp_terminal()
                    + self.slave_cmd_list.set_ptp_cmm_to_slave()
                    + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.enter_clk_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.set_ssmmode('on'), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.set_scs_wtrtime(0), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.set_scs_priority(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.exit(1), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.set_ptp_cmm_to_slave(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
            ])

            if not self.run(cmd_info_list) : errornum += 1

        return errornum

    def change_to_twostep(self):
        errornum  = 0
        for master_dic, slave_dic in self.param_dic:
            cmd_info_list = [
                [self.master_cmd_list.enter_configure_terminal()
                    + self.master_cmd_list.enter_ptp_terminal()
                    + self.master_cmd_list.set_ptp_twostep(self.master_if)
                    + self.master_cmd_list.exit(2), master_dic, self.master_ne,CLI_PORT],
                # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne,CLI_PORT],
                # [self.master_cmd_list.set_ptp_twostep(self.master_if), master_dic,self.master_ne, CLI_PORT],
                # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                [self.slave_cmd_list.enter_configure_terminal()
                    + self.slave_cmd_list.enter_ptp_terminal()
                    + self.slave_cmd_list.set_ptp_twostep(self.slave_if)
                    + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne,CLI_PORT],
                # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne,CLI_PORT],
                # [self.slave_cmd_list.set_ptp_twostep(self.slave_if), slave_dic,self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
            ]
            if not self.run(cmd_info_list): errornum += 1
        return errornum

    @log_func_name()
    def add_cfg_check(self):
        errornum = 0

        for master_dic, slave_dic in self.param_dic:
            cmd_info_list = [
                [self.master_cmd_list.enter_configure_terminal()
                    + self.master_clk_cmd_list.enter_clk_terminal()
                    + self.master_clk_cmd_list.show_config('ssua', 'on')
                    + self.master_clk_cmd_list.exit(1)
                    + self.master_cmd_list.enter_ptp_terminal()
                    + self.master_cmd_list.get_ptp_port_cfg(self.master_if)
                    + self.master_cmd_list.get_ptp_cmm_to_master_check()
                    + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.enter_clk_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.show_config('ssua', 'on'), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.exit(1), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.get_ptp_port_cfg(self.master_if), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.get_ptp_cmm_to_master_check(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                [self.slave_cmd_list.enter_configure_terminal()
                    + self.slave_clk_cmd_list.enter_clk_terminal()
                    + self.slave_clk_cmd_list.show_config(None, 'on')
                    + self.slave_clk_cmd_list.show_statinfo_workmode(self.slave_if)
                    + self.slave_clk_cmd_list.exit(1)
                    + self.slave_cmd_list.enter_ptp_terminal()
                    + self.slave_cmd_list.get_ptp_port_cfg(self.slave_if)
                    + self.slave_cmd_list.get_ptp_cmm_to_slave_check()
                    + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.enter_clk_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.show_config(None, 'on'), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.show_statinfo_workmode(self.slave_if), slave_dic, self.slave_ne, CLI_PORT, '', 2, 150],
                # [self.slave_clk_cmd_list.exit(1), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.get_ptp_port_cfg(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.get_ptp_cmm_to_slave_check(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
            ]
            if not self.run(cmd_info_list) : errornum += 1

        return errornum


    @log_func_name()
    def del_cfg(self):
        errornum = 0

        for master_dic, slave_dic in self.param_dic:
            cmd_info_list = [
                [self.master_cmd_list.enter_configure_terminal()
                    + self.master_cmd_list.enter_ptp_terminal()
                    + self.master_cmd_list.no_ptp_port(self.master_if)
                    + self.master_cmd_list.exit(1)
                    + self.master_clk_cmd_list.enter_clk_terminal()
                    + self.master_clk_cmd_list.set_ssmmode('off')
                    + self.master_clk_cmd_list.set_freerunlevel('sec')
                    + self.master_clk_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.no_ptp_port(self.master_if), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.exit(1), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.enter_clk_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.set_ssmmode('off'), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.set_freerunlevel('sec'), master_dic, self.master_ne, CLI_PORT],
                # [self.master_clk_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT]
            ]
            cmd_ip_no = self.get_cmd_master_ip_no(master_dic)
            if cmd_ip_no:
                cmd_info_list.extend(cmd_ip_no)
            cmd_info_list.extend([
                [self.slave_cmd_list.enter_configure_terminal()
                    + self.slave_cmd_list.enter_ptp_terminal()
                    + self.slave_cmd_list.no_ptp_port(self.slave_if)
                    + self.slave_cmd_list.exit(1)
                    + self.slave_clk_cmd_list.enter_clk_terminal()
                    + self.slave_clk_cmd_list.set_ssmmode('off')
                    + self.slave_clk_cmd_list.set_scs_wtrtime(5)
                    + self.slave_clk_cmd_list.no_scs_priority(self.slave_if)
                    + self.slave_clk_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.no_ptp_port(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.exit(1), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.enter_clk_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.set_ssmmode('off'), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.set_scs_wtrtime(5), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.no_scs_priority(self.slave_if), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_clk_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
            ])
            cmd_ip_no = self.get_cmd_slave_ip_no(slave_dic)
            if cmd_ip_no:
                cmd_info_list.extend(cmd_ip_no)
            if not self.run(cmd_info_list) : errornum += 1

        errornum += self.change_interface_mode_resume()

        return errornum

    @log_func_name()
    def check_cfg(self):
        errornum = 0
        for master_dic, slave_dic in self.param_dic:
            slave_slot = int(re.split("/", self.get_parse_cmd_str([self.slave_if], slave_dic))[0])
            slave_port = self.get_effective_cmd_port(self.slave_ne, slave_slot)
            cfg_info_list = [
                [self.master_cmd_list.enter_configure_terminal()
                    + self.master_cmd_list.enter_ptp_terminal()
                    + self.master_cmd_list.get_ptp_port_state(self.master_if, 'PortState:Master')
                    + self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
                # [self.master_cmd_list.get_ptp_port_state(self.master_if, 'PortState:Master'), master_dic, self.master_ne, CLI_PORT, '', 2, 20], #检查是否变成master
                # [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                [self.slave_cmd_list.check_ptp_ssmvalue(4), slave_dic, self.slave_ne, slave_port, '', 2, 20],   #检查clk是否lock上
                [self.slave_cmd_list.enter_configure_terminal()
                    + self.slave_cmd_list.enter_ptp_terminal()
                    + self.slave_cmd_list.get_ptp_port_state(self.slave_if, 'PortState:Slave')
                    + self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                # [self.slave_cmd_list.get_ptp_port_state(self.slave_if, 'PortState:Slave'), slave_dic, self.slave_ne, CLI_PORT, '', 2, 20], #检查是否变成slave
                # [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT],
                [self.slave_cmd_list.get_filteredOffs(), slave_dic, self.slave_ne, slave_port, '', 2, 20],      #检查offset是否收敛
                [self.slave_cmd_list.get_offset_segment(), slave_dic, self.slave_ne, slave_port],
            ]

            if not self.run(cfg_info_list): errornum += 1

        return errornum


    def get_effective_cmd_port(self, ne, slot):
        if (self.get_ne_type(ne) == "SPN805S"):
            effective_cmd_port = MTN_PORT
        elif (self.get_ne_type(ne) == "SPN808"):
            effective_cmd_port = [slot, MTN_PORT]
        else:
            effective_cmd_port = [slot, DEV_PORT]

        return effective_cmd_port

    def _execute(self):
        errornum = self.call_action_fun(self.__action)

        #返回case运行结果
        if errornum != 0 :
            return False
        else:
            return True



