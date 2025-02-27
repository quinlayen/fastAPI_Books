#!/bin/bash

ENV_NAME="fastapi_env"

if [ ! -d "$ENV_NAME" ]; then
    python3 -m venv $ENV_NAME
fi

source $ENV_NAME/bin/activate

pip install --upgrade pip

mkdir -p backend frontend

# Ensure log files exist and have write permissions
touch backend/fastapi.log frontend/streamlit.log
chmod 666 backend/fastapi.log frontend/streamlit.log

echo "Environment setup complete."
echo "Run 'source $ENV_NAME/bin/activate' to activate the environment."

