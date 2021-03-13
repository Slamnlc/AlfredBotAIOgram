#!/bin/bash
sudo timedatectl set-timezone Europe/Kiev
sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram

mv /home/config.py /home/AlfredBotAIOgram/data/
sudo mv /home/backup.sql /home/AlfredBotAIOgram/
sudo mv /home/.env /home/AlfredBotAIOgram/
sudo mv /home/makeBackUp.sh /home/AlfredBotAIOgram/scripts/
sudo chmod 0644 /home/AlfredBotAIOgram/scripts/makeBackUp.sh

sed -i 's/127.0.0.1/db/g' /home/AlfredBotAIOgram/data/config.py
sed -i 's/\/Users\/maksim\/CurrencyBot\/images/\/images/g' /home/AlfredBotAIOgram/data/config.py
sed -i 's/alfredBot/alfredbot/g' /home/AlfredBotAIOgram/data/config.py
sed -i 's/1437484062:AAFYAEQCs3T7723uIEX6lQOiJfjK0QhaXNc/1678753173:AAFph0Mx901NE7fCA1BPAoeQDYXIE7e3wiU/g' /home/AlfredBotAIOgram/data/config.py

# shellcheck disable=SC2164
cd /home/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up --detach --build
sudo docker-compose exec -T db psql -U postgres  -f /var/lib/postgresql/backup.sql
sudo sudo docker-compose up
