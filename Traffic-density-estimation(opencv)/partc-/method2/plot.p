set datafile separator ","
set terminal png size 600,600
set output 'method2-utility.png'
set title "Method-2 Utility Runtime Analysis (1, 0.7, 0.4, 0.3)"
set xlabel "Error (absolute of the difference)"
set ylabel "Running Time (in s)"
set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5
plot "utility.txt" with linespoints linestyle 1

