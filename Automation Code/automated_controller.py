import pysftp
import csv
import os
import paramiko


def get_aws_ec2_info():
    # find aws ec2 info from ./private/ec2_info.csv
    print("[01] Select AWS Server")
    target_ec2 = ""
    ec2_info = []
    f = open("./private/ec2_info.csv", "r", encoding="utf-8")
    lines = csv.reader(f)
    next(lines, None)
    cnt = 1
    for line in lines:
        print("└─[*]", cnt, ":", line[0], "|", line[1])
        ec2_info.append(line[1])
        cnt += 1
    print("└──[*] Select EC2: ", end="")
    target_ec2_num = input()
    f.close()
    return str(ec2_info[int(target_ec2_num)-1])


def aws_connect(target_ec2):
    # find .pem file
    print("[02] AWS Connection...")
    for (path, dir, files) in os.walk("./private"):
        for filename in files:
            ext = os.path.splitext(filename)[-1]
            if ext == '.pem':
                print("└─[*] Prepare private key: %s/%s" % (path, filename))
                fullpath = path+"/"+filename
                k = paramiko.RSAKey.from_private_key_file(fullpath)
                c = paramiko.SSHClient()
                c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print("└─[*] Connecting...")

                c.connect(target_ec2, username="ubuntu", pkey=k)
                print("└─[+] Connected!")

                # Run Command
                commands = ["cat /home/ubuntu/workspace/main.py"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print(stdout.read())
                    print("└─[*] Errors")
                    print(stderr.read())
                c.close()


if __name__ == "__main__":
    print("[00] Automated Controler Start")
    target_ec2 = get_aws_ec2_info()
    aws_connect(target_ec2)


# To Do List
# sftp
# _______________________________________
# import pysftp

# myHostname = "yourserverdomainorip.com"
# myUsername = "root"
# myPassword = "12345"

# with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
#     print "Connection succesfully stablished ... "

#     # Define the file that you want to upload from your local directorty
#     # or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
#     localFilePath = './TUTORIAL2.txt'

#     # Define the remote path where the file will be uploaded
#     remoteFilePath = '/var/integraweb-db-backups/TUTORIAL2.txt'

#     sftp.put(localFilePath, remoteFilePath)

# # connection closed automatically at the end of the with-block
