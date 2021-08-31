# How to run
# $ sudo python docker-checker.py

import subprocess

s = subprocess.check_output('docker ps', shell=True)
print("Results of docker ps", s)
