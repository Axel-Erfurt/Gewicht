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

Das Aussehen des Diagramms kann in den Dateien preview_intern.gnuplot und preview_extern.gnuplot angepasst werden.

siehe [Linetypes, colors, and styles](http://www.bersch.net/gnuplot-doc/linetypes,-colors,-and-styles.html)
