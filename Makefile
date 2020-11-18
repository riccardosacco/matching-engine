FOLDER=matching_engine

zip-layers:
	cd layers && \
	cd dependencies && zip -r ../zip/dependencies.zip python && \
	cd ../query_management && zip -r ../zip/query_management.zip python && \
	cd ../elasticsearch_metadata && zip -r ../zip/elasticsearch_metadata.zip python && \
	cd ../alias_management && zip -r ../zip/alias_management.zip python && \
	cd ../match_candidates && zip -r ../zip/match_candidates.zip python

create-venv:
	python3 -m venv ./venv && \
	source ./venv/bin/activate && \
	python3 -m pip install -U pip && \
	cd ${FOLDER} && \
	pip install -r requirements.txt && \
	pip install -r requirements.txt --target=dependencies && \
	python3 setup.py develop

remove-venv:
	rm -rf venv

