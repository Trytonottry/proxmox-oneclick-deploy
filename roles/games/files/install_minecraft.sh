#!/usr/bin/env bash
set -euo pipefail
MC_USER=mc
MC_HOME=/opt/minecraft
JAR_URL=${JAR_URL:-"https://purpur.org/download/latest/purpur.jar"}
JAR_NAME=server.jar
RAM=${RAM:-4G}
PORT=${PORT:-25565}
id -u $MC_USER &>/dev/null || useradd -r -m -d $MC_HOME -s /bin/false $MC_USER
mkdir -p $MC_HOME
chown $MC_USER:$MC_USER $MC_HOME
curl -L "$JAR_URL" -o $MC_HOME/$JAR_NAME
chown $MC_USER:$MC_USER $MC_HOME/$JAR_NAME
echo "eula=true" > $MC_HOME/eula.txt
chown $MC_USER:$MC_USER $MC_HOME/eula.txt
cat >/etc/systemd/system/minecraft.service <<EOF
[Unit]
Description=Minecraft server
After=network.target
[Service]
User=$MC_USER
WorkingDirectory=$MC_HOME
Nice=5
ExecStart=/usr/bin/java -Xmx${RAM} -Xms${RAM} -jar $JAR_NAME nogui
Restart=on-failure
RestartSec=10
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now minecraft.service
echo "Minecraft installed and started (port: $PORT, memory: $RAM)"
