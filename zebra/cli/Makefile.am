#
# (C) Copyright 2016 Hewlett Packard Enterprise Development LP
#
#  Licensed under the Apache License, Version 2.0 (the &quot;License&quot;); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an &quot;AS IS&quot; BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#
#  Process this file with Automake to create Makefile.in
#
#  File: Makefile.am

AM_CFLAGS =  ${OPSCLI_CFLAGS}
AM_CFLAGS += -I${top_srcdir}/include
AM_CFLAGS += -I$(LOCAL_SYSROOT_DIR)/usr/local/include/ovs -DOPS

libdir=${prefix}/lib/cli/plugins

lib_LTLIBRARIES = libl3routes_cli.la

libl3routes_cli_la_SOURCES = \
	l3routes_vty.c l3routes_vty.h vtysh_ovsdb_l3routes_context.c \
	vtysh_ovsdb_l3routes_context.h
libl3routes_cli_la_LDFLAGS = -avoid-version

install-exec-hook:
	@(cd $(DESTDIR)$(libdir) && $(RM) $(lib_LTLIBRARIES))
