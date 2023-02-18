#!/usr/bin/python3
#Created by Miguel Rios
import argparse
import sys
import os
from datetime import date
import getpass

def scoper(rv_num, scope, exclude_file=None): 
    if exclude_file:
        os.system('nmap -Pn -n -sL -iL '+scope+' --excludefile '+exclude_file+'|cut -d " " -f 5|grep -v "nmap\|address" > '+rv_num+'_InScope.txt')
    else:
        os.system('nmap -Pn -n -sL -iL '+scope+'|cut -d " " -f 5|grep -v "nmap\|address" > '+rv_num+'_InScope.txt')

def discovery(rv_num, target_list):
    nmap_folders = rv_num+'_Scans/'+rv_num+'_Nmap/'+rv_num+'_DISC/'
    os.system('mkdir -p '+nmap_folders)
    os.system('nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+nmap_folders+rv_num+'_DISC'+' '+'-iL '+target_list)
    os.chdir(nmap_folders)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')
    
def full_port(rv_num, target_list):
    nmap_folders = rv_num+'_Scans/'+rv_num+'_Nmap/'+rv_num+'_FULL/'
    os.system('mkdir -p '+nmap_folders)
    os.system('nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+nmap_folders+rv_num+'_FULL'+' '+'-iL '+target_list)
    os.chdir(nmap_folders)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')

def nikto(rv_num, target_list):
    nikto_folders = rv_num+'_Scans/'+rv_num+'_Nikto/'
    os.system('mkdir -p '+nikto_folders)
    home = os.getcwd()
    os.chdir(nikto_folders)
    targets = home+'/'+target_list
    filename = 'Mikto.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                mikto_location = os.path.abspath(os.path.join(root,name))
    os.system(mikto_location+' -f '+targets+' -w 10')

def aquatone(rv_num, target_list):
    aquatone_folders = rv_num+'_Scans/'+rv_num+'_Aquatone/'
    filename = 'aquatone'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                aquatone_location = os.path.abspath(os.path.join(root,name))
    os.system('mkdir -p '+aquatone_folders)
    home = os.getcwd()
    os.chdir(aquatone_folders)
    web_targets = home+'/'+target_list
    os.system('cat '+web_targets+'|'+str(aquatone_location))

def external_scans(rv_num, target_list):
    nmap_folders1 = rv_num+"_Scans/"+rv_num+"_Nmap/"+rv_num+"_DISC/"
    nmap_folders2 = rv_num+"_Scans/"+rv_num+"_Nmap/"+rv_num+"_FULL/"
    aquatone_folders1 = rv_num+"_Scans/"+rv_num+"_Aquatone/"+rv_num+"_DISC"
    aquatone_folders2 = rv_num+"_Scans/"+rv_num+"_Aquatone/"+rv_num+"_FULL"
    nikto_folders = rv_num+"_Scans/"+rv_num+"_Nikto/"
    home = os.getcwd()
    os.system('mkdir -p '+nmap_folders1)
    os.system('mkdir -p '+nmap_folders2)
    os.system('mkdir -p '+nikto_folders)
    os.system('mkdir -p '+aquatone_folders1)
    os.system('mkdir -p '+aquatone_folders2)
    nmap_initial = 'nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+nmap_folders1+rv_num+'_DISC'+' '+'-iL '+target_list
    os.system(nmap_initial)
    os.chdir(nmap_folders1)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')
    filename = 'aquatone'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                aquatone_location = os.path.abspath(os.path.join(root,name))
    os.chdir(home+'/'+aquatone_folders1)
    web_targets = home+'/'+nmap_folders1+'Parsed-Results/Third-Party/PeepingTom.txt'
    os.system('cat '+web_targets+'|'+str(aquatone_location))
    full_target = home+'/'+nmap_folders1+'Parsed-Results/Host-Lists/Alive-Hosts-Open-Ports.txt'
    nmap_full = 'nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+home+'/'+nmap_folders2+rv_num+'_FULL'+' '+'-iL '+full_target
    os.system(nmap_full)
    os.chdir(home+'/'+nmap_folders2)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')
    os.chdir(home+'/'+aquatone_folders2)
    web_targets = home+'/'+nmap_folders2+'Parsed-Results/Third-Party/PeepingTom.txt'
    os.system('cat '+web_targets+'|'+str(aquatone_location))
    os.chdir(home+'/'+nikto_folders)
    filename = 'Mikto.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                mikto_location = os.path.abspath(os.path.join(root,name))
    os.system(mikto_location+' -f '+web_targets+' -w 10')

def internal_scans(rv_num, target_list):
    nmap_folders1 = rv_num+"_Scans/"+rv_num+"_Nmap/"+rv_num+"_DISC/"
    nmap_folders2 = rv_num+"_Scans/"+rv_num+"_Nmap/"+rv_num+"_FULL/"
    aquatone_folders1 = rv_num+"_Scans/"+rv_num+"_Aquatone/"+rv_num+"_DISC"
    aquatone_folders2 = rv_num+"_Scans/"+rv_num+"_Aquatone/"+rv_num+"_FULL"
    home = os.getcwd()
    os.system('mkdir -p '+nmap_folders1)
    os.system('mkdir -p '+nmap_folders2)
    os.system('mkdir -p '+aquatone_folders1)
    os.system('mkdir -p '+aquatone_folders2)
    nmap_initial = 'nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+nmap_folders1+rv_num+'_DISC'+' '+'-iL '+target_list
    os.system(nmap_initial)
    os.chdir(nmap_folders1)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')
    filename = 'aquatone'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                aquatone_location = os.path.abspath(os.path.join(root,name))
    os.chdir(home+'/'+aquatone_folders1)
    web_targets = home+'/'+nmap_folders1+'Parsed-Results/Third-Party/PeepingTom.txt'
    os.system('cat '+web_targets+'|'+str(aquatone_location))
    full_target = home+'/'+nmap_folders1+'Parsed-Results/Host-Lists/Alive-Hosts-Open-Ports.txt'
    nmap_full = 'nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA '+home+'/'+nmap_folders2+rv_num+'_FULL'+' '+'-iL '+full_target
    os.system(nmap_full)
    os.chdir(home+'/'+nmap_folders2)
    filename = 'Gnmap-Parser.sh'
    for root,dirs,files in os.walk(r'/'):
        for name in files:
            if name == filename:
                parser_location = os.path.abspath(os.path.join(root,name))
    os.system(parser_location+' -p')
    os.chdir(home+'/'+aquatone_folders2)
    web_targets = home+'/'+nmap_folders2+'Parsed-Results/Third-Party/PeepingTom.txt'
    os.system('cat '+web_targets+'|'+str(aquatone_location))
    
def shodan_scans(rv_num, scope):
    shodan_folders = rv_num+"_Scans/"+rv_num+"_Shodan/"
    api_key = input("Enter your Shodan API Key: ")
    os.system('pip3 install -U --user shodan')
    os.system('shodan init '+api_key)
    os.system('mkdir -p '+shodan_folders)
    os.system('for i in $(cat '+scope+'); do shodan host $i && sleep 1; done >> '+shodan_folders+rv_num+'_Shodan_Results.txt')

def nuclei_scans(rv_num, target_list):
    uncover_engine = input("Use Shodan API to uncover addtional assets? (Y or N): ")
    nuclei_folders = rv_num+"_Scans/"+rv_num+"_Nuclei/"
    os.system('mkdir -p '+nuclei_folders)
    if uncover_engine == 'Y':
        api_key = input("Enter Shodan API key: ")
        os.system('export SHODAN_API_KEY='+api_key)
        os.system('nuclei -l '+target_list+' -ni -uc -ue shodan -o '+nuclei_folders+rv_num+'_Nuclei_Scans.txt')
    else:
        os.system('nuclei -l '+target_list+' -ni -o '+nuclei_folders+rv_num+'_Nuclei_Scans.txt')

#Currently there isn't a pressing need for this section but leaving here just in case
#def share_backup():
#    rv_num = input("Enter customer number: ")
#    cust_shortname = input("Enter Customer Shortname: ")
#    today = date.today()
#    archive_date = today.strftime("%Y%m%d")
#    zip_directories = 'zip -rv '+archive_date+'_'+rv_num+'_'+cust_shortname+'_share_backup.zip /share/'
#    os.system(zip_directories)
