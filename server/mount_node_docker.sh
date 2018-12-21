#!/bin/bash

MAC=`sed s/://g /sys/class/net/eth0/address`
MOUNTPOINT=/docker
REMOTEMOUNT=192.168.2.1:/data/nfs/hosts/${MAC}
DATADIR=${MOUNTPOINT}/${MAC}
DOCKERDIR=/var/lib/docker
LOCKFN=.flock_${MAC}
DATALOCK=${DATADIR}/${LOCKFN}
DOCKERLOCK=${DOCKERDIR}/${LOCKFN}

if [ -z ${MAC} ]; then
    echo "Unable to detetmine MAC address!"
    exit 10
fi

echo "Docker Swarm Startup Helper"
echo
echo "MAC address:            ${MAC}"
echo "Docker data dir:        ${DOCKERDIR}"
echo "Data dir for this node: ${DATADIR}"
echo
echo "Checking mount point at ${MOUNTPOINT}..."

if [ ! -d ${DATADIR} ]; then
    echo "Missing mount point at ${MOUNTPOINT}"
    if `mkdir -p ${DATADIR}`; then
	echo "Created mount point"
    else
	echo "Cannot create mount point at ${MOUNTPOINT}"
	exit 10
    fi
fi

echo "Checking data dir ${DATADIR}"
if `mount | grep -q ${DATADIR}`; then
    echo "Data dir is mounted already"
else
    echo "Data dir ${DATADIR} not found, attempting to mount..."
    if `mount ${REMOTEMOUNT} ${DATADIR}`; then
        echo "Successfully mounted ${DATADIR}"
    fi
fi

echo "Making sure data dir ${DATADIR} is writable..."
if `touch ${DATALOCK}`; then
    echo "Data dir is writable"
    rm ${DATALOCK}
else
    echo "Unable to touch file at ${DATADIR}!"
    exit 10
fi

echo "Checking bind mount..."
DOBIND=1
if [ -d ${DOCKERDIR} ]; then
    if [ -f ${DATALOCK} ]; then
	rm ${DATALOCK} > /dev/null 2>&1
    fi
    touch ${DATALOCK}
    if [ -f ${DOCKERLOCK} ]; then
	echo "Directory already bound"
	DOBIND=0
    else
	echo "Directory exists but is not bound"
    fi
    rm ${DATALOCK}
else
    echo "Directory doesnt exist"
fi

if [ ${DOBIND} == 1 ]; then
    echo "Binding directory"
    mount --bind ${DATADIR} ${DOCKERDIR}
    echo "Checking bind"
    if [ -d ${DOCKERDIR} ]; then
        if [ -f ${DATALOCK} ]; then
	    rm ${DATALOCK} > /dev/null 2>&1
        fi
        touch ${DATALOCK}
        if [ -f ${DOCKERLOCK} ]; then
	    echo "Bind looks OK"
	else
	    echo "Something bad happened!  Bind appears to be inactive"
	fi
    else
	echo "Something bad happened!  Directory is missing!"
    fi
    rm ${DATALOCK} > /dev/null 2>&1
fi



