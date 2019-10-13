#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/31 17:41
# @Author  : Jiang Bo
# @Site    : 
# @File    : cmd_list_clk.py
# @Software: PyCharm

from cmd_list_base import *

class cmd_list_clk(cmd_list_base) :
    def enter_clk_terminal(self):
        cmd_list = [
            "clk"
        ]
        return cmd_list

    def set_scs_wtrtime(self, time):
        cmd_list = [
            'set scs wtrtime ' + str(time)
        ]
        return cmd_list

    def set_scs_priority(self, interface):
        cmd_list = [
            'set scs priority ' + interface + ' 15'
        ]
        return cmd_list

    def no_scs_priority(self, interface):
        cmd_list = [
            'no scs priority ' + interface
        ]
        return cmd_list

    def show_statinfo_workmode(self, interface):
        cmd_list = [
            ['show statinfo workmode','work mode is:lock\r\nscs loced clock source is:'+interface]
        ]
        return cmd_list

    def set_freerunlevel(self, level):
        cmd_list = [
            'set freerunlevel ' + str(level)
        ]
        return cmd_list

    def set_ssmmode(self, swith):
        cmd_list = [
            'set ssmmode ' + swith
        ]
        return cmd_list

    def show_config(self, freerunLevel, ssmMode):
        check_str = ''
        if freerunLevel:
            check_str += 'FreerunLevel:' + freerunLevel + '\r\n'
        if ssmMode:
            check_str += 'SSMMode:' + ssmMode + '\r\n'
        if check_str == '':
            cmd_list = [
                'show config'
            ]
        else:
            cmd_list = [
            ['show config', check_str]
        ]
        return cmd_list

