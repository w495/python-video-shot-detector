clean:
	#
	#	Удаляем скомпилированные файлы байт-кода питона.
	#
	@find ./ -name "*~" -type f -exec rm -f {} \;
	@find ./ -name "*.pyc" -type f -exec rm -f {} \;
	@find ./ -name "*.pyo" -type f -exec rm -f {} \;
	@find ./ -name __pycache__ -type d -exec rm -rf {} \;

.PHONY: clean



install
    conda install -c soft-matter pyav=v0.2.3.post0
    conda install -c danielballan pyav
