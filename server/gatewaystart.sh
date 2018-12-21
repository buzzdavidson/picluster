#!/bin/bash
# this script sets the local host up to act as an internet gateway for cluster members.
# because we don't typically want the cluster slaves to have internet access, this is provided
# to be run as needed.
#
# note: these changes are not permanent!  they will be reset on the next system reboot.
IFACE_INTERNAL=eno1
IFACE_EXTERNAL=wlp6s0

sudo iptables -t nat -A POSTROUTING -o $IFACE_EXTERNAL -j MASQUERADE
sudo iptables -A FORWARD -i $IFACE_INTERNAL -o $IFACE_EXTERNAL -j ACCEPT
sudo iptables -A FORWARD -i $IFACE_EXTERNAL -o $IFACE_INTERNAL -m state --state RELATED,ESTABLISHED -j ACCEPT
