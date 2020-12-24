TITLE = "Messungen"
set title TITLE offset char 0, char -1
set datafile separator '\t' # Setze das Trennzeichen in der CSV
set xdata time  # Setze die X-Achse als Zeitachse
set timefmt "%Y%m%d" # Setze das Format der Datumsangabe
set format x "%d.%m.%y"
set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5
set tics font "Helvetica,8"
set term pngcairo background "#e9e9e9" size 900,400
set output "messung.png"
plot "zeitraum.csv" u 1:2 w linespoints linestyle 1 notitle
replot
