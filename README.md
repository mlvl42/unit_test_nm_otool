# 42 ft_nm && ft_otool unit_tester

This small python3 scripts allows you to check for differences between your
implementation of the utilities `nm` and `otool`

*Do not use this script to determine a student's grade* without discussing
with him, it may contain errors and he might not have handled some tricky cases.

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

It is also possible to test files recusrively on multiple folder, a good
one line test for this project might be:

`python3 unit_test.py -eR /bin /sbin /usr/sbin /usr/bin /usr/lib`

see se usage `python3 unit_test -h` for a detailed explanation of every flags.



if you have any suggestions feel free to contact me
