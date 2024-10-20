start:
	PYTHONPATH=src poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

token:
	PYTHONPATH=src poetry run python src/generate_token_demo.py