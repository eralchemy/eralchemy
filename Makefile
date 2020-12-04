## deleting all Python garbage
clean:
	@echo "Cleaning up ..."
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +

## black formatting
format_black:
	@echo "Black formatting ..."
	@black .

## prettier formatting
format_prettier:
	@echo "Prettier formatting ..."
	@npx prettier --write "**/*.{json,yaml,yml}"

## formatting
format: format_black format_prettier

## black linting
lint_black:
	@echo "Black linting ..."
	@black --check .

## prettier formatting
lint_prettier:
	@echo "Prettier linting ..."
	@npx prettier --check "**/*.{json,yaml,yml}"

## pylint linting
lint_pylint:
	@echo "Pylint linting ..."
	@poetry run pylint bigquery_erd

## linting
lint: lint_black lint_prettier lint_pylint
