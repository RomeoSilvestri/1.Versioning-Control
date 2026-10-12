# 06 · Quick reference and troubleshooting

[← Hands-on lab](05-hands-on-lab.md) · [Contents](../README.md)

Run commands from the project root. Uppercase names such as `FILE`, `BRANCH`,
`COMMIT`, and `URL` are placeholders, not literal arguments.

## Commands by task

| Task | Command |
| --- | --- |
| Inspect local changes | `git status --short` and `git diff` |
| Inspect the next commit | `git diff --staged` |
| Stage selected changes | `git add FILE` or `git add -p` |
| Record them | `git commit -m "Describe the change"` |
| Start a branch | `git switch -c BRANCH` |
| Inspect remote updates | `git fetch origin` |
| Update an existing tracking branch | `git pull --ff-only` |
| Publish a branch | `git push -u origin BRANCH` |
| Undo a shared commit | `git revert COMMIT` |
| See history | `git log --oneline --graph --decorate -10` |
| Show a tracked file at a revision | `git show COMMIT:path/to/file` |
| Track/update an independent artifact | `uv run dvc add FILE` |
| Reproduce declared outputs | `uv run dvc repro` |
| Inspect the recipe | `uv run dvc dag` |
| Inspect file consistency | `uv run dvc status` |
| Upload current artifacts | `uv run dvc push` |
| Download matching artifacts | `uv run dvc pull` |
| Restore from the local cache | `uv run dvc checkout` |
| Compare data/model metadata | `uv run dvc diff COMMIT` |
| Compare metrics / parameters | `uv run dvc metrics diff COMMIT` / `uv run dvc params diff COMMIT` |
| Install the recorded environment | `uv sync --locked` |
| Verify the Python example | `uv run python -m unittest discover -s tests -v` |

## Two recurring recipes

**Publish a reproducible change:** update standalone data pointers with `dvc add`,
run `dvc repro`, check metrics, then stage code, parameters, pointers, `dvc.lock`,
and small metrics. Commit, `dvc push`, then `git push` and open the PR/MR.

**Recover a recorded version:** start with a clean working tree, switch Git to the
revision, `uv sync --locked`, then `dvc checkout` for a populated cache or `dvc pull`
for remote retrieval. Check `dvc status`.

## Common problems

| Symptom | Check and fix |
| --- | --- |
| `uv sync` cannot find a project | Change to the folder with `pyproject.toml`; initialize only a genuinely new project |
| `uv sync --locked` refuses | Review requirement changes; run `uv lock`, then `uv sync`, and commit both TOML and lockfile |
| PyCharm imports fail | Select the project's `.venv` interpreter and synchronize dependencies |
| `dvc` is not found | Use `uv run dvc ...`, or synchronize the environment first |
| `not a DVC repository` | Use the initialized lab; in a new Git project run `uv run dvc init` once |
| Raw data missing before training | Generate v1 in a new lab, or pull the recorded real dataset from its remote |
| `remote origin already exists` | Inspect `git remote -v`; use `remote set-url` if the URL is wrong |
| Git push is rejected as non-fast-forward | Fetch, inspect history, integrate remote work on your branch, then push |
| `pull --ff-only` refuses | Local and remote histories diverged; inspect the graph, then explicitly merge if appropriate |
| Authentication fails | Verify host, account access, and credential helper/SSH; Git identity is not authentication |
| Cannot push to `main` | Follow the repository's protected-branch PR/MR workflow |
| `dvc push` has no remote | Configure a default DVC remote; a Git `origin` is not DVC storage |
| `dvc pull` reports missing objects | Confirm the intended Git revision, storage URL, permissions, and that the author pushed that version |
| Git is clean but DVC reports changes | Git ignores the contents; restore them or intentionally update pointers and reproduce |
| Dataset/model still has the old version after switching branches | Run `dvc checkout` or `dvc pull` after the Git switch |
| DVC says an output is already tracked | Keep one owner: standalone `dvc add` or a pipeline stage |
| A newly ignored file still appears in Git | `.gitignore` does not untrack files; use `git rm --cached FILE` after checking the path |
| Windows paths contain spaces | Quote arguments; use forward slashes in recipe paths |
| CRLF/LF messages appear | `.gitattributes` selects LF for tracked text, keeping DVC dependency hashes stable across clones; keep this file in Git |

## Before sharing a change

- Inspect the staged diff and exclude environments, credentials, data, and models.
- Run the checks relevant to the change and include the results in the review.
- Commit dependency requirements and lockfile together when they change.
- Commit DVC pointers and pipeline records with the code/parameters they describe.
- Upload artifacts before publishing the Git commit that points to them.

Use `uv run dvc --help`, `git help COMMAND`, or the linked official docs in earlier
chapters for options beyond this compact reference. Avoid deleting DVC cache or
remote objects while learning recovery; unreferenced artifacts may still belong
to another branch or tag.
