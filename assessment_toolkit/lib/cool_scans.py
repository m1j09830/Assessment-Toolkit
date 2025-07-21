#!/usr/bin/python3
# Created by Miguel Rios
import argparse
import sys
import os
from datetime import date
import getpass
import subprocess
import shlex
from pathlib import Path
from typing import Optional


def find_file_in_path(filename: str) -> Optional[str]:
    """Find a file in the system PATH and common locations"""
    for root, dirs, files in os.walk('/'):
        if filename in files:
            return os.path.abspath(os.path.join(root, filename))
    print(f"{filename} not found in the system.")
    return None


def run_command_safe(command: str, cwd: Optional[str] = None) -> bool:
    """Safely execute shell commands using subprocess and show real-time output"""
    try:
        print(f"🔄 Running command: {command}")
        if cwd:
            print(f"📁 Working directory: {cwd}")
        print("-" * 50)
        
        # Run command with real-time output streaming
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Merge stderr with stdout
            cwd=cwd,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Print output in real-time as it comes
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
        
        # Wait for process to complete
        process.stdout.close()
        return_code = process.wait()
        
        print("-" * 50)
        if return_code == 0:
            print(f"✅ Command completed successfully")
            return True
        else:
            print(f"❌ Command failed with exit code {return_code}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error running command: {command}\nError: {e}")
        return False

def scoper(rv_num: str, scope: str, exclude_file: Optional[str] = None) -> bool: 
    if exclude_file:
        command = f'nmap -Pn -n -sL -iL {shlex.quote(scope)} --excludefile {shlex.quote(exclude_file)} | cut -d " " -f 5 | grep -v "nmap\\|address" > {shlex.quote(rv_num)}_InScope.txt'
    else:
        command = f'nmap -Pn -n -sL -iL {shlex.quote(scope)} | cut -d " " -f 5 | grep -v "nmap\\|address" > {shlex.quote(rv_num)}_InScope.txt'
    return run_command_safe(command)

def discovery(rv_num: str, target_list: str) -> bool:
    """Run initial discovery scan"""
    nmap_folders = f'{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_DISC/'
    
    # Create directories safely
    Path(nmap_folders).mkdir(parents=True, exist_ok=True)
    
    # Build nmap command with proper escaping
    nmap_cmd = f'nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders + rv_num + "_DISC")} -iL {shlex.quote(target_list)}'
    
    if not run_command_safe(nmap_cmd):
        return False
    
    # Find and run parser
    parser_location = find_file_in_path('Gnmap-Parser.sh')
    if parser_location:
        return run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders)
    else:
        print("Gnmap-Parser.sh not found")
        return False
    
def full_port(rv_num: str, target_list: str) -> bool:
    """Run full port scan"""
    nmap_folders = f'{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_FULL/'
    
    # Create directories safely
    Path(nmap_folders).mkdir(parents=True, exist_ok=True)
    
    # Build and run nmap command
    nmap_cmd = f'nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders + rv_num + "_FULL")} -iL {shlex.quote(target_list)}'
    
    if not run_command_safe(nmap_cmd):
        return False
    
    # Find and run parser
    parser_location = find_file_in_path('Gnmap-Parser.sh')
    if parser_location:
        return run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders)
    else:
        print("Gnmap-Parser.sh not found")
        return False

def nikto(rv_num: str, target_list: str) -> bool:
    """Run Nikto scans"""
    nikto_folders = f'{rv_num}_Scans/{rv_num}_Nikto/'
    Path(nikto_folders).mkdir(parents=True, exist_ok=True)
    
    home = os.getcwd()
    targets = os.path.join(home, target_list)
    
    # Find Mikto.sh script
    mikto_location = find_file_in_path('Mikto.sh')
    if mikto_location:
        command = f'{shlex.quote(mikto_location)} -f {shlex.quote(targets)} -w 10'
        return run_command_safe(command, cwd=nikto_folders)
    else:
        print("Mikto.sh not found")
        return False

