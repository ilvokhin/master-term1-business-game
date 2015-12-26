# Makefile for LaTeX presentation

tex = src/main.tex
pdf = main.pdf
pics = pics

# targets
all: $(pdf)

read:
	open $(pdf)

main.pdf: $(tex) $(pics)
	latexmk -pdf -pdflatex="pdflatex -interactive=nonstopmode" -use-make $(tex)

clean:
	latexmk -c $(pdf)
	rm -rf main.*

.PHONY: all read clean
