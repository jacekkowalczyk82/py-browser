#!/bin/bash

# --- Function to check for command existence ---
command_exists () {
  command -v "$1" >/dev/null 2>&1
}

echo "Starting installation..."

# --- Attempt 1: Use Pipenv ---
if command_exists pipenv; then
  echo "✅ Pipenv detected. Installing dependencies using Pipenv..."
  
  # Check if a Pipfile exists
  if [ -f Pipfile ]; then
    pipenv install
    
    # Check for success
    if [ $? -eq 0 ]; then
      echo "✨ All Pipenv dependencies installed successfully."
      exit 0
    else
      echo "❌ Pipenv installation failed."
    fi
  else
    echo "⚠️ Pipfile not found. Falling back to requirements.txt..."
  fi
fi

# --- Attempt 2: Use Pip with requirements.txt ---
if [ -f requirements.txt ]; then
  echo "🛠️ Using standard pip to install from requirements.txt..."
  
  # Use python -m pip to ensure the correct pip is used
  python3 -m pip install -r requirements.txt
  
  # Check for success
  if [ $? -eq 0 ]; then
    echo "✨ All pip dependencies installed successfully."
    exit 0
  else
    echo "❌ Pip installation failed. Please check your environment or permissions."
    exit 1
  fi
else
  echo "❌ Could not find a Pipfile or requirements.txt."
  echo "Installation aborted. Please create a dependency file."
  exit 1
fi
