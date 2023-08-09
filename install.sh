if [ ! -d /var/log/discord ]
then
    mkdir /var/log/discord
fi
chmod 777 /var/log/discord
cp role_bot.service /etc/systemd/system/
