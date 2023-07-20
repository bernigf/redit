import time
import datetime
import sys
import os
import subprocess

import pexpect
import getpass

from datetime import datetime, timedelta
from time import sleep

name = "redit"
version = "0.2.3"

folder_main  = ".redit"
folder_temp  = "tmp"
folder_cache = "cache"
folder_hosts = "hosts"
folder_home = os.path.expanduser("~")

config_file_recent = "recent.yaml"

editor_name = "vim"

GLOBAL_ARGS = sys.argv[1:]

class pcolors :
    
    green = '\033[92m' 
    blue = '\033[34m'
    RED = '\033[91m'
    VIOLET = '\33[95m'
    yellow = '\33[93m'
    TUR = '\33[96m'
    
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    warning = '\033[93m'
    endc = '\033[0m'
            
    BLINK    = '\33[5m'
    BLINK2   = '\33[6m'
    SELECTED = '\33[7m'

def main(PARAM_args) :
    
    defName = " ### main : "

    ARGS = PARAM_args

    pre_str = " >>> "

    now = datetime.now()
    now_str = str(now.strftime('%H:%M:%S'))

    print()
    print(defName + f"Starting python {pcolors.yellow}{name}{pcolors.endc} v{version} at {now_str}")

    if(ARGS==[]):
        source = recent_menu()
    else:
        source = ARGS[0]

    print(defName + f"Caching source: {pcolors.green}{source}{pcolors.endc}")

    print()
    print(f" {pcolors.warning}WARNING:{pcolors.endc} If you dont want to use password completion leave blank")
    host_password = getpass.getpass(pre_str + "SSH host password: ") 
    print()

    target = source_deconstruct(source)

    recent_add(source)

    if(host_password != ""):
        get_ok = scp_copy_auto(source,target,host_password)
    else:
        get_ok = scp_copy(source, target)

    if(get_ok):

        exit_flag = False

        while(not exit_flag):

            output = editor_open(target)

            upload_flag = False
            resp = input(pre_str + "Upload file back to host (yes/no) [no] : ")
            if(resp == "") : resp = "no"
            if(resp.lower() == "n") : resp = "no"
            if(resp != "no") : upload_flag = True
            
            if(upload_flag):

                upload_ok = False
                if(host_password != ""):
                    upload_ok = scp_copy_auto(target, source, host_password)
                else:
                    upload_ok = scp_copy(target, source)

                if(upload_ok):
                    print()
                    print(defName + f"Upload finished {pcolors.green}OK{pcolors.endc}")
                    print()
                else:
                    print()
                    print(defName + f"Error uploading file")
                    print()

            resp = input(pre_str + "Continue editing file (yes/no) [yes] : ")
            if(resp == "") : resp = "yes"
            if(resp.lower() == "y") : resp = "yes"
            if(resp != "yes") : exit_flag = True

def recent_add(PARAM_file) :

    defName = " ### recent_add : "

    pre_str = " >>> "

    config_recent_file = folder_home + "/" + folder_main + "/" + config_file_recent

    new_file = PARAM_file

    if(not os.path.exists(config_recent_file)):

        lines = []

    else:

        with open(config_recent_file, 'r') as file:
            lines = file.read().splitlines()

        for item in lines:

            if item.strip() :

                if(item.strip() == new_file) : lines.remove(item)

            else:

                lines.remove(item)

    lines.insert(0, new_file)

    with open(config_recent_file, 'w') as file:

        for item in lines:
            file.write(item + "\n")

def recent_menu():

    defName = " ### recent_menu : "

    pre_str = " >>> "

    config_recent_file = folder_home + "/" + folder_main + "/" + config_file_recent

    if(os.path.exists(config_recent_file)):

        with open(config_recent_file, 'r') as file:
            lines = file.readlines()

        counter = 1
        files = [None]

        print()

        for item in lines :

            if(item.strip() != "") :
                files.append(item.strip())
                print(f" {str(counter)} > {item.strip()}")
                counter += 1

        print()
        input(pre_str + "Select item: ")

def editor_open(PARAM_file) :

    defName = " ### editor_open: "

    pre_str = " >>> "
    
    filename = PARAM_file

    print(defName + "Opening editor ...")
    print()
    print(pre_str + f"editor: {pcolors.yellow}{editor_name}{pcolors.endc}")
    print(pre_str + f"file: {filename}")
    print()

    try:

        subprocess.run([editor_name, filename])

    except subprocess.CalledProcessError as e:

        print(defName + f"Error occurred trying to edit the file: {e}")
        print()
        quit()

def scp_copy(PARAM_source, PARAM_target):
    
    defName = " ### scp_copy: "

    source = PARAM_source
    target = PARAM_target

    pre_str = " >>> "

    print()
    print(defName + "Calling scp...")
    print()
    print(pre_str + "source: " + source)
    print(pre_str + "target: " + target)
    print()

    try:
        subprocess.run(['scp', source, target])
        print()
        print(defName + f"File copied {pcolors.green}OK{pcolors.endc}")
        return True

    except subprocess.CalledProcessError as e:
        print(defName + f"Error occurred while copying the file: {e}")
        return False

    print()

def scp_copy_auto(PARAM_source, PARAM_target, PARAM_password):
    
    defName = " ### scp_copy_auto: "

    source = PARAM_source
    target = PARAM_target
    password = PARAM_password

    pre_str = " >>> "

    print()
    print(defName + "Calling scp (autofill password) ...")
    print()
    print(pre_str + "source: " + source)
    print(pre_str + "target: " + target)
    print()

    #parts = source.split(":")
    #host = parts[0]
    #host_pass_str = host + "'s password:"
    #print(host_pass_str)

    child = pexpect.spawn(f"scp {source} {target}")
    child.logfile_read = sys.stdout.buffer
    index = child.expect(["password:", pexpect.EOF, pexpect.TIMEOUT])

    if index == 0:

        child.sendline(password)
        child.expect(pexpect.EOF)
        print()
        print(defName + f"File copied {pcolors.green}OK{pcolors.endc}")
        return True

    else:

        print(defName + f"Error occurred while copying the file: {e}")
        return False

    print()


def source_deconstruct(PARAM_source):

    defName = " ### source_deconstruct: "

    source = PARAM_source
    
    print()
    print(defName + "Parsing source string...")
    print()

    pre_str = " >>> "
    print(pre_str + "source: " + source)
    print()

    parts = source.split(':')
    username_host = parts[0].split('@')
    source_username = username_host[0]
    source_host = username_host[1]
    path_parts = parts[1].split('/')
    source_dirs = path_parts[:-1]
    source_filename = path_parts[-1]

    print(pre_str + "host: " + source_host)
    print(pre_str + "user: " + source_username)
    print()
    
    counter = 0 
    for item in source_dirs:
        counter += 1
        print(pre_str + "dir " + str(counter) + ": " + item)

    print()
    print(pre_str + "file: " + source_filename)
    print()

    target_path = folder_home + "/" + folder_main + "/" + folder_cache + "/"
    target_path += source_username + "@" + source_host + "/"
    for item in source_dirs:
        target_path += item + "/"

    try:
        os.makedirs(target_path)
        result_str = f"created {pcolors.green}OK{pcolors.endc}"
    except FileExistsError:
        result_str = f"already {pcolors.blue}EXISTS{pcolors.endc}"

    print(pre_str + "target_path: " + target_path)
    print(pre_str + "target_path " + result_str)

    target_file = target_path + source_filename

    return target_file

main(GLOBAL_ARGS)

