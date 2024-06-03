# coffeemachine
A CLI Coffee Machine developed as part of a 100 day coding challenge.

## Installation

### with pipx
Test the cli app without permanently installing it:
   
     $ pipx run --spec git+https://github.com/philippesamuel/coffeemachine.git coffee

Install the command `snake-game` in your machine and execute it to play the game:
     
     $ pipx install git+https://github.com/philippesamuel/coffeemachine.git
     $ coffee

### with pip
1. Clone the repository
2. (Optional) Create a virtual environment with `python -m venv .venv` and activate 
   it with `source .venv/bin/activate` (Linux) or `.venv\Scripts\activate` (Windows)
3. Install the dependencies with `pip install -r requirements.txt`
4. Run the game with `python coffeemachine/main.py`

### with poetry
1. Clone the repository
2. (Optional) Create a virtual environment with `poetry shell` and activate it with 
   `poetry shell` or use venv with `poetry config virtualenvs.in-project true`
3. Install the dependencies with `poetry install`
4. Run the game with `poetry run python coffeemachine/main.py` or `python coffeemachine/main.py`
