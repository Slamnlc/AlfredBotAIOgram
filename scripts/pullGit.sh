#!/bin/bash
sudo docker system prune -a -f
sudo docker stop $(sudo docker ps -a -q)
git pull origin master -r
sudo docker-compose up
