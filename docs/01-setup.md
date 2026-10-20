# 01 · Set up a project

[Contents](../README.md) · [Next: Everyday Git →](02-git.md)

Complete the prerequisites, then choose one workflow: create a project on
[GitHub](#create-a-new-project-on-github), create one on
[GitLab](#create-a-new-project-on-gitlab), or
[clone an existing project](#work-with-an-existing-project).
Run terminal commands from the project folder unless stated otherwise.

## Prerequisites

Install [Git](https://git-scm.com/downloads), [Python 3.11+](https://www.python.org/downloads/),
and [uv](https://docs.astral.sh/uv/getting-started/installation/).
[PyCharm](https://www.jetbrains.com/pycharm/) and
[GitHub Desktop](https://desktop.github.com/) are optional interfaces.
Verify the terminal can find the tools:

```sh
git --version
python --version
uv --version
```

### Commit identity

Check the name and email Git will use for your commits:

```sh
git config --get user.name
git config --get user.email
```

If missing or incorrect, set them:

```sh
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Replace the placeholders; use your host's private commit email if desired.
These settings identify your commits; they do not log you in. In GitHub Desktop,
edit them under **File → Options → Git**. Repository-specific settings override
these defaults; see [chapter 06](06-reference.md#git-commands-and-desktop-equivalents).

### Authentication

Before cloning a private repository or publishing changes, authenticate through
the application you use:

- **GitHub Desktop:** sign in to your GitHub account.
- **PyCharm:** add your account under **Settings → Version Control → GitHub / GitLab**.

For terminal access or GitLab through GitHub Desktop, use a Git credential manager
or SSH; see the [authentication reference](06-reference.md#authentication-and-storage).
The local lab needs no remote authentication.

The examples use `main`; substitute your repository's actual branch if different.

## Create a new project on GitHub

Use GitHub Desktop → PyCharm → uv:

1. In GitHub Desktop, choose **File → New repository**, select the name and local
   path, initialize a README, and choose the Python `.gitignore`. Select a license
   suitable for the project; this tutorial uses MIT.
2. Use **Publish repository**, choosing the intended account and visibility.
3. In PyCharm, choose **File → Open** and select the repository folder.
4. In the interpreter selector, choose **Add New Interpreter → Add Local Interpreter**,
   then **uv**. For a new project, this creates `pyproject.toml` automatically.
5. Run `uv sync` in the terminal to synchronize the virtual environment `.venv` and
   generate `uv.lock`.
6. Ensure `.idea/` and `.venv/` are in `.gitignore`. Commit everything and push.

Optionally create `main.py` and a **Run → Edit Configurations → Add → uv run**
configuration with `main.py` as the script and the project root as the working
directory. A regular Python configuration using `.venv` also works.

Menu labels vary by PyCharm version; see the
[uv interpreter instructions](https://www.jetbrains.com/help/pycharm/uv.html).

### CLI alternative

Install [GitHub CLI](https://cli.github.com/) and sign in with `gh auth login`.
In a new, empty folder outside any existing Git repository, run:

```sh
uv init --no-package
uv sync
```

`uv init` creates the Python project and initializes Git locally; `uv sync`
creates `.venv` and `uv.lock`. Ensure `.venv/` and `.idea/` are in `.gitignore`
and add a license if needed. Then commit and publish:

```sh
git add .
git commit -m "Initialize Python project"
git branch -M main
gh repo create YOUR-REPOSITORY --private --source=. --remote=origin --push
```

Replace `YOUR-REPOSITORY` with the desired name. Use `--public` instead of
`--private` for a public repository. Open the folder in PyCharm and select its
existing `.venv` if you want to use the IDE.

## Create a new project on GitLab

1. In GitLab, select **New project → Create blank project**; set the name,
   namespace, and visibility, and initialize with a README.
2. Copy its HTTPS or SSH clone URL from the project's **Code** menu.
3. In GitHub Desktop, use **File → Clone repository → URL**, paste that URL, and
   choose the local destination. Alternatively, use `git clone` in a terminal.
4. Follow steps 3–6 of the [GitHub workflow](#create-a-new-project-on-github)
   to configure Python and push the setup to GitLab.

GitHub Desktop can manage a GitLab clone; authenticate as described
[above](#authentication).

## Work with an existing project

Clone once using GitHub Desktop (**File → Clone repository → URL**),
PyCharm (**Git → Clone**), or the terminal:

```sh
git clone https://HOST/NAMESPACE/REPOSITORY.git
cd REPOSITORY
```

Replace the placeholders with the repository's clone URL and folder name.
For a uv project with `pyproject.toml` and `uv.lock`, install the recorded environment:

```sh
uv sync --locked
```

If it has no lockfile yet, use `uv sync`. If it does not use uv, follow its own
setup instructions. Do not run `uv init` over an existing `pyproject.toml`.

In PyCharm, use **File → Open** for a folder already cloned, then select the
existing `.venv`. On Windows, its interpreter is `.venv/Scripts/python.exe`.
Reuse that environment for run configurations.

Cloning retrieves Git files and configures `origin`; DVC-tracked data and models
require a separate download, covered in [chapter 04](04-dvc.md).

For everyday dependency and Python commands, see the
[uv reference](06-reference.md#python-environment-with-uv).