def aquatone(rv_num: str, target_list: str) -> bool:
    """Run Aquatone scans"""
    aquatone_folders = f'{rv_num}_Scans/{rv_num}_Aquatone/'
    Path(aquatone_folders).mkdir(parents=True, exist_ok=True)
    
    home = os.getcwd()
    web_targets = os.path.join(home, target_list)
    
    aquatone_location = find_file_in_path('aquatone')
    if aquatone_location:
        command = f'cat {shlex.quote(web_targets)} | {shlex.quote(aquatone_location)}'
        return run_command_safe(command, cwd=aquatone_folders)
    else:
        print("aquatone not found")
        return False

def external_scans(rv_num: str, target_list: str) -> bool:
    """Run external scans (discovery, full port, aquatone, nikto)"""
    # Create all necessary directories
    nmap_folders1 = f"{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_DISC/"
    nmap_folders2 = f"{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_FULL/"
    aquatone_folders1 = f"{rv_num}_Scans/{rv_num}_Aquatone/{rv_num}_DISC"
    aquatone_folders2 = f"{rv_num}_Scans/{rv_num}_Aquatone/{rv_num}_FULL"
    nikto_folders = f"{rv_num}_Scans/{rv_num}_Nikto/"
    
    home = os.getcwd()
    
    # Create directories safely
    for folder in [nmap_folders1, nmap_folders2, nikto_folders, aquatone_folders1, aquatone_folders2]:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    # Initial nmap discovery scan
    nmap_initial = f'nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders1 + rv_num + "_DISC")} -iL {shlex.quote(target_list)}'
    
    if not run_command_safe(nmap_initial):
        return False
    
    # Run parser on discovery results
    parser_location = find_file_in_path('Gnmap-Parser.sh')
    if parser_location:
        if not run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders1):
            return False
    else:
        print("Gnmap-Parser.sh not found")
        return False
    
    # Run aquatone on discovery results
    aquatone_location = find_file_in_path('aquatone')
    if aquatone_location:
        web_targets = os.path.join(home, nmap_folders1, 'Parsed-Results/Third-Party/PeepingTom.txt')
        if not run_command_safe(f'cat {shlex.quote(web_targets)} | {shlex.quote(aquatone_location)}', cwd=aquatone_folders1):
            return False
    else:
        print("aquatone not found")
        return False
    
    # Full port scan
    full_target = os.path.join(home, nmap_folders1, 'Parsed-Results/Host-Lists/Alive-Hosts-Open-Ports.txt')
    nmap_full = f'nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders2 + rv_num + "_FULL")} -iL {shlex.quote(full_target)}'
    
    if not run_command_safe(nmap_full):
        return False
    
    # Parse full scan results
    if not run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders2):
        return False
    
    # Run aquatone on full scan results
    web_targets = os.path.join(home, nmap_folders2, 'Parsed-Results/Third-Party/PeepingTom.txt')
    if not run_command_safe(f'cat {shlex.quote(web_targets)} | {shlex.quote(aquatone_location)}', cwd=aquatone_folders2):
        return False
    
    # Run Nikto scans
    mikto_location = find_file_in_path('Mikto.sh')
    if mikto_location:
        command = f'{shlex.quote(mikto_location)} -f {shlex.quote(web_targets)} -w 10'
        return run_command_safe(command, cwd=nikto_folders)
    else:
        print("Mikto.sh not found")
        return False

