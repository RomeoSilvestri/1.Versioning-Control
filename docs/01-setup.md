# 01 · Set up a project

[Contents](../README.md) · [Next: Everyday Git →](02-git.md)

## Prerequisites

Install [Git](https://git-scm.com/downloads), [Python](https://www.python.org/downloads/),
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
These settings identify your commits; they do not log you in. Changing them
requires no password and does not modify existing commits. Repository-specific
settings take precedence: a name/email configured for one project applies only there.
To change a project's own identity, see [chapter 06](06-reference.md).

In GitHub Desktop, check or edit them under **File → Options → Git**.
PyCharm also prompts for missing identity when first committing. See
[Desktop Git configuration](https://docs.github.com/en/desktop/configuring-and-customizing-github-desktop/configuring-git-for-github-desktop).

### Authentication

Before accessing a private remote repository or pushing changes, sign in through
your chosen application, if needed:

- **GitHub Desktop:** sign in to your GitHub account.
- **PyCharm:** add your account under **Settings → Version Control → GitHub / GitLab**.

Authentication is not required for the local lab. For GitLab access through
GitHub Desktop, see [chapter 03](03-collaboration.md).

The examples use `main`; substitute your repository's actual branch if different.

## Create a new project on GitHub

Use GitHub Desktop → PyCharm → uv:

1. In GitHub Desktop, choose **File → New repository**, select the name and local
   path, initialize a README, and choose the Python `.gitignore`. Select a license
   suitable for the project; this tutorial uses MIT.
2. Use **Publish repository**, choosing the intended account and visibility.
3. In PyCharm, choose **File → Open** and select the repository folder.
4. Configure a uv environment as described below. For a new project without
   `pyproject.toml`, run `uv init --bare`, then `uv sync`.
5. Ensure `.idea/` and `.venv/` are ignored. Commit `pyproject.toml` and `uv.lock`.
6. Optionally create `main.py` and a **Run → Edit Configurations → Add → uv run**
   configuration with `main.py` as the script and the project root as the working
   directory. A regular Python configuration using `.venv` also works.

If you prefer the CLI, create an **empty** remote repository without an initial
README, then run these commands in a new local project folder:

```sh
git init -b main
uv init --bare
uv sync
git add pyproject.toml uv.lock
git commit -m "Initialize Python project"
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL. Add a README, Python `.gitignore`, and license before growing the
project. If the remote already has an initial commit, clone it instead.

`git init` creates a local repository; it does not create a hosted repository.
`git remote add origin URL` names the remote destination, and `git push` sends
commits there. In PyCharm, **VCS → Enable Version Control Integration → Git**
initializes Git for an existing project folder; **Git → Manage Remotes** manages
the remote URL. GitHub Desktop's **File → New repository** performs the local
setup, and **Publish repository** creates its GitHub destination.

## Create a new project on GitLab

1. In GitLab, select **New project → Create blank project**; set the name,
   namespace, and visibility, and initialize with a README.
2. Copy its HTTPS or SSH clone URL from the project's **Code** menu.
3. In GitHub Desktop, use **File → Clone repository → URL**, paste that URL, and
   choose the local destination. Alternatively, use `git clone` in a terminal.
4. Continue at step 3 of the GitHub workflow: open in PyCharm and configure uv.

GitHub Desktop can manage a local GitLab clone, but its GitHub account integration
does not provide GitLab authentication. Use the Git credential manager, SSH, or
PyCharm's GitLab integration; see [chapter 03](03-collaboration.md).

## Work with an existing project

In GitHub Desktop, choose **File → Clone repository → GitHub.com** or **URL**
(the URL tab works for either host). Or use:

```sh
git clone https://HOST/NAMESPACE/REPOSITORY.git
cd REPOSITORY
uv sync --locked
```

Replace the placeholders. Do not run `uv init` in a project that already has
`pyproject.toml`. If it has no lockfile yet, use `uv sync`; if it has no uv project
configuration, follow its own setup instructions.

`git clone` downloads a Git repository and normally configures `origin` for you.
In PyCharm, use **Git → Clone**, enter the URL, and select the destination.
To open a folder already cloned by GitHub Desktop, use **File → Open** instead
of cloning again. Cloning does not install Python dependencies or retrieve
DVC-tracked contents.
See [PyCharm repository setup](https://www.jetbrains.com/help/pycharm/set-up-a-git-repository.html).

## Configure PyCharm and uv

In the interpreter selector, choose **Add New Interpreter → Add Local Interpreter**,
then **uv**. For a new project, generate a new environment. If PyCharm has not
created `pyproject.toml`, run `uv init --bare` first, then `uv sync`.
`uv sync` creates `.venv` and resolves `uv.lock`; it does not initialize a project.

For an existing project, run `uv sync --locked` and reuse that environment. Its
interpreter is `.venv/Scripts/python.exe`. Avoid creating a second environment
for the same project.
Menu labels vary by PyCharm version; see the
[uv interpreter instructions](https://www.jetbrains.com/help/pycharm/uv.html).

For this example, set the run configuration's script to `scripts/train.py` and
working directory to the lab root. Generate the data first. Run `uv run dvc repro`
in the IDE terminal to update DVC's record after changing code, data, or parameters.

## Daily Python commands

| Command | Use |
| --- | --- |
| `uv init --bare` | Initialize a minimal new Python project |
| `uv sync` | Resolve if needed, then synchronize the project environment |
| `uv sync --locked` | Install from a current lockfile; fail if it needs updating |
| `uv add PACKAGE` / `uv remove PACKAGE` | Change requirements and lockfile |
| `uv run main.py` | Run a script in the synchronized project environment |
| `uv run dvc status` | Run a project tool without activating `.venv` |

Commit `pyproject.toml` and `uv.lock` together when dependencies change.
Additional commands are in [chapter 06](06-reference.md#python-environment).
Documentation: [uv projects](https://docs.astral.sh/uv/guides/projects/).
