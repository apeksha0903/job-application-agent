# Environment Setup

## Operating System

Windows

## Development Environment

* Windows
* VS Code
* Git
* Python
* Python virtual environment

## Python Versions

Multiple Python versions are installed on the development machine.

The project uses:

Python 3.12

The Python launcher is used to explicitly create the project environment with Python 3.12.

## Project Location

C:\Users\Apeksha\Documents\job-application-agent

## Virtual Environment

The project environment was created using:

py -3.12 -m venv .venv

The environment is activated using:

.venv\Scripts\activate

## Verification

Python version inside the virtual environment:

python --version

Expected:

Python 3.12.x

## Reason for Using a Virtual Environment

The virtual environment isolates project dependencies from other Python projects installed on the machine.

This prevents dependency conflicts and makes the project easier to reproduce on another machine.

## Version Control

Git is used for source control.

The repository is initialized at the project root.

Sensitive files such as .env must never be committed.

## Current Environment

Python:
3.12.0

Git:
2.43.0.windows.1

VS Code:
1.136.1

## Setup Status

Initial environment setup completed.

## Next Step

Initialize the first Git commit and install the initial project dependencies.
