#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/15 11:35
# @Author  : Jiang Bo
# @Site    : ${SITE}
# @File    : test_cmd_list_ptp.py
from unittest import TestCase
from cmd_list_ptp import cmd_list_ptp


# @Software: PyCharm
class TestCmd_list_1588(TestCase):
    cmd_list_set = cmd_list_ptp("705E")

    def test_get_ptp_port_set(self):
        cmd_list = [
            "set interface PTP_INTERFACE_GE porttype mc txframetype l2 enable true anncintv -3 syncintv -4 delayreqintv -4 steptype onestep",
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.set_ptp_port_mc("PTP_INTERFACE_GE"))

    def test_get_ptp_port_no(self):
        cmd_list = [
            "no interface PTP_INTERFACE_GE",
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.no_ptp_port("PTP_INTERFACE_GE"))

    def test_get_ptp_port_state(self):
        cmd_list = [
            ['show portstat interface PTP_INTERFACE_GE', 'Port:PTP_INTERFACE_GE']
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.get_ptp_port_state("PTP_INTERFACE_GE"))
        cmd_list = [
            "show portstatall"
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.get_ptp_port_state())
        cmd_list = [
            ['show portstat interface PTP_INTERFACE_GE', 'PortState:Master']
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.get_ptp_port_state('PTP_INTERFACE_GE', 'PortState:Master'))
        cmd_list = [
            ['show portstat interface PTP_INTERFACE_GE', self.test_get_ptp_port_state]
        ]
        self.assertEqual(cmd_list,
                         self.cmd_list_set.get_ptp_port_state('PTP_INTERFACE_GE', self.test_get_ptp_port_state))

    def test_get_set_ptpipaddr(self):
        cmd_list = [
            "set ptpipaddr PTP_GE_L3_IP/24 mode port"
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.set_ptpipaddr("PTP_GE_L3_IP/24"))

    def test_get_ptp_port_uc_set(self):
        cmd_list = [
            "set interface PTP_INTERFACE_GE porttype uc txframetype l3 ucmstip PTP_GE_L3_NEXT_IP encapmode l3port enable true anncintv -3 syncintv -4 delayreqintv -4 steptype onestep"
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.set_ptp_port_uc("PTP_INTERFACE_GE", "PTP_GE_L3_NEXT_IP"))


    def test_get_no_ptpipaddr(self):
        cmd_list = [
            "no ptpipaddr PTP_GE_L3_IP"
        ]
        self.assertEqual(cmd_list, self.cmd_list_set.no_ptpipaddr("PTP_GE_L3_IP"))
