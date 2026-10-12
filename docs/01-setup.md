# 01 · Set up a project

[Contents](../README.md) · [Next: Everyday Git →](02-git.md)

## Prerequisites and identity

Install [Git](https://git-scm.com/downloads), [Python](https://www.python.org/downloads/),
and [uv](https://docs.astral.sh/uv/getting-started/installation/).
[PyCharm](https://www.jetbrains.com/pycharm/) and
[GitHub Desktop](https://desktop.github.com/) are optional interfaces.
Verify the terminal can find the tools:

```sh
git --version
python --version
uv --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
```

Replace the identity placeholders. The email is recorded in commits; use your
host's private commit email if desired. Git identity does not authenticate you
to GitHub or GitLab. The examples assume `main`; substitute your repository's
actual default branch if different.

## Create a new project on GitHub

The original GitHub Desktop → PyCharm → uv workflow is:

1. In GitHub Desktop, choose **File → New repository**, select the name and local
   path, initialize a README, and choose the Python `.gitignore`. Select a license
   suitable for the project; this tutorial uses MIT.
2. Use **Publish repository**, choosing the intended account and visibility.
3. In PyCharm, choose **File → Open** and select the repository folder.
4. Configure a uv environment as described below, then run `uv sync`.
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

Replace all uppercase placeholders. For a project without `pyproject.toml`, follow
its own setup instructions before migrating it to uv. Do not run `uv init` in
this tutorial or another project that already has that file. If a uv project has
no lockfile yet, run `uv sync` and commit the generated `uv.lock`.

## Configure PyCharm and uv

In the interpreter selector, choose **Add New Interpreter → Add Local Interpreter**,
then **uv**. For a new project, generate a new environment. If PyCharm has not
created `pyproject.toml`, run `uv init --bare` first, then `uv sync`.
`uv sync` creates `.venv` and resolves `uv.lock`; it does not initialize a project.

For an existing project, run `uv sync --locked` and reuse that environment. Its
interpreter is `.venv/Scripts/python.exe` on Windows or `.venv/bin/python` on
macOS/Linux. Avoid creating a second environment for the same project.
Menu labels vary by PyCharm version; see the
[uv interpreter instructions](https://www.jetbrains.com/help/pycharm/uv.html).

For this example, set the run configuration's script to `scripts/train.py` and
working directory to the lab root. Generate the data first. Run `uv run dvc repro`
in the IDE terminal to update DVC's record after changing code, data, or parameters.

## uv commands overview

| Command | Use |
| --- | --- |
| `uv init --bare` | Initialize a minimal new Python project |
| `uv sync` | Resolve if needed, then synchronize the project environment |
| `uv sync --locked` | Install from a current lockfile; fail if it needs updating |
| `uv add PACKAGE` / `uv remove PACKAGE` | Change requirements and lockfile |
| `uv lock --upgrade-package PACKAGE` | Update one dependency within its constraints |
| `uv lock --upgrade` | Update all dependencies within their constraints |
| `uv run main.py` | Run a script in the synchronized project environment |
| `uv run dvc status` | Run a project tool without activating `.venv` |

After `uv lock --upgrade`, use `uv sync` to install the new resolution.
`uv run` checks the project's environment, including its declared dependencies;
it is not a per-script dependency scanner. Commit both requirement and lockfile
changes together. Details: [uv projects](https://docs.astral.sh/uv/guides/projects/)
and [locking and syncing](https://docs.astral.sh/uv/concepts/projects/sync/).
