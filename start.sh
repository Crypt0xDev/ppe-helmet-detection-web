#!/bin/bash
set -e

echo "📦 Installing dependencies..."
pip install --user -r requirements.txt

echo "🚀 Starting server..."
cd iape
python -m uvicorn src.app:app --host 0.0.0.0 --port $PORT
