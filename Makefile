
define save_conda_env
	conda env export \
		> "./requirements/$(1)/shot-detector.yml";
	conda list -e \
		> "./requirements/$(1)/requirements-conda.txt";
	conda list --explicit \
		> "./requirements/$(1)/requirements-conda-explicit.txt"
	pip freeze \
		> "./requirements/$(1)/requirements-pip.txt";
	@echo save_conda_env
endef


save-conda-env-py27:
	$(call save_conda_env,py27)


save-conda-env-py34:
	$(call save_conda_env,py34)

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


.PHONY: clean clean_logs save-27
