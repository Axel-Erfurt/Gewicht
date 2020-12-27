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
set samples 100
set tics font "Helvetica,8"
set terminal wxt size 900,500
plot "zeitraum.csv" index 0 u 1:2 w linespoints linestyle 1 notitle
set style line 5 lt rgb "#33ff33" lw 3 pt 6
set term pngcairo size 1200,800
set output "messung.png"
replot
