#!/bin/bash

CIP="192.168.1.3,192.168.1.100"
SIP="192.168.1.2/24"

if [ $# -eq 2 ]
  then
  	IFACE=$1
  	IMAGE=$2
  else
    echo "Got $# arguments but expected 2. Usage is:
    $0 [IFACE] [IMAGE]
    Where IFACE is the wired network interface connected to the router (e.g. eth0 or enp0s25)
    And IMAGE is a recovery image as found on http://www.miwifi.com/miwifi_download.html"
    exit 1
fi

if [[ $(id -u) -ne 0 ]]; then
    echo "Please run this script as root"
    exit 1
fi

nmcli device set ${IFACE} managed no
ip addr add $SIP broadcast + dev ${IFACE}
# ip link set dev ${IFACE} up
echo "Starting dnsmasq with this configuration:"
echo -e "\
	interface=${IFACE}
	domain=unbrick.local
	dhcp-range=${CIP},2m
	dhcp-boot=${IMAGE}
	enable-tftp
	tftp-root=${PWD}" | tee /dev/stderr | dnsmasq -d -C -

ip addr delete $SIP dev enp0s25
nmcli device set ${IFACE} managed yes