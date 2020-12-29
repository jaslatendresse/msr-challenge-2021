#!/bin/bash

echo "----- clean -----"
rm -f msr-challenge-2020.aux msr-challenge-2020.bbl msr-challenge-2020.blg msr-challenge-2020.log msr-challenge-2020.out msr-challenge-2020.tex

echo "----- pandoc -----"
pandoc -s -F pandoc-crossref --natbib meta.yaml --template=acmwrapper.tex -N -f markdown+raw_tex+tex_math_dollars+citations -t latex -o msr-challenge-2020.tex msr-challenge-2020.md

echo "----- pdflatex (1st pass) -----"
pdflatex msr-challenge-2020.tex

echo "----- bibtex -----"
bibtex msr-challenge-2020

echo "----- pdflatex (2nd pass) -----"
pdflatex msr-challenge-2020.tex

echo "----- pdflatex (3rd pass) -----"
pdflatex msr-challenge-2020.tex