#!/bin/sh
sudo iptables -t nat -A POSTROUTING -o wlp6s0 -j MASQUERADE
sudo iptables -A FORWARD -i eno1 -o wlp6s0 -j ACCEPT
sudo iptables -A FORWARD -i wlp6s0 -o eno1 -m state --state RELATED,ESTABLISHED -j ACCEPT
