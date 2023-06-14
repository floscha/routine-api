# Don't change
SRC_DIR := routine
TEST_DIR := tests
RUN_CMD := poetry run

help:  ## 💬 This help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

check: .  ## 🔎 Lint & format, will not fix but sets exit code on error 
	$(RUN_CMD) black --check $(SRC_DIR) $(TEST_DIR) && \
	$(RUN_CMD) ruff $(SRC_DIR) $(TEST_DIR) && \
	$(RUN_CMD) mypy $(SRC_DIR)

format: .  ## 📜 Lint & format, will try to fix errors and modify code
	$(RUN_CMD) black $(SRC_DIR) $(TEST_DIR) && \
	$(RUN_CMD) ruff --fix $(SRC_DIR) $(TEST_DIR)

test: .  ## 🎯 Run tests
	$(RUN_CMD) pytest $(TEST_DIR)

test-verbose: .  ## 🎯 Run tests with verbose output
	$(RUN_CMD) pytest -vv -s $(TEST_DIR)
