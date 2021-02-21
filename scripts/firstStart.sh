#!/bin/bash
sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram
mv /home/ubuntu/config.py /home/ubuntu/AlfredBotAIOgram/data/
mv /home/ubuntu/main.sql /home/ubuntu/AlfredBotAIOgram/
mv /home/ubuntu/yap.sql /home/ubuntu/AlfredBotAIOgram/
sed -i 's/127.0.0.1/db/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/postgres/maksim/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/alfredBot/alfredbot/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/1437484062:AAFYAEQCs3T7723uIEX6lQOiJfjK0QhaXNc/1678753173:AAFph0Mx901NE7fCA1BPAoeQDYXIE7e3wiU/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up --detach --build
sudo docker-compose exec -T db psql -c "create database alfredbot"
sudo docker-compose exec -T db psql -c "create database yaposhka"
sudo docker-compose exec -T db psql -U maksim alfredbot < ./main.sql
sudo docker-compose exec -T db psql -U maksim yaposhka < ./yap.sql
sudo sudo docker-compose up
