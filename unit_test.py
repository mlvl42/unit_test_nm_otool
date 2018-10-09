#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import signal
import subprocess
import argparse
import textwrap


# absolute path to your nm_otool project
PROJECT_PATH = 'YOUR PATH'

NM_PATH = os.path.join(PROJECT_PATH, 'ft_nm')
OTOOL_PATH = os.path.join(PROJECT_PATH, 'ft_otool')


def execute(cmd):
    proc = subprocess.Popen(cmd, shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()
    output = output.decode('unicode-escape').rstrip()
    error = error.decode('unicode-escape').rstrip()
    rc = proc.returncode
    return (output, rc, error)


def title(str):
    print('-' * (len(str) + 4))
    print('| ' + str + ' |')
    print('-' * (len(str) + 4))
    print()


def tests_nm(tests_array, args):

    errors = 0
    title("NM unit_tests")

    if len(tests_array) == 0 :
        return errors
    # get the longest test name, useful for padding
    max_len = max(tests_array, key=len)
    max_len = len(max_len)

    for t in tests_array:

        # execute nm and ft_nm
        nm_out , nm_rc , _ = execute("{} {}".format("nm", t))
        out , rc , err = execute("{} {}".format(NM_PATH, t))

        # compare their return value and output
        if rc == -signal.SIGSEGV:
            result = "\033[91mSEGMENTATION FAULT\033[0m"
            errors += 1
        elif nm_rc != 0 and rc != 0:
            result = "\033[92mOK\033[0m: \033[93mWARNING\033[0m nm returned {} and ft_nm returned {} but the error messages were not compared for more flexibility".format(nm_rc, rc)
        elif rc != nm_rc:
            result = "\033[91mERROR\033[0m: nm returned {}, ft_nm returned {}.".format(nm_rc, rc)
            errors += 1
        elif nm_out != out:
            result = "\033[91mERROR\033[0m: output differs"
            errors += 1
        else:
            result = "\033[92mOK\033[0m"

        if args.errors and "OK" in result:
           continue
        print("\t+ {:{length}} {result}".format(t, length=max_len, result=result))

    return errors


def tests_otool(tests_array):
    errors = 0
    title("OTOOL unit_tests")

    # get the longest test name, useful for padding
    max_len = max(tests_array, key=len)
    max_len = len(max_len)

    for t in tests_array:

        otool_out , otool_rc , _ = execute("{} {}".format("otool -t ", t))
        out , rc , err = execute("{} {}".format(OTOOL_PATH, t))

        # compare their return value and output
        if rc == -signal.SIGSEGV:
            result = "\033[91mSEGMENTATION FAULT\033[0m"
            errors += 1
        elif otool_rc != 0 and rc != 0:
            result = "\033[92mOK\033[0m: \033[93mWARNING\033[0m otool returned {} and ft_otool returned {} but the error messages were not compared for more flexibility".format(otool_rc, rc)
        elif rc != otool_rc:
            result = "\033[91mERROR\033[0m: otool returned {}, ft_otool returned {}.".format(otool_rc, rc)
            errors += 1
        elif otool_out != out:
            result = "\033[91mERROR\033[0m: output differs"
            errors += 1
        else:
            result = "\033[92mOK\033[0m"

        if args.errors and "OK" in result:
           continue
        print("\t+ {:{length}} {result}".format(t, length=max_len, result=result))

    return errors


def tests_main(args):

    errors = 0
    files_to_test = []

    # fill the files_to_test array according to the given parameters
    for arg in args.files:

        absolute_path = os.path.abspath(arg)
        if os.path.isdir(absolute_path):
            path = absolute_path

            for root, dirs, files in os.walk(path):
                path = root.split(os.sep)

                for file in files:
                    f = os.path.join(root, file)
                    out, rc, _ = execute("file {}".format(f))

                    if args.noignore or not rc and "Mach-O" in out:
                        files_to_test.append(f)

                if not args.recursive:
                    break
        else:
            files_to_test.append(absolute_path)

    print("[+] total amount of files to process: {}".format(len(files_to_test)))

    # # launch tests
    if args.nm:
        errors += tests_nm(files_to_test, args)
    if args.otool:
        errors += tests_otool(files_to_test)

    if errors:
        print("\n[!] total amount of errors: \033[91m{}\033[0m".format(errors))
    else:
        print("\n[T]/ no error occured, \033[92mgood job!\033[0m")

    return errors


if __name__ == '__main__':

    # argument parsing
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=textwrap.dedent('''
    \033[92m███╗   ██╗███╗   ███╗         ██████╗ ████████╗ ██████╗  ██████╗ ██╗     
    ████╗  ██║████╗ ████║        ██╔═══██╗╚══██╔══╝██╔═══██╗██╔═══██╗██║     
    ██╔██╗ ██║██╔████╔██║        ██║   ██║   ██║   ██║   ██║██║   ██║██║     
    ██║╚██╗██║██║╚██╔╝██║        ██║   ██║   ██║   ██║   ██║██║   ██║██║     
    ██║ ╚████║██║ ╚═╝ ██║███████╗╚██████╔╝   ██║   ╚██████╔╝╚██████╔╝███████╗
    ╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\033[0m

    Unit testing script made for the 42 school project nm_otool.
    This script compares your ft_nm/ft_otool output and return code to the system
    ones.

    In order to run this script, you must edit the following configuration
    variable located at the beginning of this file:

        PROJECT_PATH -> absolute path to your nm_otool project

    made by mguillau
    '''))

    parser.add_argument('files', nargs='+', help="files and/or folders to process")
    parser.add_argument('--recursive', '-R',  dest='recursive', action='store_true', help="recursively test binaries encountered for any folder passed as a parameter")
    parser.add_argument('--no-ignore', '-N',  dest='noignore', action='store_true', help="test every file encountered, even non binary ones")
    parser.add_argument('--errors', '-e',  dest='errors', action='store_true', help="only output errors")
    parser.add_argument('--otool', '-o',  dest='nm', action='store_false', help="only test otool")
    parser.add_argument('--nm', '-n',  dest='otool', action='store_false', help="only test nm")
    parser.set_defaults(recursive=False)
    parser.set_defaults(noignore=False)
    parser.set_defaults(errors=False)
    parser.set_defaults(otool=True)
    parser.set_defaults(nm=True)

    if len(sys.argv[1:]) == 0:
        parser.print_usage() # for just the usage line
        parser.exit()

    args = parser.parse_args()

    # check configuration
    if not os.path.exists(NM_PATH) or not os.path.exists(OTOOL_PATH):
        if os.path.exists(PROJECT_PATH):
            print("[!] NM_PATH and OTOOL_PATH not found but PROJECT_PATH exists")
            print("[?] attempting to compile ft_nm and ft_otool")
            out, rc, err = execute("make -C {}".format(PROJECT_PATH))
            if rc != 0:
                print(err)
                sys.exit(1)
            else:
                print(out)
        else:
            print("[!] PROJECT_PATH \033[91mnot found\033[0m. It needs to be the absolute_path to your nm_otool project")
            sys.exit(1)

    sys.exit(tests_main(args))
