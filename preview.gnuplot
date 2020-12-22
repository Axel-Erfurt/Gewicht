TITLE = "Messungen"
set title TITLE offset char 0, char -1
set datafile separator '\t' # Setze das Trennzeichen in der CSV
set xdata time  # Setze die X-Achse als Zeitachse
set timefmt "%Y%m%d" # Setze das Format der Datumsangabe
set format x "%d.%m.%y"
plot "~/.local/share/Gewicht/zeitraum.csv" index 0 u 1:2 w filledcurves below y1=88 lt 2 notitle, "~/.local/share/Gewicht/zeitraum.csv" index 0 u 1:2 w filledcurves above y1=88 lt 7 notitle
