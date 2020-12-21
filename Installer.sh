#!/bin/sh
cd ~/Downloads
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

