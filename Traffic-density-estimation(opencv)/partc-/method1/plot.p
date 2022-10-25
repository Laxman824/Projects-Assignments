set datafile separator ","
set terminal png size 500,500
set output 'method1-utility.png'
set title "Method-1 Utility Runtime Analysis"
set xlabel "Error (absolute of the difference)"
set ylabel "Running Time (in s)"
set style line 1 \
    linecolor rgb '#0060ad' \
    linetype 1 linewidth 2 \
    pointtype 7 pointsize 1.5
plot "utility.txt" with linespoints linestyle 1

