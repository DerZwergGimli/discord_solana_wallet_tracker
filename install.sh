#!/bin/bash

useradd pythonBOT
chown -r pwd python


echo "[Unit]
Description=DiscordSolanaWalletBot
After=multi-user.target

[Service]
User=pythonBOT
Group=pythonBOT
WorkingDirectory=$(pwd)
VIRTUAL_ENV=$(pwd)/venv
Environment=PATH=$VIRTUAL_ENV/bin:$PATH
ExecStart=$(pwd)/venv/bin/python wallet_tracker_solana.py
Restart=on-failure

[Install]
WantedBy=multi-user.target" > /etc/systemd/system/discordwalletbot.service


systemctl daemon-reload
systemctl enable discordwalletbot.service
systemctl start discordwalletbot.service
systemctl status discordwalletbot.service

echo "DONE"