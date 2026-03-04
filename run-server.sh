#!/bin/bash

echo "========================================"
echo " Cognitive Load API Server"
echo "========================================"
echo ""
echo "Starting Flask server..."
echo "Server will be available at:"
echo "  - http://localhost:8080"
echo "  - http://$(hostname -I | awk '{print $1}'):8080"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

python3 app.py
