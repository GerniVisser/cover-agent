#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Exit if any command in a pipeline fails
set -x  # Print commands and their arguments as they are executed

# Default model name
MODEL="gpt-4o"
RUN_INSTALLER=false

# Function to display usage
usage() {
    echo "Usage: $0 [--model model_name] [--run-installer]"
    echo "  --model model_name      Set the model name (default: gpt-3.5-turbo)"
    echo "  --run-installer         Run the installer within a Docker container"
    exit 1
}

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift
            ;;
        --run-installer)
            RUN_INSTALLER=true
            ;;
        *)
            usage
            ;;
    esac
    shift
done

# Conditional Docker commands
if [ "$RUN_INSTALLER" = true ]; then
    # Build the installer within a Docker container
    docker build -t cover-agent-installer -f Dockerfile .

    # Run the Docker container with the current user's ID and group ID
    mkdir -p dist
    docker run --rm --volume "$(pwd)/dist:/app/dist" cover-agent-installer
fi

# Python FastAPI Example
sh tests_integration/test_with_docker.sh \
  --dockerfile "templated_tests/python_fastapi/Dockerfile" \
  --source-file-path "app.py" \
  --test-file-path "test_app.py" \
  --test-command "pytest --cov=. --cov-report=xml --cov-report=term" \
  --model "gpt-3.5-turbo"