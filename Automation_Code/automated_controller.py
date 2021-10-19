import csv
import os
import time
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
                dockerhub_info = []
                target_dockerhub_num = "0"
                while(target_dockerhub_num == "0"):
                    f = open("./private/dockerhub_info.csv",
                             "r", encoding="utf-8")
                    lines = csv.reader(f)
                    next(lines, None)
                    cnt = 1
                    dockerhub_info = []

                    print("└─[+] Dockerhub Info. read")
                    for line in lines:
                        print("└─[*]", cnt, ":", line[0],
                              "|", line[1], "|", line[2])
                        temp = []
                        temp.append(line[0])
                        temp.append(line[1])
                        temp.append(line[2])
                        dockerhub_info.append(temp)
                        cnt += 1
                    print("└──[*] Select Docker Image, ", end="")
                    target_dockerhub_num = input("\"0\" call a new list: ")

                target_dockerhub_num = int(target_dockerhub_num) - 1
                dockerhub_login.append(
                    dockerhub_info[target_dockerhub_num][0])  # Username
                dockerhub_login.append(
                    dockerhub_info[target_dockerhub_num][1])  # Password
                # target image
                dockerhub_tag = dockerhub_info[target_dockerhub_num][2]

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

    return dockerhub_tag


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
                    "bash /transmission/sed.sh",
                    "bash /transmission/evaluation.sh"]
                for command in commands:
                    print("└─[*] Executing: {}".format(command))
                    stdin, stdout, stderr = c.exec_command(command)
                    print("└─[+]", stdout.read())
                    print("└──[*] Errors & Warnings")
                    print("└──[-]", stderr.read())
                c.close()


def aws_sftp_receive(target_ec2, dockerhub_tag):
    # find .pem file
    print(
        "\n==========[06] Receiver: File transmission (Worker (EC2) to Controller)")
    default_local_path = "./output"
    replace_token_list = "{}[]\"\'/: "
    for remove_char in replace_token_list:
        dockerhub_tag = dockerhub_tag.replace(remove_char, "_")
    default_local_path += dockerhub_tag
    try:
        if not os.path.exists(default_local_path):
            os.makedirs(default_local_path)
    except OSError:
        print("└─[-] Error: Failed to create the directory.")

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
                commands = ["ls /output"]
                output_list = []

                print("└─[*] Executing: {}".format(commands[0]))
                stdin, stdout, stderr = c.exec_command(commands[0])
                print("└─[+]", stdout.read())
                stdin, stdout, stderr = c.exec_command(commands[0])
                output_list = stdout.read().decode('ascii').split("\n")
                output_list.remove('')
                print("└──[*] Errors & Warnings")
                print("└──[-]", stderr.read())

                # Download
                sftp = c.open_sftp()
                print("└─[*] Receive targets:", output_list)
                for entry in output_list:
                    print("└──[*] Receiving target:", entry, end=' ')
                    ec2_path = "/output/"
                    ec2_path += entry
                    print(ec2_path)
                    local_path = os.path.join(default_local_path, "/", entry)
                    sftp.get(ec2_path, local_path)

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
                    "sudo rm -rf /output",
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

    # Docker container remove & delete transmission dir.
    clear_all(target_ec2)

    # ec2 connection & mkdir
    aws_connect(target_ec2)

    # Send files (transmission)
    aws_sftp_send(target_ec2)

    # Docker image & container making
    dockerhub_tag = docker_image_handling(target_ec2)

    # `transmission` data injection to docker container & make output
    data_in_out(target_ec2)

    # Receive files
    aws_sftp_receive(target_ec2, dockerhub_tag)

    # Docker container remove & delete transmission dir.
    # clear_all(target_ec2)
