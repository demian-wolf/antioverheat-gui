import subprocess


def verify_sudo_pwd(pwd):
    """Verify if the given user password is right.

    This is the password required for changing
    CPU frequency policies and other commands that
    require root privileges.

    :param pwd: the user password
    :type pwd: string

    :returns True if password is correct, and False otherwise.
    :rtype: boolean

    :example:

    >>> verify_sudo_pwd("the right password")
    True
    >>> verify_sudo_pwd("the wrong password")
    False
    """
    
    # TODO: replace this dirty workaround with a more clean solution
    failure = "Password: \r\nsu: Authentication failure\r\n"
    cmd = '{ sleep 1; echo "%s"; } | script -q -c "su -l root -c ls /root" /dev/null' % pwd
    return failure != subprocess.check_output(cmd, shell=True).decode()
