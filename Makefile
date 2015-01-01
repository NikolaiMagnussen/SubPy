target = SubPy.py
path = ~/bin/$(target)
bashrc = ~/.bashrc

install:
	@cp $(target) $(path)
	@echo "alias SubPy='python $(path)'" >> $(bashrc)
	@bash -c "source $(bashrc)"
	@echo "SubPy is installed! Type 'SubPy' to run the script."
