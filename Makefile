target = SubPy.py
path = ~/bin/$(target)
bashrc = ~/.bashrc

install:
	@bash -c "pip install rarfile"
	@cp $(target) $(path)
	@echo "alias SubPy='python $(path)'" >> $(bashrc)
	@bash -c "source $(bashrc)"
	@echo "SubPy is installed! Type 'SubPy' to run the script."
