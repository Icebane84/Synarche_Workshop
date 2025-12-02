#!/bin/bash
# setup_prs_db.sh
# Created: 2026-02-23 02:23:45 EST
#
# This script automates the setup of a Python virtual environment,
# installs necessary packages, and initializes a PostgreSQL
# database directory structure within the current project folder.

# --- What: Define Variables ---
# How: Set the names for the virtual environment directory and the database directory.
# Why: Using variables makes the script easier to read and modify.
VENV_DIR=".venv_prs"
DB_DIR="prs_database"

echo "--- Starting PostgreSQL Database Setup for PRS ---"

# --- What: Create Python Virtual Environment ---
# How: Check if the virtual environment directory exists. If not, create it using python3 -m venv.
# Why: A virtual environment isolates project dependencies, preventing conflicts with other Python projects.
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating Python virtual environment in '$VENV_DIR'..."
  python3 -m venv "$VENV_DIR"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment. Please ensure Python 3 and venv are installed."
    exit 1
  fi
else
  echo "Virtual environment '$VENV_DIR' already exists."
fi

# --- What: Activate Virtual Environment ---
# How: Source the activation script within the virtual environment's bin directory.
# Why: Activating the environment makes its Python interpreter and installed packages available in the current shell.
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
  echo "Error: Failed to activate virtual environment."
  exit 1
fi

# --- What: Install Required Packages ---
# How: Use pip to install 'pgserver' and 'psycopg2-binary' within the active virtual environment.
# Why: 'pgserver' provides an embedded PostgreSQL server, and 'psycopg2-binary' is the PostgreSQL adapter for Python.
echo "Installing pgserver and psycopg2-binary..."
pip install pgserver psycopg2-binary
if [ $? -ne 0 ]; then
  echo "Error: Failed to install required packages."
  deactivate
  exit 1
fi

# --- What: Initialize Database Directory ---
# How: Check if the database directory exists. If not, create it and initialize a pgserver instance within it.
# Why: This creates the necessary file structure for the embedded PostgreSQL database.
if [ ! -d "$DB_DIR" ]; then
  echo "Initializing PostgreSQL database directory in '$DB_DIR'..."
  mkdir "$DB_DIR"
  pgserver init "$DB_DIR"
  if [ $? -ne 0 ]; then
    echo "Error: Failed to initialize database directory with pgserver."
    deactivate
    exit 1
  fi
  echo "Database directory initialized. You can start the server using: pgserver run $DB_DIR"
else
  echo "Database directory '$DB_DIR' already exists."
  echo "If you want to re-initialize, please remove the directory first."
  echo "You can start the server using: pgserver run $DB_DIR"
fi

# --- What: Deactivate Virtual Environment ---
# How: Call the 'deactivate' command.
# Why: It's good practice to deactivate the virtual environment when the script is done.
echo "Deactivating virtual environment..."
deactivate

echo "--- Setup Complete ---"
echo "To activate the environment later, run: source $VENV_DIR/bin/activate"
echo "To start the database server, first activate the environment, then run: pgserver run $DB_DIR"
