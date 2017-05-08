# 42 ft_nm && ft_otool unit_tester

This small python3 script allows you to check for differences between your
implementation of the utilities `nm` and `otool`

**Do not use this script to determine a student's grade** without discussing
with him, it may contain errors and he might not have handled some tricky cases.
Moreover this script doesn't test every behaviours (like launching `nm` without any parameter),
passing every tests doesn't mean you'll get a good grade. Consider yourself warned.

# Install

In order to run this script, you must edit the following configuration
variable located at the beginning of `unit_test.py`:

`PROJECT_PATH -> absolute path to your nm_otool project`

and then you are good to go!

# Examples

By default the script will check both your `ft_nm` and `ft_otool` on every
*binaries* encountered for a given path:

`python3 unit_test.py /bin`

If you wish to test every files (including non mach-o ones):

`python3 unit_test.py -N /bin`

It is also possible to test files recursively on multiple folders, a good
one line test for this project might be:

`python3 unit_test.py -eR /bin /sbin /usr/sbin /usr/bin /usr/lib`

Use the help parameter : `python3 unit_test -h` for a detailed explanation of every flags.

# Custom Tests folders

The OSx implementations of `nm and otool` handle a lot of parsing errors, the folder
`custom_tests` contains some basic tests, as well as some harder ones. (If you did not handle
parsing errors you'll definitely get a segmentation fault)


If you have any suggestions feel free to contact me.
