# Sorting Algorithm Complexity Analysis Tool (SACAT)

Prototype of a tool useful for time and space complexity analysis of sorting algorithms.
The current version is available as a desktop GUI application, fully crossplatform. Currently available for Python versions 3.8+.


# Running the prototype

Step by step guide for running the application.

## With a virtual environment (For Linux and MACOS systems)
In a terminal:
- Move into the directory `sacat_project/`.
- Ensure correct version of python is installed using `python3 --version` (Alernatively use `python --version`). Only Python versions 3.8+ are guaranteed to work.
- Install `virtualenv` package for Python3 using pip with the following command: `python3 -m pip install virtualenv`.
- Create a new virtual environment in the directory `sacat_project/` using the following command: `virtualenv venv`.
- Activate the virtual environment using `source venv/bin/activate`.
- Install all requirements for the projects using `pip install -r requirements.txt`.
- Run the program using `python3 run.py`.

When no longer running the program, deactivate the virtual environment using the command `deactivate`.

## With a virtual environment (For Windows systems)

Follow the same istructions as above, but instead of using the alias `python3`, use `py`.

Additionally the structure of the virtual environment will be different, so running the virtual environment will require this command: `venv\Scripts\activate.bat`.
