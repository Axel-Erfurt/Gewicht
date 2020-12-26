# Gewicht
Gewichtskontrolle für Linux

### Voraussetzungen
- PyQt5
- gnuplot

<img src="https://raw.githubusercontent.com/Axel-Erfurt/Gewicht/main/screenshot.png" width="600" />

### Installation

- PyQt5 Installation

```sudo apt-get install python3-pyqt5```

- gnuplot Installation

```sudo apt-get install gnuplot gnuplot-x11 gnuplot-doc```

### Programm Installation

```cd ~/Downloads && wget https://raw.githubusercontent.com/Axel-Erfurt/Gewicht/main/Installer.sh && chmod +x ./Installer.sh && ./Installer.sh```

### Deinstallation

```rm -rf ~/.local/share/Gewicht```

### Bedienung

#### Toolbar 1

- neuer Eintrag

erstellt neue Teile am Ende mit dem Datum des folgenden Tages des letzen Eintrags

- Zeile löschen

löscht die markierte Zeile

- Programmordner öffnen

öffnet den Programmordner im Dateimanager

- Import

CSV importieren

- Export

CSV exportieren mit dem aktuellen Inhalt der Tabelle

#### Toolbar 2

- Datumswähler

zum Ändern des Zeitraums der angezeigt werden soll.

In das Feld klicken und Ziffern eingeben

Bei Tagen (erste 2 Ziffern) unter 10 eine 0 voranstellen, z.B 04

Springt automtisch weiter zu Monat und Jahr. Auch ein Weiterspringen mit TAB ist möglich.

Bei Falscheingabe noch einmal in das Feld klicken und Eingabe wiederholen.

- Plot

Das erste Plot Icon zeigt das externe Diagramm an.

Das zweite Plot Icon schaltet das interne Diagramm ein/aus.

Das Aussehen der Diagramme kann in den Dateien preview_intern.gnuplot und preview_extern.gnuplot angepasst werden.

siehe [Linetypes, colors, and styles](http://www.bersch.net/gnuplot-doc/linetypes,-colors,-and-styles.html)
