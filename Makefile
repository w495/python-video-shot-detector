
save-conda-env-py27:
	$(call save_conda_env,py27);

save-conda-env-py34:
	$(call save_conda_env,py34);

build: conda_build python_build

conda_build:
	conda build conda-recipe

python_build:
	python setup.py sdist

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



.PHONY: clean clean_logs save-conda-env-py27 save-conda-env-py34

define save_conda_env
	# ----------------------------------------------------------------
	# 1/4 Save conda environment for $(1)
	# ----------------------------------------------------------------
	conda env export \
		> "./requirements/$(1)/shot-detector.yml";
	# ----------------------------------------------------------------
	# 2/4 Save conda package list for $(1)
	# ----------------------------------------------------------------
	conda list -e \
		> "./requirements/$(1)/requirements-conda.txt";
	# ----------------------------------------------------------------
	# 3/4 Save conda explicit package list for $(1)
	# ----------------------------------------------------------------
	conda list --explicit \
		> "./requirements/$(1)/requirements-conda-explicit.txt"
	# ----------------------------------------------------------------
	# 4/4 Save pip explicit package list for $(1)
	# ----------------------------------------------------------------
	pip freeze \
		> "./requirements/$(1)/requirements-pip.txt";
	@echo
endef

