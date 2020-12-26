#!/bin/sh
echo "temporäres Backup anlegen"
[ -e /tmp/backupG ] && rm -rf /tmp/backupG
mkdir /tmp/backupG
cp ~/.local/share/Gewicht/*.gnuplot /tmp/backupG
cp ~/.local/share/Gewicht/*.csv /tmp/backupG
cp ~/.local/share/Gewicht/*.png /tmp/backupG
echo "altes Programm löschen"
[ -e ~/.local/share/Gewicht ] && rm -rf ~/.local/share/Gewicht
cd ~/Downloads
echo "alte main.zip löschen"
[ -e main.zip ] && rm main.zip
echo "herunterladen ..."
wget https://github.com/Axel-Erfurt/Gewicht/archive/main.zip
echo "entpacken ..."
unzip main.zip
echo "verschiebe nach ~/local/share"
mv Gewicht-main ~/.local/share/Gewicht
echo "kopiere Icon nach .icons"
cp ~/.local/share/Gewicht/waage.png ~/.icons
echo "kopiere Starter nach ~/.local/share/applications"
cp ~/.local/share/Gewicht/Gewicht.desktop ~/.local/share/applications
echo "temporäres Backup zurückkopieren"
cp /tmp/backupG/*.csv ~/.local/share/Gewicht
cp /tmp/backupG/*.gnuplot ~/.local/share/Gewicht
cp /tmp/backupG/*.png ~/.local/share/Gewicht
echo "main.zip löschen"
[ -e main.zip ] && rm main.zip
echo "Ein Backup der alten CSV befindet sich im Benutzerordner"
