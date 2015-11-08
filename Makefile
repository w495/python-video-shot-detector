

test_detector:
	@python -m shot_detector.test_detector

clean:
	#
	#	Удаляем скомпилированные файлы байт-кода питона.
	#
	@find ./ -name "*~" -type f -exec rm -f {} \;
	@find ./ -name "*.pyc" -type f -exec rm -f {} \;
	@find ./ -name "*.pyo" -type f -exec rm -f {} \;
	@find ./ -name __pycache__ -type d -exec rm -rf {} \;

.PHONY: clean

