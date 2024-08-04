#!/bin/bash

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_DIR=$(realpath "$CWD")
cd "$APP_DIR" || exit 1

uvicorn main:app --reload --host 0.0.0.0 --port 8080
