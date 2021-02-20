sudo apt-get update
git clone https://github.com/Slamnlc/AlfredBotAIOgram
mv /home/ubuntu/config.py /home/ubuntu/AlfredBotAIOgram/data/
mv /home/ubuntu/backUp.sql /home/ubuntu/AlfredBotAIOgram/
sed -i 's/127.0.0.1/172.31.11.161/g' /home/ubuntu/AlfredBotAIOgram/data/config.py
# shellcheck disable=SC2164
cd /home/ubuntu/AlfredBotAIOgram/
sudo snap install docker
sudo sudo docker-compose up -d
sudo docker-compose exec db psql -U maksim -f /var/lib/postgresql/backUp.sql
#sudo sudo docker-compose up
