#!/bin/bash
sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram

mv /home/ubuntu/config.py /home/ubuntu/AlfredBotAIOgram/data/
sudo mv /home/ubuntu/backup.sql /home/ubuntu/AlfredBotAIOgram/
#sudo mv /home/ubuntu/alfred.sql /home/ubuntu/AlfredBotAIOgram/
sudo mv /home/ubuntu/.env /home/ubuntu/AlfredBotAIOgram/
sudo mv /home/ubuntu/makeBackUp.sh /home/ubuntu/AlfredBotAIOgram/scripts/

sed -i 's/127.0.0.1/db/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/\/Users\/maksim\/CurrencyBot\/images/\/images/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/alfredBot/alfredbot/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
sed -i 's/1437484062:AAFYAEQCs3T7723uIEX6lQOiJfjK0QhaXNc/1678753173:AAFph0Mx901NE7fCA1BPAoeQDYXIE7e3wiU/g' /home/ubuntu/AlfredBotAIOgram/data/config.py

# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up --detach --build
#sudo docker-compose exec -T db psql -U postgres -c 'create database alfredbot'
#sudo docker-compose exec -T db psql -U postgres -c 'create database yaposhka'
sudo docker-compose exec -T db psql -U postgres  -f /var/lib/postgresql/backup.sql
#sudo docker-compose exec -T db psql -U postgres -d alfredbot -f /var/lib/postgresql/alfred.sql
sudo sudo docker-compose up
