set datafile separator ","
set terminal png size 600,600
set output 'method4-2.png'
set title "Method-4 2 Thread Queue Density "
set xlabel "Time (in s)"
set ylabel "Queue Density"
set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 
plot "2.txt" with linespoints linestyle 1

