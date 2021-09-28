#!/usr/bin/env python3

import subprocess

def determineReturnCode(*args):
    """ Determine the ultimate return code for the given return codes.

        If 1 of the given return codes is nonzero, return that code.
        If 2 or more given return codes are nonzero, return 255.
        If no given return codes are nonzero, return 0.

        Input:  return codes <int>

        Output: ultimate return code <int>
    """
    # Default good return code
    returnCode = 0

    # The number of given nonzero return codes
    nonZeroRCCount = 0

    # Go through each given return code
    for code in args:
        # If the return code is not 0 (a bad return code)
        if code != 0:
            # Increment and set the new return code
            nonZeroRCCount += 1
            returnCode = code

    # If there are multiple nonzero return codes given, return code is 255
    if nonZeroRCCount > 1:
        returnCode = 255

    return returnCode

def startProcess(cmd):
    """ Start up a new process using the given command/parameters.

        Return the newly created process.

        Input:  process command [command and parameters <str>]

        Output: process <subprocess.Popen>
    """
    # Create a process with the given command/parameters
    process = subprocess.Popen(cmd)

    return process

def stopProcess(process, timeout=60, termRetries=5, killRetries=5):
    """ Attempt to stop the given process. First, try to nicely terminate the
        process 'termRetries' number of times. If terminating fails, try
        killing the process 'killRetries' number of times. By setting
        'killRetries' to 0, kill process is disabled.

        Return the process's return code.

        Input:  process <subprocess.Popen>
                terminate/kill timeout <int>
                terminate retries <int>
                kill retries <int>

        Output: process return code <int>
    """
    # Try terminating the process
    for retry in range(termRetries):
        try:
            # Tell the process to terminate (SIGINT) and wait for the process
            # to terminate.
            process.terminate()
            process.wait(timeout=timeout)
            break
        # process.wait() timed out
        except subprocess.TimeoutExpired:
            print("Attempt {}/{} to terminate PID ({}) failed.".format(retry+1, termRetries, process.pid))

    # If allowed and the process didn't terminate nicely, try killing it
    if process.poll() is None:
        for retry in range(killRetries):
            try:
                # Tell the process to kill itself (SIGKILL) and wait for the
                # process to be killed.
                process.kill()
                process.wait(timeout=timeout)
                break
            # process.wait() timed out
            except subprocess.TimeoutExpired:
                print("Attempt {}/{} to kill PID ({}) failed.".format(retry+1, termRetries, process.pid))

    return process.returncode


def startGui():
    """ Start the Qt GUI in a new process. Return the new process.

        Input:  None
        Output: process <subprocess.Popen>
    """
    # Command and parameters
    cmd = ["./minesweeper.py"]

    # Start new process and return process object
    return startProcess(cmd)


def startWebServer():
    """ Start the web server in a new process. Return the new process.

        Input:  None
        Output: process <subprocess.Popen>
    """
    # Command and parameters
    cmd = ["./web/website.py"]

    # Start new process and return process object
    return startProcess(cmd)


def main():
    """
        WRITTEN BY DAVID WESCOTT - Thank you dave

        A quick example of how to run a Qt GUI and a web server from 1 start
        script.

        This script creates 2 processes using subprocess.Popen. Then it waits
        for the GUI process to exit. After the GUI exits, the web server
        process is stopped. The return codes from both processes are evaluated
        and an ultimate return code is determined. This script's return code is
        the ultimate return code.

        Input:  None

        Output: None
    """
    # Start the GUI process
    guiProcess = startGui()

    # Start the web server process
    webProcess = startWebServer()

    # Wait for the GUI process to exit
    guiProcess.wait()

    # Get the GUI process's return code
    guiReturnCode = guiProcess.returncode

    # Stop the web server process and get its return code
    webReturnCode = stopProcess(webProcess)

    print("GUI Return Code:", guiReturnCode)
    print("Web Server Return Code:", webReturnCode)

    # Determine the ultimate return code from the GUI and web server return codes
    returnCode = determineReturnCode(guiReturnCode, webReturnCode)

    exit(returnCode)

if __name__ == "__main__":
    main()
