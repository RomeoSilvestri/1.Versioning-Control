# 1.Versioning-Control

Steps:

New Project:

1. GitHub Desktop: Create new repository in the correct path with inizialized README, GitIgnore set to Python and License MIT. Then, push to GitHub.
2. PyCharm: Open the new project. Use File -> Open... and select the project folder.
3. Generate new virtual environment and select it as interpreter with uv. Add New Interpreter > Add Local Interpreter, select Environment: Generate new, Type: uv.  
4. Terminal: Invoke uv sync to sync the project. It creates the pyproject.toml and uv.lock files.
5. In the gitignore file add the .idea folder by removing the # at the beginning of the line.
(Optionally) Create a main.py file and add a configuration for uv run: Current File > Edit Configurations... > Add new > uv run, set a name (e.g., main) and select Script: main.py.

New Project GitLab:

0. GitLab: Create new repository. Use New Project > Create blank project. Set Project name, Project URL, Visibility Level. Inizialize repository with a README.
1. GitHub Desktop: Clone the GitLab repository. Use File > Clone Repository... > URL tab, paste the GitLab repository URL and select the local path. You can find the URL in GitLab under Project > Repository > Files > Clone > Clone with HTTPS.
All the other steps are the same as New Project from step 2.

Existing Project:

1. GitHub Desktop: Clone the existing repository. Use File > Clone Repository... > GitHub.com (already available) or URL (GitHub o GitLab) tab, paste the repository URL and select the local path.
All the other steps are the same as New Project from step 2.