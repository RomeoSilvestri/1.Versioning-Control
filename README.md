# Versioning & Control for MLOps

A short practical book and command reference for **Git, GitHub, GitLab, and DVC**.
This is part 1 of an MLOps toolkit: version the code, data, and model artifacts
needed to recover a specific result. The examples use Python and `uv`, with
PyCharm guidance where the IDE helps.

Git records code and small metadata files. GitHub and GitLab host Git repositories
and support reviews. DVC connects dataset and model versions to Git commits while
keeping their contents in separate storage.

## Read the book

| Chapter | Use it when you need to... |
| --- | --- |
| [01 · Setup](docs/01-setup.md) | Create a GitHub/GitLab project, clone an existing one, or configure PyCharm and uv |
| [02 · Everyday Git](docs/02-git.md) | Review changes, commit, push/pull, and work on branches |
| [03 · GitHub & GitLab](docs/03-collaboration.md) | Connect a remote and review changes through PRs/MRs |
| [04 · Data & models with DVC](docs/04-dvc.md) | Track files, configure storage, and recover matching artifacts |
| [05 · Hands-on lab](docs/05-hands-on-lab.md) | Run the complete workflow locally, including a fresh clone |
| [06 · Quick reference](docs/06-reference.md) | Find a command or fix a common problem |

Read chapters **01 → 02 → 03 → 04**, then run the lab in **05**. Keep **06**
available as a reference for commands, less frequent tasks, and troubleshooting.
The book is Markdown, readable directly in GitHub, GitLab, or PyCharm.
Git commands include **PyCharm** and **GitHub Desktop** equivalents; Python and
DVC commands run in the project terminal.

## What is in the repository?

| Path | Purpose |
| --- | --- |
| `docs/` | The book and command reference |
| `scripts/create_lab.py` | Create a new isolated practice directory |
| `scripts/make_data.py` | Generate deterministic dataset versions 1 and 2 |
| `scripts/train.py` | Fit a tiny linear regression using the Python standard library |
| `params.json`, `dvc.yaml` | Parameter and pipeline templates |
| `pyproject.toml`, `uv.lock` | Dependency requirements and resolved versions |
| `tests/test_example.py` | Checks for repeatability, fitting, and invalid inputs |

The tutorial repository contains source templates, not an initialized DVC project.
`create_lab.py` copies the book and runnable sources into an independent directory
without `.git`, `.venv`, `.idea`, credentials, or generated outputs. All practice
commits and DVC state belong there.

Explore the scripts during chapter 05: start with `create_lab.py`, then read
`make_data.py`, `train.py`, `params.json`, and `dvc.yaml` before the first pipeline
run. The example uses the Python standard library for training and DVC for versioning.

## Optional quickstart: run your first version

This starts **step 1 of chapter 05** for readers who want to try the example
immediately. On a first read, you can skip it, read chapters 01–04, and run the
same commands when you reach the lab. Run this setup only once per lab directory.

Install **Git**, **Python 3.11+**, and **uv** following [chapter 01](docs/01-setup.md).
Open a PowerShell terminal in this repository:

```sh
uv sync --locked
uv run python scripts/create_lab.py ../versioning-lab
cd ../versioning-lab
git init -b main
uv run dvc init
uv run python scripts/make_data.py --version 1
uv run dvc add data/raw/samples.csv
uv run dvc repro
uv run dvc metrics show
uv run dvc status
```

The final command should report that data and pipelines are up to date. You now
have 40 synthetic rows, a JSON model, and holdout metrics. Continue at **step 2**
of [the lab](docs/05-hands-on-lab.md) to commit, upload, change, and recover versions.
The lab directory must not already exist; choose another name for another run.
No cloud account or external dataset is needed. Installing dependencies requires
internet access; the exercises then use local storage.

## Check the example

Run the example checks from the tutorial or lab repository root:

```sh
uv run python -m unittest discover -s tests -v
```

See each chapter's official documentation links for further detail. MIT licensed;
see [LICENSE](LICENSE).
