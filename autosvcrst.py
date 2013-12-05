#   AUTO SERVICES RESTART (autosvcrst)
#   VERSION: 0.2
#   Tested on Windows XP, 7
#   module need (time, wmi, argparse, win32serviceutil, sys, time)
#   Created by: Armando & Zer0Trac3
#
#
#   This program will check if a service is down and restart it.
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import win32serviceutil as wsu
#import win32service
import sys, time
import argparse
import wmi
'''
This program was developed for Network Defense and CTF competition. 
    Syntax use
    
    -h (help menu)
    -u (keep services up requires the Name of the service and not the Caption) example autosvcrst -u Apache2.4,mysql,vsftpd
    -l (list all running services) example: autosvcrst -l stop or autosvcrst -l start


'''
# function check the status of a service and start it if not running
def manage (action, service):
    c = wmi.WMI()
    if action == 'status':
        if wsu.QueryServiceStatus(service)[1] != 4:
            for services in c.Win32_Service(Name=service):
                #added v0.2 (bug fix: System crash if service was disabled)
                # this will make sure the StartType is set to Automatic before restarting the service
                services.ChangeStartMode(StartMode='Automatic')
                print '%s is down restarting NOW' % service
                wsu.RestartService(service)
                # sleep must be at least 10 sec. 
                # Tested 5 sec and it crashes the program
                time.sleep(10)

# add v0.2
# This function creates a list of services that are running/stopped with name, caption 
def ListService(l):
    l = wmi.WMI ()
    # only running services check
    if ServicesList.l=='start':
        for l in l.Win32_Service ():
            if l.State == 'Running':
                print l.Name,'|', l.Caption, '|', l.State
    # only stop services check
    elif ServicesList.l=='stop':
        l = wmi.WMI ()
        for l in l.Win32_Service ():
            if l.State == 'Stopped':
                print l.Name, '|', l.Caption, '|', l.State
    # All services check
    elif ServicesList.l =='all':
        for l in l.Win32_Service ():
            print l.Name, '|', l.Caption, '|', l.State
                
# split the service name input by user
def split(ServicesList):
    ServicesList = ServicesList.u.split(',')
    for services in ServicesList:
        manage('status', services)

# main function
if __name__ == '__main__':

    # add v0.2 
    # This parse was added for multiple type of operation
    p = argparse.ArgumentParser(description='Auto Services Restart')
    p.add_argument('-u', type=str, 
                   help='Keeps Services UP and RUNNING. Please separate services by "," ex: mysql,apache2.4')
    p.add_argument('-l', type=str, 
                   help='List all running services with name commands: all, stop, start')
    ServicesList =p.parse_args()
    
    if ServicesList.u is None and ServicesList.l is None:
        p.error('\n \nAt least one argument must be supplied.')
    elif ServicesList.l:
        ListService(ServicesList)
        if ServicesList.u:
            while True:
                send = split(ServicesList)
    elif ServicesList.u:
            while True:
                send = split(ServicesList)
    
    
    ############################# OLD v0.1 code ################################
    #######Removed from v0.2 didn't need after using argparse###################
    #######Keeping code until final decision to completely remove###############
    
    #Declare ServicesList string
#    ServicesList = ''

#    if len(sys.argv) <= 1:
#        print "ERROR: You must supply at least one service if multiple service required separate with a comma \n"
#        print "example: Apache2.4 or Apache2.4,MySQL\n"
#        sys.exit()
        
#    else:
#        ServicesList = str(sys.argv[1])

# Endless loop (will sleep for 5 sec. before re-checking)
#while True:
#    send = split(ServicesList)
#    time.sleep(5)
    
