#!/bin/bash
sudo docker stop $(sudo docker ps -a -q)
git pull origin master -r
sudo docker-compose up
