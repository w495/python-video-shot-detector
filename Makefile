clean:
	#
	#	Delete python bytecode files.
	#
	@find ./ -name '__pycache__' -type d -exec rm -rf {} +
	@find ./ -name "*~" -type f -exec rm -f {} \;
	@find ./ -name "*.pyc" -type f -exec rm -f {} \;
	@find ./ -name "*.pyo" -type f -exec rm -f {} \;


clean_logs:
	#
	#	Delete logs.
	#
	@find ./ -name "*.log" -type f -exec rm -f {} \;


.PHONY: clean clean_logs
