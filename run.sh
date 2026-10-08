#!/usr/bin/env bash
set -e

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

cat <<'EOF' > .env
ADDRESS=127.0.0.1
PORT=5000
EOF

kill -9 $(lsof -t -i :5000) 2>/dev/null

coverage run -m unittest test.py
coverage report -m

python3 run.py