for i in `ls *.html`
do
    echo $i
    python importmenu.py $i
done
