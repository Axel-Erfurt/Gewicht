#TITLE = "Messungen"
#set title TITLE offset char 0, char -1
set datafile separator '\t' # Setze das Trennzeichen in der CSV
set xdata time  # Setze die X-Achse als Zeitachse
set timefmt "%Y%m%d" # Setze das Format der Datumsangabe
set format x "%d.%m.%y"
set style line 1 lc rgb '#729fcf'
set style fill solid border lt -1 
#set boxwidth 0.9 absolute
set tics font "Helvetica,8"
set term pngcairo background "#e9e9e9" size 1200,400
set output "messung_intern.png"
plot "zeitraum.csv" u 1:2 with lines linestyle 1 notitle
replot
