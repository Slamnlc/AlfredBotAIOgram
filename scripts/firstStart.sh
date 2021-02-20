sudo apt update
sed -i 's/127.0.0.1/172.31.11.161/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo docker-compose up --build
sudo docker-compose exec db psql -U maksim -f /var/lib/postgresql/backUp.sql
