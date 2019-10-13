#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/18 15:04
# @Author  : Jiang Bo
# @Site    : 
# @File    : cmd_list_base.py
# @Software: PyCharm

import re

def re_check_ret_str_callback(ret_str, find_str):
    result = bool(re.search(find_str, ret_str))

    if not result:
        print "ret_str: " + ret_str + '\n' + 'find_str: ' + find_str
    return result

class cmd_list_base :

    def __init__(self, type):
        self.type = type

    def get_cmd_str(self, cmd_list):
        cmd_str = ""
        for cmd_info in cmd_list:
            if issubclass(cmd_info.__class__, list):
                cmd_str = cmd_str + cmd_info[0] + "\n"
            else:
                cmd_str = cmd_str + cmd_info + "\n"

        return cmd_str

    def enter_configure_terminal(self):
        cmd_list = [
            "configure terminal",
        ]

        return cmd_list

    def exit(self, exit_num):
        cmd_list = [
        ]

        for i in range(exit_num):
            cmd_list.append("exit")

        return cmd_list

    def enter_ethernet_interface(self, interface_name):
        cmd_list = [
            'interface ethernet ' + interface_name
        ]

        return cmd_list

    def interface_switchport(self):
        cmd_list = [
            'switchport'
        ]

        return cmd_list

    def interface_no_switchport(self):
        cmd_list = [
            'no switchport'
        ]

        return cmd_list

    def set_ipaddr(self, ip_mask):
        cmd_list = [
            'set ipaddr ' + ip_mask
        ]
        return cmd_list

    def no_ipaddr(self, ip):
        cmd_list = [
            'no ipaddr ' + ip
        ]
        return cmd_list
