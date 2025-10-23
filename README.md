# 1.Versioning-Control

Steps:

New Project:

1. GitHub Desktop: Create new repository in the correct path with inizialized README, GitIgnore set to Python and License MIT. Then, push to GitHub.
2. PyCharm: Open the new project. In the gitignore file add the .idea folder by removing the # at the beginning of the line.
3. PyCharm Terminal: Use uv init & uv sync to create the virtual environment and sync the project. It creates the .venv directory, pyproject.toml and uv.lock files.
The generated .python-version and hello.py files can be deleted. Also in the .venv folder there is a .gitignore file that can be deleted, because the .venv folder is already excluded from the root.
4. PyCharm: Select the Python interpreter for the project: File > Settings > Python Interpreter > Add Interpreter > Existing environment > Select the uv interpreter python.exe file in the .venv/Scripts folder.
