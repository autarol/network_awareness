#!/usr/bin/python

class logger():
    def log_error(e):
        f = open("/var/log/driverSDN.log","a")
        f.write("error : %s\n"%e)
        f.close()
