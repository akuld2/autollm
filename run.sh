echo "Starting setup..."
python -m pip install EdgeGPT --upgrade > /dev/null 2>&1
echo "Setup done. Starting run..."
python get_code_snippets.py