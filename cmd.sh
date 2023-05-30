#!/bin/bash

python_path=/opt/miniconda3/envs/filmy/bin/python
manage_path=/opt/django_projects/filmy/manage.py
ip='192.168.100.240'
port=8765

if [[ "$1" == "restart" ]];then
    echo " ps -ef|grep ${python_path}|grep  manage.py|grep -q ${port}"
    if ps -ef|grep ${python_path}|grep  manage.py|grep -q ${port};then
        echo "process:"
        echo "ps -ef|grep ${python_path}|grep  manage.py|grep ${port}"
        echo `ps -ef|grep ${python_path}|grep  manage.py|grep ${port}`
        echo "process id:"
        echo "ps -ef|grep ${python_path}|grep  manage.py|grep ${port}|awk '{print \$2}'"
        echo `ps -ef|grep ${python_path}|grep  manage.py|grep ${port}|awk '{print \$2}'`
        echo "kill process..."
        ps -ef|grep ${python_path}|grep  manage.py|grep ${ip}:${port}|awk '{print $2}'|xargs kill -9
    fi
    echo "nohup ${python_path} ${manage_path} runserver ${ip}:${port} >> django.log 2>&1 &"
    nohup ${python_path} ${manage_path} runserver ${ip}:${port} >> django.log 2>&1 &
    if ps -ef|grep ${python_path}|grep  manage.py|grep -q ${port};then
        echo "server restart succ."
        echo "Starting development server at http://${ip}:${port}/"
    else
        echo "restart server failed."
    fi
elif [[ "$1" == "stop" ]];then
    echo " ps -ef|grep ${python_path}|grep  manage.py|grep -q ${port}"
    if ps -ef|grep ${python_path}|grep  manage.py|grep -q ${port};then
        echo "process:"
        echo "ps -ef|grep ${python_path}|grep  manage.py|grep ${port}"
        echo `ps -ef|grep ${python_path}|grep  manage.py|grep ${port}`
        echo "process id:"
        echo "ps -ef|grep ${python_path}|grep  manage.py|grep ${port}|awk '{print \$2}'"
        echo `ps -ef|grep ${python_path}|grep  manage.py|grep ${port}|awk '{print \$2}'`
        echo "kill process..."
        ps -ef|grep ${python_path}|grep  manage.py|grep ${ip}:${port}|awk '{print $2}'|xargs kill -9
        echo "kill process finished."
    else
        echo "no process running"
    fi
else
    echo "sub command [$1] not config. please use [restart][stop]"
fi
