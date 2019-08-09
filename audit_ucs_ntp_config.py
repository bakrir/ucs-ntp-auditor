#!/usr/bin/env python

from ucsmsdk.ucshandle import UcsHandle
from ucsmsdk.mometa.aaa.AaaUserEp import AaaUserEp
import getpass
from tabulate import tabulate
from datetime import datetime
from IPython.display import clear_output
import os
import ipaddress
import platform

ucs_ip = input('ucs system (or all): ')
ucs_username= input("username: ")
user_passwd = getpass.getpass("passowrd: ")
table_output=input("provide table output format (pipe, jira, simple): ")

ucs_list = []

if ucs_ip.lower() == 'all':
    from ucs_list import ucs_list
    ucs_list = ucs_list
else:
    ucs_list.append(ucs_ip)

def get_ucs_ntp_settings(ucs_list, ucs_username, user_passwd):
    timestamps_all=[]

    for ucs in ucs_list:
        handle =  UcsHandle(ip=ucs, username=ucs_username, password=user_passwd)
        handle.login()

        mo_dn = handle.query_dn("sys")
        ucs_current_time=mo_dn.current_time
        utc_current_time=datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f1')
        utc_current_time = utc_current_time[:-4]

        t1 = datetime.strptime(ucs_current_time, "%Y-%m-%dT%H:%M:%S.%f")
        t2 = datetime.strptime(utc_current_time, "%Y-%m-%dT%H:%M:%S.%f")

        diff = t1 - t2

        ntp_dn = handle.query_classid("commNtpProvider")
        mgmt_ip_a = handle.query_dn("sys/switch-A")

        fi_ip = mgmt_ip_a.oob_if_ip
        netmask = mgmt_ip_a.oob_if_mask

        if len(ntp_dn) > 0:
            ntp_servers = [ n.name for n in ntp_dn ]
            network=ipaddress.ip_network('{}/{}'.format(fi_ip,netmask),strict=False)
            correct_ntp=ipaddress.ip_address(ntp_servers[0]) in ipaddress.ip_network(network)
        else:
            ntp_servers = ['no ntp']



        # create temp list to add to a list of lists
        timestamp_per_site = []
        timestamp_per_site.extend([handle.ip,
                                   utc_current_time,
                                   ucs_current_time,
                                   abs(diff.total_seconds()),
                                   ntp_servers[0],
                                   correct_ntp])
        timestamps_all.append(timestamp_per_site)

        print("=> logged out of {}".format(handle.ip))
        handle.logout()

    clear_output()
    if platform.system() != ('Windows'):
        os.system('clear')
    else:
        os.system( 'cls' )
    
    headers=['site', 'utc timestamp', 'ucs timestamp', 'offset', 'ntp server', 'correct']
    
    print(tabulate(timestamps_all, headers=headers, tablefmt=table_output))

if __name__ == "__main__":
    get_ucs_ntp_settings(ucs_list, ucs_username, user_passwd)