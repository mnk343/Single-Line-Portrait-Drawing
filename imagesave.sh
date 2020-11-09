cd stippling/Final_Output
for d in */ ; do
    cd $d
    echo "$d"
    for f in file*; do
        python3 /home/aman/Desktop/sem7/Graphics/project/Single-Line-Portrait-Drawing/bezier_curve/curve.py $f
    done
    cd ..
done