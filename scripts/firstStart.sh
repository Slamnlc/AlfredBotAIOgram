sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram
mv /home/ubuntu/config.py /home/ubuntu/AlfredBotAIOgram/data/
mv /home/ubuntu/backUp.sql /home/ubuntu/AlfredBotAIOgram/
sed -i 's/127.0.0.1/db/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up --detach
sudo docker-compose exec db psql -U maksim -f /var/lib/postgresql/main.sql
sudo docker-compose exec db psql -U maksim -f /var/lib/postgresql/yap.sql
sudo sudo docker-compose up
