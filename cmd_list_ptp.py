#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/15 11:19
# @Author  : Jiang Bo
# @Site    : 
# @File    : cmd_list_ptp.py
# @Software: PyCharm

from cmd_list_base import *

def check_filteredOffs(ret_str, parm):
    type = parm[0]
    threshold = parm[1]
    if(type in ("SPN805S", "SPN808")):
        findStr = r'The value is (-?\d+\.?\d*)'
    else:
        findStr = r'value = (-?\d+\.?\d*)'
    diffoffset = re.findall(findStr, ret_str)
    if (len(diffoffset) == 1 and abs(float(diffoffset[0]) / 65536) < threshold):
        ret = True
    else:
        ret = False
    return ret

def check_offset_segment(ret_str, threshold):
    ret = True
    diffoffset = re.findall(r'(?<=diffoffset = )-?\d+\.?\d*', ret_str)
    maxoffset = re.findall(r'(?<=maxoffset = )-?\d+\.?\d*', ret_str)
    minoffset = re.findall(r'(?<=minoffset = )-?\d+\.?\d*', ret_str)
    if not (len(diffoffset) == 1 and (abs(float(diffoffset[0])) * 1000000000) < (threshold * 2)):
        print('offset过大 diffoffset:' + str(diffoffset))
        ret = False
    if not (len(maxoffset) == 1 and (abs(float(maxoffset[0])) * 1000000000) < threshold):
        print('offset过大 maxoffset:' + str(maxoffset))
        ret = False
    if not (len(minoffset) == 1 and (abs(float(minoffset[0])) * 1000000000) < threshold):
        print('offset过大 minoffset:' + str(minoffset))
        ret = False

    return ret

class cmd_list_ptp(cmd_list_base) :

    def enter_ptp_terminal(self):
        cmd_list = [
            "ptp"
        ]

        return cmd_list


    def set_ptp_port_mc(self, interface_name):
        cmd_list = [
            "set interface " + interface_name + " porttype mc txframetype l2 enable true anncintv -3 syncintv -4 delayreqintv -4 steptype onestep"
        ]
        return cmd_list

    def set_ptp_port_uc(self, interface_name, next_ip):
        cmd_list = [
            "set interface " + interface_name + " porttype uc txframetype l3 ucmstip " + next_ip + " encapmode l3port enable true anncintv -3 syncintv -4 delayreqintv -4 steptype onestep"
        ]
        return cmd_list

    def no_ptp_port(self, interface_name):
        cmd_list = [
            "no interface " + interface_name
        ]

        return cmd_list

    def get_ptp_port_state(self, interface_name=None, check=None):
        '''check可以传递为字符串（判断命令的执行结果是否有check），或者不带参数的回调函数func，或者带参数的回调函数[func, param],回调函数的形式为fun(ret_str, param)'''
        if check:
            if interface_name:
                cmd_list = [
                    ["show portstat interface " + interface_name, check]   #添加一个两个元素的list，后面的是需要验证的内容
                ]
            else:
                cmd_list = [
                    ["show portstatall", check]
                ]
        else:
            if interface_name:
                cmd_list = [
                    ["show portstat interface " + interface_name, "Port:" + interface_name]   #添加一个两个元素的list，后面的是需要验证的内容
                ]
            else:
                cmd_list = [
                    "show portstatall"
                ]

        return cmd_list

    def get_ptp_port_cfg(self, interface_name):
        cmd_list = [
            ["show portcfg interface " + interface_name, "Port:" + interface_name]  #添加一个两个元素的list，后面的是需要验证的内容
        ]

        return cmd_list

    def set_ptpipaddr(self, ip_mask):
        cmd_list = [
            'set ptpipaddr ' + ip_mask + ' mode port'
        ]

        return cmd_list

    def no_ptpipaddr(self, ip):
        cmd_list = [
            'no ptpipaddr ' + ip
        ]

        return cmd_list

    def set_ptp_cmm_to_master(self):
        cmd_list = [
            'set cmmconfig clockclass 6 priority1 1 priority2 1'
        ]
        return cmd_list


    def set_ptp_cmm_to_slave(self):
        cmd_list = [
            'set cmmconfig clockclass 248 priority1 128 priority2 128'
        ]
        return cmd_list

    def get_ptp_cmm_to_master_check(self):
        cmd_list = [
            [
                'show cmmconfig',
                [re_check_ret_str_callback, 'ClockClass:6[a-zA-Z0-9:\r\n]+Priority1:1[\r\n]+Priority2:1']
             ]
        ]
        return cmd_list

    def get_ptp_cmm_to_slave_check(self):
        cmd_list = [
            [
                'show cmmconfig',
                [re_check_ret_str_callback, 'ClockClass:248[a-zA-Z0-9:\r\n]+Priority1:128[\r\n]+Priority2:128']
             ]
        ]
        return cmd_list

    def set_ptp_domainnumber(self, interface_name, domain_num):
        cmd_list = [
            'set interface ' + interface_name + ' domainnumber ' + str(domain_num)
        ]
        return cmd_list

    def set_ptp_twostep(self, interface_name):
        cmd_list = [
            'set interface ' + interface_name + ' steptype twostep enable false',
            'set interface ' + interface_name + ' enable true'
        ]
        return cmd_list

    def check_ptp_ssmvalue(self, ssm_value):
        if (self.type in ("SPN805S", "SPN808")):
            cmd_list = [
                [
                    'necli.0.CmdEx "DbgCmdEx",{{String,"print_data_val(\'g_Ptp_SSMValue\',1)"}}',
                    'The value is ' + str(ssm_value)
                ]
            ]
        else:
            cmd_list = [
                [
                    '(char)g_Ptp_SSMValue',
                    'value = ' + str(ssm_value) + ' '
                ]
            ]
        return cmd_list


    def get_filteredOffs(self, threshold = 200):
        '''
        检验offset的值
        :param threshold: offset的门限值，单位纳秒
        :return:
        '''
        if(self.type in ("SPN805S", "SPN808")):
            cmd_list = [
                [
                    'necli.0.CmdEx "DbgCmdEx",{{String,"print_data_val(\'filteredOffs\',8)"}}',
                    [check_filteredOffs, (self.type,threshold)]
                ]
            ]
        else:
            cmd_list = [
                [
                    '(long long)filteredOffs',
                    [check_filteredOffs, (self.type,threshold)]
                ]
            ]
        return cmd_list

    def get_offset_segment(self, threshold = 200):
        if (self.type in ("SPN805S", "SPN808")):
            cmd_list = [
                ['necli.0.CmdEx "DbgCmdEx",{{String,"PtpBeginOffsetStatic()"}}', '', 20],
                ['necli.0.CmdEx "DbgCmdEx",{{String,"PtpEndOffsetStatic()"}}', [check_offset_segment, threshold]]
            ]
        else:
            cmd_list = [
                ['PtpBeginOffsetStatic','', 20],
                ['PtpEndOffsetStatic', [check_offset_segment, threshold]]
            ]
        return cmd_list

