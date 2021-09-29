import os

for (path, dir, files) in os.walk("./private"):
    for filename in files:
        ext = os.path.splitext(filename)[-1]
        if ext == '.pem':
            print("%s/%s" % (path, filename))

# import paramiko
# k = paramiko.RSAKey.from_private_key_file("./mykey.pem")
# c = paramiko.SSHClient()
# c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# print "connecting"
# c.connect(hostname="www.acme.com", username="ubuntu", pkey=k)
# print "connected"
# commands = ["/home/ubuntu/firstscript.sh", "/home/ubuntu/secondscript.sh"]
# for command in commands:
#     print "Executing {}".format(command)
#     stdin, stdout, stderr = c.exec_command(command)
#     print stdout.read()
#     print("Errors")
#     print stderr.read()
# c.close()
