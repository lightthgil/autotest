#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/11 10:12
# @Author  : Jiang Bo
# @Site    : 
# @File    : case_1588_ge_uni_l3uc_e2e_onstep_domain.py
# @Software: PyCharm

from case_1588_ge_uni_l3uc_e2e_onestep import *

class TestCaseDomain (TestCase) :
    @log_func_name()
    def chang_domain(self, master_domain_num, slave_domain_num):
        errornum = 0
        for master_dic, slave_dic in self.param_dic:
            cmd_info_list = [
                [self.master_cmd_list.enter_configure_terminal(), master_dic, self.master_ne, CLI_PORT],
                [self.master_cmd_list.enter_ptp_terminal(), master_dic, self.master_ne, CLI_PORT],
                [self.master_cmd_list.set_ptp_domainnumber(self.master_if, master_domain_num), master_dic, self.master_ne, CLI_PORT],
                [self.master_cmd_list.exit(2), master_dic, self.master_ne, CLI_PORT],
                [self.slave_cmd_list.enter_configure_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                [self.slave_cmd_list.enter_ptp_terminal(), slave_dic, self.slave_ne, CLI_PORT],
                [self.slave_cmd_list.set_ptp_domainnumber(self.slave_if, slave_domain_num), slave_dic, self.slave_ne, CLI_PORT],
                [self.slave_cmd_list.exit(2), slave_dic, self.slave_ne, CLI_PORT]
            ]
            if not self.run(cmd_info_list): errornum += 1
        return errornum

    @log_func_name()
    def check_cfg(self):
        errornum = super(TestCaseDomain, self).check_cfg()
        errornum += self.chang_domain(10, 20)
        if 0 == super(TestCaseDomain, self).check_cfg():
            errornum += 1
        errornum += self.chang_domain(30, 30)
        errornum += super(TestCaseDomain, self).check_cfg()

        return errornum

if __name__ == "__main__" :
    case = TestCaseDomain('ne1', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP', 'ne2', "PTP_INTERFACE_GE", 'PTP_GE_L3_IP', 'PTP_GE_L3_NEXT_IP')
    # case.init_redirection()
    case.execute()
