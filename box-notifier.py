#!/usr/bin/python
#Box-notifier
#@author : naper
#tells you if a new client is connected to your router , designed for linux
#
#                   GNU LESSER GENERAL PUBLIC LICENSE
#                       Version 3, 29 June 2007
#
# Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
# Everyone is permitted to copy and distribute verbatim copies
# of this license document, but changing it is not allowed.
#
#
#  This version of the GNU Lesser General Public License incorporates
#the terms and conditions of version 3 of the GNU General Public
#License, supplemented by the additional permissions listed below.
#
#  0. Additional Definitions.
#
#  As used herein, "this License" refers to version 3 of the GNU Lesser
#General Public License, and the "GNU GPL" refers to version 3 of the GNU
#General Public License.
#
#  "The Library" refers to a covered work governed by this License,
#other than an Application or a Combined Work as defined below.
#
#  An "Application" is any work that makes use of an interface provided
#by the Library, but which is not otherwise based on the Library.
#Defining a subclass of a class defined by the Library is deemed a mode
#of using an interface provided by the Library.
#
#  A "Combined Work" is a work produced by combining or linking an
#Application with the Library.  The particular version of the Library
#with which the Combined Work was made is also called the "Linked
#Version".
#
import os
import os.path
import time
import socket
import fcntl
import struct
import argparse
import sys
from gi.repository import Notify

RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
YELLOW = "\033[36m"
DEFAULT = "\033[0m"

ACTION = BLUE + "[+] " + DEFAULT 
ERROR = RED + "[+] " + DEFAULT
OK =  GREEN + "[+] " + DEFAULT

#====================
#		OPTIONS
#====================

interface = -1
nbtime = 0
lastnb = 0

#====================
#		Parser
#====================

parser = argparse.ArgumentParser(description='Box-notifier.py tells you if someone is connected or disconnected to your router')
parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag' )
parser.add_argument('-i', nargs=1, help="set an interface")
parser.add_argument('-m', nargs=1, help="set a methode")

def SendNotif(message, title):
	""" send the notification to gnome """
	Notify.init('box-notify')
	n = Notify.Notification.new(title, message, "dialog-information")
	n.show()
	n.close()
	Notify.uninit()

def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,
        struct.pack('256s', ifname[:15])
    )[20:24])

def arp():
	global lastnb
	ip = get_ip(interface)
	fip = ip.split('.', 1)
	test = -1
	""" using the pwd arp-scan """
	print ACTION + "checking user list  .."
	os.system("sudo arp-scan -l --interface " + interface + " | sudo grep "+ fip[0] +" >> /tmp/bnt-list.txt")
	print ACTION + "reading user list .."
	#get file line number
	os.system("wc -l /tmp/bnt-list.txt >> /tmp/bnt-num.txt")
	with open("/tmp/bnt-num.txt", "rb") as f:
		first = f.readline()     	# Read the first line.
		test = first.split(' ', 1)	# Split it , so as to have the number
    	lastnb = test[0]
	
def nmap():
	global lastnb
	test = -1
	""" using the pwd arp-scan """
	print ACTION + "checking user list  .."
	os.system("sudo nmap -T5 -O "+ interface +"-255 >> /tmp/bnt-list.txt")
	print ACTION + "reading user list .."
	#get file line number
	os.system("wc -l /tmp/bnt-list.txt >> /tmp/bnt-num.txt")
	with open("/tmp/bnt-num.txt", "rb") as f:
		first = f.readline()     	# Read the first line.
		test = first.split(' ', 1)	# Split it , so as to have the number
    	lastnb = test[0]

def arp1():
	global lastnb
	ip = get_ip(interface)
	fip = ip.split('.', 1)
	output = os.system("sudo arp-scan -l --interface " + interface + " | sudo grep "+ fip[0] +" | wc -l")
	lastnb = output


def checker(nb, t):
	""" check connection and send notification """

	print "actual = " , nb
	print "last = ", t
	if nb > t:
		if t != 0:
			SendNotif("someone has connected to your router", "New connection")
		t = nb
	if nb < t:
		if t != 0:
			SendNotif("someone has disconnected from your router", "New disconnection")
		t = nb
	if nb == t:
		t = nb

	return t

def checkArp():
	""" check if arp-scan is installed """
	print ACTION + "Checking if arp-scan is installed .."
	if os.path.isfile("/usr/bin/arp-scan"):
		print OK + "arp-scan exist"
		return 1
	else :
		print ERROR  + "please install arp-scan , using sudo apt-get install arp-scan"
		return -1


def header():
	""" header informations """
	print "Box-notifier.py version 0.0.2"
	print "@author : Naper"
	print "Designed for Linux"
	print ""	

def clear():
	os.system("clear")
	header()

def delTMP():
	""" delete tmp files """
	os.system("rm /tmp/bnt-list.txt")
 	os.system("rm /tmp/bnt-num.txt")

args = parser.parse_args()

header()
if args.i and args.m:
	interface = args.i[0]
	#check if root
	#if os.geteuid() != 0:
		#print ERROR + "Please run box-notifier as root"
		#exit(1)
	arpi = checkArp()
	if arpi == -1:
		exit(1)
	""" doing arp every two seconds """
	while(1):
		#global lastnb
		if args.m[0] == "arp":
			arp()
		if args.m[0] == "nmap":
			#nmap
			nmap()
		print lastnb
		nbtime = checker(lastnb, nbtime)
		delTMP()
		clear()
		time.sleep(2)
else:
	print ERROR + "box-notifer.py need arguments please use -h"






