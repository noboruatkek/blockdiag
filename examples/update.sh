#!/bin/sh

EXAMPLES=`dirname $0`
BLOCKDIAG=$EXAMPLES/../bin/blockdiag

for diag in `ls $EXAMPLES/*.diag`
do
    png=$EXAMPLES/`basename $diag .diag`.png
    echo $BLOCKDIAG -Tpng -o $png $diag
    $BLOCKDIAG -Tpng -o $png $diag

    svg=$EXAMPLES/`basename $diag .diag`.svg
    echo $BLOCKDIAG -Tsvg -o $svg $diag
    $BLOCKDIAG -Tsvg -o $svg $diag

    pdf=$EXAMPLES/`basename $diag .diag`.pdf
    echo $BLOCKDIAG -Tpdf -o $pdf $diag
    $BLOCKDIAG -Tpdf -o $pdf $diag
done
