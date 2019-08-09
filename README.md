# ucs-ntp-auditor

## Overview

This script is used to collect ntp setting from a single UCS or all UCS systems in your environment. It will check the current time on the UCS and compare to the local UTC time and determine the offset. If you are using your gateway for NTP, this script will confirm that as well.

## Requirements

`pip install -R requirements.txt`

## Execution

This script can executed directly from the terminal as such:

```
./audit_ucs_ntp_config.py
```
**note**: make sure it is executable `chmod +x audit_ucs_ntp_config.py`

The script will prompt you select a single UCS or all UCS systems. If all is selected, it will use the `ucs_list.py` file. This list can be updated with additional systems if needed.

Example output:

```
$ ./audit_ucs_ntp_config.py
ucs system (or all): all
username: <username>
passowrd: <password>
provide table output format (pipe, jira, simple): pipe
=> logged out of ucs1
=> logged out of ucs2
=> logged out of ucs3
=> logged out of ucs4
=> logged out of ucs5

| site                  | utc timestamp           | ucs timestamp           |   offset | ntp server   | ntp correct  |
|:----------------------|:------------------------|:------------------------|---------:|:-------------|:-------------|
| ucs1                  | 2019-08-08T08:20:27.935 | 2019-08-08T08:20:18.195 |    9.74  | 10.1.1.1     | True         |
| ucs2                  | 2019-08-08T08:20:43.202 | 2019-08-08T08:20:35.615 |    7.587 | 10.1.2.1     | True         |
| ucs3                  | 2019-08-08T08:20:58.939 | 2019-08-08T08:07:09.714 |  829.225 | 10.1.3.1     | True         |
| ucs4                  | 2019-08-08T08:21:12.625 | 2019-08-08T08:21:08.012 |    4.613 | 10.1.4.1     | True         |
| ucs5                  | 2019-08-08T08:21:25.872 | 2019-08-08T08:21:22.820 |    3.052 | 10.1.5.1     | True         |
```