def internal_scans(rv_num: str, target_list: str) -> bool:
    """Run internal scans (discovery, full port, aquatone)"""
    nmap_folders1 = f"{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_DISC/"
    nmap_folders2 = f"{rv_num}_Scans/{rv_num}_Nmap/{rv_num}_FULL/"
    aquatone_folders1 = f"{rv_num}_Scans/{rv_num}_Aquatone/{rv_num}_DISC"
    aquatone_folders2 = f"{rv_num}_Scans/{rv_num}_Aquatone/{rv_num}_FULL"
    home = os.getcwd()

    # Create directories safely
    for folder in [nmap_folders1, nmap_folders2, aquatone_folders1, aquatone_folders2]:
        Path(folder).mkdir(parents=True, exist_ok=True)

    # Initial discovery scan
    nmap_initial = f'nmap -Pn -n -sS -p 21,22,23,25,53,111,137,139,445,80,443,8443,8080,8000,1812,1433,135,4443,110,2222,993,2077,2078,3306,3389 --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders1 + rv_num + "_DISC")} -iL {shlex.quote(target_list)}'
    
    if not run_command_safe(nmap_initial):
        return False

    # Run parser on discovery
    parser_location = find_file_in_path('Gnmap-Parser.sh')
    if parser_location:
        if not run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders1):
            return False
    else:
        print("Gnmap-Parser.sh not found")
        return False

    # Run aquatone on discovery results
    aquatone_location = find_file_in_path('aquatone')
    if aquatone_location:
        web_targets = os.path.join(home, nmap_folders1, 'Parsed-Results/Third-Party/PeepingTom.txt')
        if not run_command_safe(f'cat {shlex.quote(web_targets)} | {shlex.quote(aquatone_location)}', cwd=aquatone_folders1):
            return False

        # Full port scan
        full_target = os.path.join(home, nmap_folders1, 'Parsed-Results/Host-Lists/Alive-Hosts-Open-Ports.txt')
        nmap_full = f'nmap -Pn -n -sV -p- --min-hostgroup 255 --min-rtt-timeout 0ms --max-rtt-timeout 100ms --max-retries 1 --max-scan-delay 0 --min-rate 2000 -vvv --open -oA {shlex.quote(nmap_folders2 + rv_num + "_FULL")} -iL {shlex.quote(full_target)}'
        
        if not run_command_safe(nmap_full):
            return False

        # Parse full scan results
        if not run_command_safe(f'{shlex.quote(parser_location)} -p', cwd=nmap_folders2):
            return False

        # Run aquatone on full scan results
        web_targets = os.path.join(home, nmap_folders2, 'Parsed-Results/Third-Party/PeepingTom.txt')
        return run_command_safe(f'cat {shlex.quote(web_targets)} | {shlex.quote(aquatone_location)}', cwd=aquatone_folders2)
    else:
        print("aquatone not found")
        return False

def shodan_scans(rv_num: str, scope: str) -> bool:
    """Run Shodan scans"""
    shodan_folders = f'{rv_num}_Scans/{rv_num}_Shodan/'
    api_key = input("Enter your Shodan API Key: ")
    
    Path(shodan_folders).mkdir(parents=True, exist_ok=True)
    
    # Install shodan package safely
    install_cmd = 'pip3 install -U --user shodan'
    if not run_command_safe(install_cmd):
        return False
    
    # Initialize shodan
    init_cmd = f'shodan init {shlex.quote(api_key)}'
    if not run_command_safe(init_cmd):
        return False
    
    # Run shodan scans
    scan_cmd = f'for i in $(cat {shlex.quote(scope)}); do shodan host $i && sleep 1; done >> {shlex.quote(shodan_folders + rv_num + "_Shodan_Results.txt")}'
    return run_command_safe(scan_cmd)

def nuclei_scans(rv_num: str, target_list: str) -> bool:
    """Run Nuclei scans"""
    uncover_engine = input("Use Shodan API to uncover additional assets? (Y or N): ")
    nuclei_folders = f'{rv_num}_Scans/{rv_num}_Nuclei/'
    Path(nuclei_folders).mkdir(parents=True, exist_ok=True)
    
    if uncover_engine.upper() == 'Y':
        api_key = input("Enter Shodan API key: ")
        # Set environment variable securely
        env = os.environ.copy()
        env['SHODAN_API_KEY'] = api_key
        
        command = f'nuclei -l {shlex.quote(target_list)} -ni -uc -ue shodan -o {shlex.quote(nuclei_folders + rv_num + "_Nuclei_Scans.txt")}'
        return run_command_safe(command)
    else:
        command = f'nuclei -l {shlex.quote(target_list)} -ni -o {shlex.quote(nuclei_folders + rv_num + "_Nuclei_Scans.txt")}'
        return run_command_safe(command)

#Currently there isn't a pressing need for this section but leaving here just in case
#def share_backup():
#    rv_num = input("Enter customer number: ")
#    cust_shortname = input("Enter Customer Shortname: ")
#    today = date.today()
#    archive_date = today.strftime("%Y%m%d")
#    zip_directories = 'zip -rv '+archive_date+'_'+rv_num+'_'+cust_shortname+'_share_backup.zip /share/'
#    os.system(zip_directories)
