# PHONY ALIASING
.PHONY: html, env, clean

# Commands
env :
	conda env update -n ligo -f environment.yml 
html : 
	myst build --html
clean : 
	rm -f figures/*
	rm -f audio/*
	rm -f _build/*