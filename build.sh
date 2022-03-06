#!/bin/bash
export $(cat  variables | xargs)

sudo amazon-linux-extras install ansible2
ssh-keygen -t rsa -f /etc/ssh/id_rsa
ssh-copy-id -i /etc/ssh/id_rsa.pub $SSH_USERNAME@$INSTANCE_1
ssh-copy-id -i /etc/ssh/id_rsa.pub $SSH_USERNAME@$INSTANCE_2
ssh-copy-id -i /etc/ssh/id_rsa.pub $SSH_USERNAME@$INSTANCE_3

systemctl restart sshd

echo "[WebApp]
$INSTANCE_1
$INSTANCE_2
$INSTANCE_3

[WebApp:vars]
ansible_user=$SSH_USERNAME
ansible_password=$SSH_PASSWORD" > /etc/ansible/hosts

sudo ansible-playbook docker.yml -kK

echo "FROM python:3.10
RUN pip install -r app/requirements.txt
ADD ./app/app.py /
CMD [ "python", "./app/app.py"]" > app/dockerfile

sudo systemctl start docker

sudo docker build -t /app/app .
