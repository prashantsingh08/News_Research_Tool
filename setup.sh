#!/bin/bash
# ============================================================
# setup.sh  —  One-click setup (Mac / Linux)
# Run: bash setup.sh
# ============================================================
set -e
echo ""
echo "========================================"
echo "  📰 News Research Tool — Setup"
echo "========================================"
echo ""
echo "✅ [1/5] Checking Python..."
python3 --version || { echo "❌ Python3 not found."; exit 1; }

echo "✅ [2/5] Creating virtual environment..."
python3 -m venv venv
echo "   Created: ./venv/"

echo "✅ [3/5] Activating venv..."
source venv/bin/activate

echo "✅ [4/5] Upgrading pip & installing packages..."
pip install --upgrade pip -q
pip install -r requirements.txt

echo "✅ [5/5] .env already contains your API keys."
echo ""
echo "========================================"
echo "  🎉 Setup Complete!"
echo "========================================"
echo ""
echo "  Run the app:"
echo "    source venv/bin/activate"
echo "    streamlit run app.py"
echo ""
