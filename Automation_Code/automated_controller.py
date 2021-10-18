from threading import local
from paramiko import transport
import pysftp
import csv
import os
import paramiko


def get_aws_ec2_info():
    # find aws ec2 info from ./private/ec2_info.csv
    print("\n==========[01] Select AWS Server")
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
    print("\n==========[02] AWS Connection...")
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
                commands = ["sudo mkdir /home/ubuntu/transmission",
                            "sudo chmod -R 777 /home/ubuntu/transmission"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


def aws_sftp_send(target_ec2):
    # find .pem file
    print(
        "\n==========[03] Sender: File transmission (Controller to Worker (EC2))")
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

                sftp = c.open_sftp()

                entries = os.listdir('./transmission')
                for entry in entries:
                    print("└──[*] Send target:", entry, end=' ')
                    local_path = "./transmission/"
                    local_path = os.path.join(local_path, entry)
                    print(local_path)
                    target_path = "/home/ubuntu/transmission/"
                    target_path = os.path.join(target_path, entry)
                    sftp.put(local_path, target_path)

                # Run Command
                commands = ["sudo cp -R /home/ubuntu/transmission /",
                            "sudo chmod -R 777 /transmission",
                            "ls /transmission"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


def docker_image_handling(target_ec2):
    # find .pem file
    print("\n==========[04] Docker Setting...")
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

                # Get dockerhub info (dockerhub_info.csv)
                dockerhub_login = []
                dockerhub_tag = ""
                f = open("./private/dockerhub_info.csv", "r", encoding="utf-8")
                lines = csv.reader(f)
                next(lines, None)
                cnt = 1
                dockerhub_info = []
                for line in lines:
                    print("└─[*]", cnt, ":", line[0],
                          "|", line[1], "|", line[2])
                    temp = []
                    temp.append(line[0])
                    temp.append(line[1])
                    temp.append(line[2])
                    dockerhub_info.append(temp)
                    cnt += 1
                print("└──[*] Select Docker Image: ", end="")
                target_dockerhub_num = input()
                target_dockerhub_num = int(target_dockerhub_num) - 1
                dockerhub_login.append(
                    dockerhub_info[target_dockerhub_num][0])  # Username
                dockerhub_login.append(
                    dockerhub_info[target_dockerhub_num][1])  # Password
                # target image
                dockerhub_tag = dockerhub_info[target_dockerhub_num][2]
                # print(dockerhub_login, dockerhub_tag)

                # make login cmd
                login_cmd = "sudo docker login -u "
                login_cmd = login_cmd + \
                    dockerhub_login[0] + " -p "+dockerhub_login[1]
                # print(login_cmd)

                # docker pull cmd
                docker_pull_cmd = "sudo docker pull"
                docker_pull_cmd = docker_pull_cmd + dockerhub_tag

                # docker run cmd
                docker_run_cmd = "sudo docker run -dit --name" + \
                    " worker-container" + dockerhub_tag

                # Run Command
                commands = ["sudo docker logout",
                            login_cmd,
                            "sudo docker info | grep Username",
                            docker_pull_cmd,
                            "sudo docker images",
                            "sudo docker ps -a",
                            docker_run_cmd,
                            "sudo docker ps -a"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


def data_in_out(target_ec2):
    # find .pem file
    print("\n==========[05] Data Injection & Get Results")
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
                commands = [
                    "sudo /transmission/evaluation.sh"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


def aws_sftp_receive(target_ec2):
    # find .pem file
    print(
        "\n==========[06] Receiver: File transmission (Worker (EC2) to Controller)")
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
                commands = ["ls /output", "sudo chmod -R 777 /output"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read().decode('ascii'))
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())

                # Download
                sftp = c.open_sftp()
                sftp.get("/output/evaluation.sh", "./output/evaluation.sh")

                c.close()


def clear_all(target_ec2):
    # find .pem file
    print("\n==========[XX] Cleaning...")
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
                commands = [
                    "sudo rm -rf /home/ubuntu/transmission",
                    "sudo rm -rf /transmission",
                    "sudo docker stop $(sudo docker ps -a -q)",
                    "sudo docker rm $(sudo docker ps -a -q)",
                    "sudo docker rmi $(sudo docker images -a -q)"
                ]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


if __name__ == "__main__":
    print("==========[00] Automated Controler Start")

    # Select ec2
    target_ec2 = get_aws_ec2_info()

    # ec2 connection & mkdir
    # aws_connect(target_ec2)

    # Send files (transmission)
    # aws_sftp_send(target_ec2)

    # Docker image & container making
    # docker_image_handling(target_ec2)

    # `transmission` data injection to docker container & make output
    # data_in_out(target_ec2)

    # Receive files
    aws_sftp_receive(target_ec2)

    # Docker container remove & delete transmission dir.
    # clear_all(target_ec2)
