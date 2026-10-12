# 06 · Quick reference and troubleshooting

[← Hands-on lab](05-hands-on-lab.md) · [Contents](../README.md)

Run commands from the project root. Uppercase names such as `FILE`, `BRANCH`,
`COMMIT`, and `URL` are placeholders, not literal arguments.

## Git commands and desktop equivalents

These are equivalent tasks; GUI actions may combine commands or use different
options. **Branch selector** means PyCharm's Git/VCS widget in the window header.
**Changes**, **History**, and **Current Branch** refer to GitHub Desktop.
Detailed explanations and official UI documentation are in
[chapter 02](02-git.md). Both apps should point to the same repository folder.

| Task | CLI | PyCharm | GitHub Desktop |
| --- | --- | --- | --- |
| Initialize local Git | `git init -b main` | **VCS → Enable Version Control Integration → Git**; verify branch name | **File → New repository**; to register an existing clone, **File → Add Local Repository** |
| Clone a repository | `git clone URL` | **Git → Clone** | **File → Clone repository → URL** |
| Inspect local changes | `git status --short`, `git diff` | **Commit** window; select file → **Show Diff** | **Changes**; select a file to inspect its diff |
| Select files or hunks | `git add FILE`, `git add -p` | Select files/chunks in **Commit**, or **Stage** with staging enabled | File checkboxes and selected lines in **Changes** |
| Inspect the next commit | `git diff --staged` | Review selected diffs; with staging enabled, inspect **Staged** | Review checked files and included lines before commit |
| Commit locally | `git commit -m "Message"` | **Commit** window → message → **Commit** | **Changes → Summary → Commit to BRANCH** |
| Create a branch | `git switch -c BRANCH` | Branch selector → **New Branch** | **Current Branch → New Branch**; choose the base |
| List local branches | `git branch` | Branch selector → **Local branches** | **Current Branch** list |
| Switch branches | `git switch BRANCH` | Branch selector → branch → **Checkout** | **Current Branch → branch** |
| Fetch remote commits | `git fetch origin` | **Git → Fetch** | **Fetch origin** |
| Pull into current branch | `git pull --ff-only` | **Git → Pull → Modify options → `--ff-only`** | **Fetch origin → Pull origin**; no explicit fast-forward-only guard |
| Publish / push a branch | `git push -u origin BRANCH` | **Git → Push**; check remote/branch target | **Publish branch**, then **Push origin** for later commits |
| Merge into current branch | `git merge --ff-only BRANCH` | **Git → Merge**; select branch and `--ff-only` in **Modify options** | **Current Branch → Choose a branch to merge into BRANCH**; use CLI for the `--ff-only` guard |
| Delete a local branch | `git branch -d BRANCH` | Branch selector → branch → **Delete**; can delete unmerged work | Select branch → **Branch → Delete**; review any remote-delete option |
| Rename / delete a tracked file | `git mv OLD NEW` / `git rm FILE` | Rename/delete in Project, then select the change for commit | Rename/delete in your editor or file manager, then select the change in **Changes** |
| Stop tracking, keep local copy | `git rm --cached FILE` | Terminal; add the ignore rule too | Terminal; add the ignore rule too |
| Inspect / change remotes | `git remote -v` / `git remote set-url origin URL` | **Git → Manage Remotes** | **Repository → Repository settings → Remote** for the primary URL |
| Exclude edits from a commit | `git restore --staged FILE` | **Unstage** in staging mode; otherwise deselect the file | Deselect the file/lines; this excludes them from the GUI commit |
| Discard uncommitted edits | `git restore FILE` | **Commit → right-click file → Rollback** | **Changes → right-click file → Discard Changes** |
| Undo a shared commit | `git revert COMMIT` | **Git → Log → right-click commit → Revert Commit** | **History → right-click commit → Revert Changes in Commit** |
| Inspect recorded history | `git log`, `git show COMMIT:path/to/file` | **Git → Log**, or file → **Git → Show History** | **History**; select commit and changed file |
| Temporarily set edits aside | `git stash push -u -m "WIP"` | Commit context menu → **Git → Stash Changes**; use CLI for explicit `-u` | Changes header → **Stash All Changes**; one set at a time |
| Restore stashed edits | `git stash pop` | **Stash** tab → stash → **Pop** | **Stashed Changes → Restore** on the relevant branch |
| Create an annotated tag | `git tag -a TAG -m "Message"` | **Git → New Tag**; provide a **Message** | **History → right-click commit → Create Tag** |
| Inspect a recorded version | `git switch --detach TAG` | Branch selector → **Tags → tag → Checkout** | **History → right-click tagged commit → Checkout Commit** |
| Recover recent local positions | `git reflog` | Terminal | **Repository → Open in command line**, then terminal command |

**Selection is not deletion:** deselect/unstage preserves edits; Rollback/Discard
removes them. A GUI's default merge/pull is not necessarily `--ff-only`, and GUI
branch deletion is not necessarily the guarded `git branch -d`.
If a file is separately staged, `git restore FILE` restores its index version;
GUI Rollback/Discard may revert to the last commit instead.
In PyCharm, **Update Project** follows its configured merge/rebase strategy.
See [chapter 02](02-git.md#commit-push-fetch-and-pull-are-different-operations)
for the differences between commit, push, fetch, and pull.

## DVC and Python commands

Run these in the project terminal, including PyCharm's terminal. GitHub Desktop
does not provide DVC operations, and its **Push origin**/**Pull origin** buttons
transfer Git commits, not DVC artifact contents.

| Task | Command |
| --- | --- |
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
