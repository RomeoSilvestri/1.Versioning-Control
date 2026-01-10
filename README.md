# 1.Versioning-Control

This guide describes the recommended workflow for setting up and managing Python projects with GitHub, GitLab, PyCharm, and `uv`.

## Creating a New Project (GitHub)

1. **GitHub Desktop**:  
   - Create a new repository in the desired path.
   - Initialize with a README, set `.gitignore` to Python, and choose the MIT License.
   - Push the repository to GitHub.

2. **PyCharm**:  
   - Open the new project via `File > Open...` and select the project folder.

3. **Virtual Environment**:  
   - Create a new virtual environment using `uv`.
   - In PyCharm: `Add New Interpreter > Add Local Interpreter`, select `Environment: New`, and choose `Type: uv`.

4. **Dependencies**:  
   - Open the terminal and run `uv sync` to synchronize dependencies.
   - This will generate `pyproject.toml` and `uv.lock`.

5. **.gitignore**:  
   - Ensure the `.idea` folder is ignored by uncommenting the corresponding line in `.gitignore`.

6. **Optional**:  
   - Create a `main.py` file.
   - Add a run configuration: `Run > Edit Configurations... > Add New > uv run`, set a name (e.g., `main`), and select `Script: main.py`.

---

## Creating a New Project (GitLab)

1. **GitLab**:  
   - Create a new repository: `New Project > Create blank project`.
   - Set the project name, URL, and visibility.
   - Initialize the repository with a README.

2. **GitHub Desktop**:  
   - Clone the GitLab repository: `File > Clone Repository... > URL`, paste the GitLab repository URL, and select the local path.
   - The URL can be found in GitLab under `Project > Repository > Files > Clone > Clone with HTTPS`.

3. **Continue from Step 2** of the GitHub workflow above.

---

## Working with an Existing Project

1. **GitHub Desktop**:  
   - Clone the existing repository: `File > Clone Repository... > GitHub.com` (for GitHub) or `URL` (for GitHub or GitLab), paste the repository URL, and select the local path.

2. **Continue from Step 2** of the GitHub workflow above.

---

## Notes

- Use `uv add <package>` to add a new dependency to your project. This updates `pyproject.toml` and `uv.lock` automatically.
- Use `uv remove <package>` to remove a dependency from your project. Use `uv update` to update all dependencies to their latest compatible versions.
- Use `uv sync` to install or update all project dependencies defined in `pyproject.toml` / `uv.lock`.
- Use `uv run <script>` to execute scripts (e.g., `uv run main.py`). Uv will automatically install only the missing dependencies required for that script.
- For further customization, refer to the official documentation of [PyCharm](https://www.jetbrains.com/pycharm/), [GitHub Desktop](https://desktop.github.com/), and [uv](https://github.com/astral-sh/uv).