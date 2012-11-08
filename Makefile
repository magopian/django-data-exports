test:
	coverage run --branch --source=data_exports `which django-admin.py` test data_exports
	coverage report --omit=data_exports/test* --omit=data_exports/migrations/*
