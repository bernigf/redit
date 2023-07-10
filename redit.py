import time
import datetime
import sys
import os
import subprocess

from datetime import datetime, timedelta
from time import sleep

name = "redit"
version = "0.1.8"

folder_main  = ".redit"
folder_temp  = "tmp"
folder_cache = "cache"
folder_hosts = "hosts"
folder_home = os.path.expanduser("~")

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
    WARNING = '\033[93m'
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

    source = ARGS[0]

    print(defName + f"Caching source: {pcolors.green}{source}{pcolors.endc}")

    target = source_deconstruct(source)
    get_ok = scp_copy(source, target)

    if(get_ok):

        exit_flag = False

        while(!exit_flag):

            output = editor_open(target)


def editor_open(PARAM_file) :

    defName = " ### editor_open: "

    pre_str = " >>> "

    print(defName + "Opening editor ...")
    print()
    print(pre_str + f"editor: {pcolors.yellow}{editor_name}{pcolors.endc}")
    print(pre_str + f"file: {target}")
    print()

    try:

        subprocess.run([editor_name, target])

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

