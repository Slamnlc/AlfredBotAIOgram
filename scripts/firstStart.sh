#!/bin/bash
sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram
mv /home/ubuntu/config.py /home/ubuntu/AlfredBotAIOgram/data/
mv /home/ubuntu/main.sql /home/ubuntu/AlfredBotAIOgram/
mv /home/ubuntu/yap.sql /home/ubuntu/AlfredBotAIOgram/
sed -i 's/127.0.0.1/db/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/postgres/maksim/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up --detach --build
sudo docker-compose exec -T db psql -c "create database alfredBot"
sudo docker-compose exec -T db psql -c "create database yaposhka"
sudo docker-compose exec -T db psql -U maksim alfredBot /var/lib/postgresql/main.sql
sudo docker-compose exec -T db psql -U maksim yaposhka /var/lib/postgresql/yap.sql
sudo sudo docker-compose up
