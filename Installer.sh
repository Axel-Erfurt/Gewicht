#!/bin/sh
echo "alte csv und preview kopieren"
[ -e ~/.local/share/Gewicht/Gewicht.csv ] && cp ~/.local/share/Gewicht/Gewicht.csv /tmp/Gewicht.csv
[-e ~/.local/share/Gewicht/preview_extern.gnuplot] && cp ~/.local/share/Gewicht/preview_extern.gnuplot /tmp/preview_extern.gnuplot
[-e ~/.local/share/Gewicht/preview_intern.gnuplot] && cp ~/.local/share/Gewicht/preview_intern.gnuplot /tmp/Gewicht_preview_intern.gnuplot
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
echo "alte csv und preview zurückkopieren"
[ -e /tmp/Gewicht.csv ] && mv /tmp/Gewicht.csv ~/.local/share/Gewicht/Gewicht.csv 
[ -e /tmp/preview_extern.gnuplot ] && mv /tmp/preview_extern.gnuplot ~/.local/share/Gewicht/preview_extern.gnuplot
[ -e /tmp/preview_extern.gnuplot ] && mv /tmp/Gewicht_preview_intern.gnuplot ~/.local/share/Gewicht/preview_intern.gnuplot
echo "main.zip löschen"
[ -e main.zip ] && rm main.zip
