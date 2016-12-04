#!/bin/bash

if hash python3 2>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

./halite -d "30 30" "${PYTHON_CMD} MyBot.py Randominator random" "${PYTHON_CMD} MyBot.py Overkilla overkill debug"
