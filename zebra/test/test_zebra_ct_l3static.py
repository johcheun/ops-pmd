#!/usr/bin/python

# Copyright (C) 2015 Hewlett Packard Enterprise Development LP
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from halonvsi.docker import *
from halonvsi.halon import *
from halonutils.halonutil import *

class staticRouteConfigTest( HalonTest ):

    def setupNet(self):
        self.net = Mininet(topo=SingleSwitchTopo(k=0,
                                                 hopts=self.getHostOpts(),
                                                 sopts=self.getSwitchOpts()),
                                                 switch=HalonSwitch,
                                                 host=HalonHost,
                                                 link=HalonLink, controller=None,
                                                 build=True)

    def test_ipv4(self):
        info('\n########## Test  to verify IPv4 static routes ##########\n')
        s1 = self.net.switches[ 0 ]
        intf_check = 0

        s1.cmdCLI("configure terminal")
        s1.cmdCLI("interface 1")
        s1.cmdCLI("ip address 192.168.1.1/24")
        s1.cmdCLI("exit")
        s1.cmdCLI("interface 2")
        s1.cmdCLI("ip address 192.168.2.1/24")
        s1.cmdCLI("exit")

        info('### Verify ip route configuration with nexthop address ###\n')
        s1.cmdCLI("ip route 192.168.3.1/24 192.168.2.2 2")
        ret = s1.cmdCLI("do show ip route")

        if '192.168.3.1/24' in ret and '192.168.2.2' in ret and 'static' in ret and '[2/0]' in ret:
            info('### IP route configuration passed ###\n')
        else:
            assert 0, ('IP route configuration failed')

        info('### Verify deletion of ip route with nexthop address ###\n')
        s1.cmdCLI("no ip route 192.168.3.1/24 192.168.2.2 2")
        ret = s1.cmdCLI("do show ip route")

        if 'No ip routes configured' in ret:
            info('### Deletion of ip route passed ###\n')
        else:
            assert 0, ('Deletion of ip route failed')

        info('### Verify prefix format ###\n')
        s1.cmdCLI("ip route 192.168.3.1 192.168.2.2 2")
        ret = s1.cmdCLI("do show ip route")

        if 'No ip routes configured' in ret:
            info('### Prefix format verification passed ###\n\n')
        else:
            assert 0, ('Prefix format verification failed')

        info('### Verify ip route configuration with nexthop interface ###\n')
        s1.cmdCLI("ip route 192.168.3.1/24 2 2")
        ret = s1.cmdCLI("do show ip route")

        for index, word in enumerate(ret.split(" ")):
            if index == 13 and word == '2,':
                intf_check = 1

        if intf_check == 1:
            info('### IP route configuration passed ###\n\n')
        else:
            assert 0, ('IP route configuration failed')

        info('### Verify deletion of ip route with nexthop interface ###\n')
        s1.cmdCLI("no ip route 192.168.3.1/24 2 2")
        ret = s1.cmdCLI("do show ip route")

        if 'No ip routes configured' in ret:
            info('### Deletion of ip routes passed ###\n\n')
        else:
            assert 0, ('Deletion of ip routes failed')

        info('### Verify setting of default distance ###\n')
        s1.cmdCLI("ip route 192.168.3.1/24 192.168.2.2")
        ret = s1.cmdCLI("do show ip route")

        for index, word in enumerate(ret.split(" ")):
            if index == 15 and word == '[1/0]':
                intf_check = 1

        if intf_check == 1:
            info('### Default distance verification success ###\n\n')
        else:
            assert 0, ('Default distance verification failed')

    def test_ipv6(self):
        info('\n########## Test  to verify IPv6 static routes ##########\n')
        s1 = self.net.switches[ 0 ]
        intf_check = 0

        s1.cmdCLI("configure terminal")
        s1.cmdCLI("interface 1")
        s1.cmdCLI("ipv6 address 2000::1/120")
        s1.cmdCLI("exit")
        s1.cmdCLI("interface 2")
        s1.cmdCLI("ipv6 address 2001::1/120")
        s1.cmdCLI("exit")

        info('### Verify ip route configuration with nexthop address ###\n')
        s1.cmdCLI("ipv6 route 2002::1/120 2001::2 2")
        ret = s1.cmdCLI("do show ipv6 route")

        if '2002::1/120' in ret and '2001::2' in ret and 'static' in ret and '[2/0]' in ret:
            info('### IPv6 route configuration passed ###\n')
        else:
            assert 0, ('IPv6 route configuration failed')

        info('### Verify deletion of ipv6 route ###\n')
        s1.cmdCLI("no ipv6 route 2002::1/120 2001::2 2")
        ret = s1.cmdCLI("do show ipv6 route")

        if 'No ipv6 routes configured' in ret:
            info('### Deletion of ipv6 route passed ###\n')
        else:
            assert 0, ('Deletion of ipv6 route failed')

        info('### Verify prefix format ###\n')
        s1.cmdCLI("ipv6 route 2002::1 2001::2 2")
        ret = s1.cmdCLI("do show ipv6 route")

        if 'No ipv6 routes configured' in ret:
            info('### Prefix format verification passed ###\n\n')
        else:
            assert 0, ('Prefix format verification failed')

        info('### Verify ipv6 route configuration with nexthop interface ###\n')
        s1.cmdCLI("ipv6 route 2002::1/120 2 2")
        ret = s1.cmdCLI("do show ipv6 route")

        for index, word in enumerate(ret.split(" ")):
            if index == 13 and word == '2,':
                intf_check = 1

        if intf_check == 1:
            info('### IPv6 route configuration passed ###\n\n')
        else:
            assert 0, ('IPv6 route configuration failed')

        info('### Verify deletion of ipv6 route with nexthop interface ###\n')
        s1.cmdCLI("no ipv6 route 2002::1/120 2 2")
        ret = s1.cmdCLI("do show ipv6 route")

        if 'No ipv6 routes configured' in ret:
            info('### Deletion of ipv6 routes passed ###\n\n')
        else:
            assert 0, ('Deletion of ipv6 routes failed')

        info('### Verify setting of default distance ###\n')
        s1.cmdCLI("ipv6 route 1001:2001::1/64 1001:3001::3")
        ret = s1.cmdCLI("do show ipv6 route")

        for index, word in enumerate(ret.split(" ")):
            if index == 15 and word == '[1/0]':
                intf_check = 1

        if intf_check == 1:
            info('### Default distance verification success ###\n\n')
        else:
            assert 0, ('Default distance verification failed')

    def test_show_running_config(self):
        info("\n=====================================================================\n")
        info("*** Tests To Verify 'show running-config' for IPv4 and IPv6 Static Routes")
        info("\n=====================================================================\n")
        s1 = self.net.switches[ 0 ]
        intf_check = 0
        clilist = []

        s1.cmdCLI("configure terminal")
        info('\n***Adding Ipv4 Routes\n')
        info('*** CMD: ip route 10.10.10.10/8 20.20.20.20 ***\n')
        s1.cmdCLI("ip route 10.10.10.10/8 20.20.20.20")
        clilist.append('ip route 10.10.10.10/8 20.20.20.20')
        info('*** CMD: ip route 30.30.30.30/8 40.40.40.40 15 ***\n')
        s1.cmdCLI("ip route 30.30.30.30/8 40.40.40.40 15")
        clilist.append('ip route 30.30.30.30/8 40.40.40.40 15')
        s1.cmdCLI("interface 25")
        s1.cmdCLI("vrf attach vrf_default")
        s1.cmdCLI("ip address 50.50.50.60")
        s1.cmdCLI("exit")
        info('*** CMD: ip route 50.50.50.50/8 25***\n')
        s1.cmdCLI("ip route 50.50.50.50/8 25")
        clilist.append('ip route 50.50.50.50/8 25')
        s1.cmdCLI("interface 26")
        s1.cmdCLI("vrf attach vrf_default")
        s1.cmdCLI("ip address 60.60.60.70")
        s1.cmdCLI("exit")
        info('*** CMD: ip route 60.60.60.60/8 26 26***\n')
        s1.cmdCLI("ip route 60.60.60.60/8 26 26")
        clilist.append('ip route 60.60.60.60/8 26 26')

        info('\n***Adding Ipv6 Routes\n')
        info('*** CMD: ipv6 route 2001::1/120  2001::2***\n')
        s1.cmdCLI("ipv6 route 2001::1/120 2001::2")
        clilist.append('ipv6 route 2001::1/120 2001::2')
        info('*** CMD: ipv6 route 2002::1/120  2002::2 12 ***\n')
        s1.cmdCLI("ipv6 route 2002::1/120 2002::2 12")
        clilist.append('ipv6 route 2002::1/120 2002::2 12')
        s1.cmdCLI("interface 13")
        s1.cmdCLI("vrf attach vrf_default")
        s1.cmdCLI("ipv6 address 2003::2")
        s1.cmdCLI("exit")
        info('*** CMD: ipv6 route 2003::1/120 13  ***\n')
        s1.cmdCLI("ipv6 route 2003::1/120 13")
        clilist.append('ipv6 route 2003::1/120 13')
        s1.cmdCLI("interface 14")
        s1.cmdCLI("vrf attach vrf_default")
        s1.cmdCLI("ip address 2004::2")
        s1.cmdCLI("exit")
        info('*** CMD: ipv6 route 2004::1/120 14 14  ***\n')
        s1.cmdCLI("ipv6 route 2004::1/120 14 14")
        clilist.append('ipv6 route 2004::1/120 14 14')

        out = s1.cmdCLI("do show running-config")
        lines = out.split('\n')
        found = 0
        for line in lines:
            if line in clilist:
                found = found + 1

        if found == 8:
            print "\n****** show running-config succss ******\n"
            return True
        else:
            assert 0, "\nERROR: show running-config command failure"

class Test_vtysh_static_routes_ct:

    def setup_class(cls):
        Test_vtysh_static_routes_ct.test = staticRouteConfigTest()

    def teardown_class(cls):
        Test_vtysh_static_routes_ct.test.net.stop()

    def test_ipv4(self):
        self.test.test_ipv4()

    def test_ipv6(self):
        self.test.test_ipv6()

    def test_show_running_config(self):
        self.test.test_show_running_config()
        #CLI(self.test.net)

    def __del__(self):
        del self.test
