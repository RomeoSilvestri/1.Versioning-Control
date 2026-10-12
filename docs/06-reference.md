# 06 · Quick reference and troubleshooting

[← Hands-on lab](05-hands-on-lab.md) · [Contents](../README.md)

Run commands from the project root. Uppercase names such as `FILE`, `BRANCH`,
`COMMIT`, and `URL` are placeholders, not literal arguments.

## Git commands and desktop equivalents

These are equivalent tasks; GUI actions may combine commands or use different
options. **Branch selector** means PyCharm's Git/VCS widget in the window header.
**Changes**, **History**, and **Current Branch** refer to GitHub Desktop.
The daily workflow is explained in [chapter 02](02-git.md). This table also
includes operations you may need occasionally. Both apps should point to the
same repository folder.

| Task | CLI | PyCharm | GitHub Desktop |
| --- | --- | --- | --- |
| Initialize local Git | `git init -b main` | **VCS → Enable Version Control Integration → Git**; verify branch name | **File → New repository**; to register an existing clone, **File → Add Local Repository** |
| Clone a repository | `git clone URL` | **Git → Clone** | **File → Clone repository → URL** |
| Check commit identity | `git config --get user.name` / `git config --get user.email` | Terminal | **File → Options → Git** for global defaults; **Repository settings → Git config** for this project |
| Set identity for this repository | `git config --local user.email "you@example.com"` / `git config --local user.name "Your Name"` | Terminal inside an initialized repository | **Repository → Repository settings → Git config** |
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
| Merge into current branch | `git merge BRANCH`; add `--ff-only` to require a fast-forward | **Git → Merge**; optional `--ff-only` in **Modify options** | **Current Branch → Choose a branch to merge into BRANCH**; use CLI for the `--ff-only` guard |
| Delete a local branch | `git branch -d BRANCH` | Branch selector → branch → **Delete**; can delete unmerged work | Select branch → **Branch → Delete**; review any remote-delete option |
| Rename / delete a tracked file | `git mv OLD NEW` / `git rm FILE` | Rename/delete in Project, then select the change for commit | Rename/delete in your editor or file manager, then select the change in **Changes** |
| Stop tracking, keep local copy | `git rm --cached FILE` | Terminal; add the ignore rule too | Terminal; add the ignore rule too |
| Inspect / change remotes | `git remote -v` / `git remote set-url origin URL` | **Git → Manage Remotes** | **Repository → Repository settings → Remote** for the primary URL |
| Connect an existing project to a remote | `git remote add origin URL` | **Git → Manage Remotes** | **Publish repository** for a new GitHub repository; terminal for an existing remote |
| Exclude edits from a commit | `git restore --staged FILE` | **Unstage** in staging mode; otherwise deselect the file | Deselect the file/lines; this excludes them from the GUI commit |
| Discard uncommitted edits | `git restore FILE` | **Commit → right-click file → Rollback** | **Changes → right-click file → Discard Changes** |
| Undo a shared commit | `git revert COMMIT` | **Git → Log → right-click commit → Revert Commit** | **History → right-click commit → Revert Changes in Commit** |
| Inspect recorded history | `git log --oneline --graph --decorate -10`, `git show COMMIT:path/to/file` | **Git → Log**, or file → **Git → Show History** | **History**; select commit and changed file |
| Temporarily set edits aside | `git stash push -u -m "WIP"` | Commit context menu → **Git → Stash Changes**; use CLI for explicit `-u` | Changes header → **Stash All Changes**; one set at a time |
| Restore stashed edits | `git stash pop` | **Stash** tab → stash → **Pop** | **Stashed Changes → Restore** on the relevant branch |
| List stashes | `git stash list` | **Stash** tab | One stashed set at a time; use terminal for a list |
| Create a version tag | `git tag -a TAG -m "Message"` | **Git → New Tag**; provide a **Message** | **History → right-click commit → Create Tag** |
| Publish a specific tag | `git push origin TAG` | **Git → Push → Push Tags**; inspect the tags selected | **Push origin** publishes Desktop-created tags with their commits |
| Inspect a recorded version | `git switch --detach TAG` | Branch selector → **Tags → tag → Checkout** | **History → right-click tagged commit → Checkout Commit** |
| Start work from a tag | `git switch -c BRANCH TAG` | Check out tag, then branch selector → **New Branch** | Check out tagged commit, then **Branch → New Branch** |
| Cancel an in-progress merge | `git merge --abort` | **Abort Merge** action | Terminal |
| Recover recent local positions | `git reflog` | Terminal | **Repository → Open in command line**, then terminal command |
| Confirm which files Git tracks | `git ls-files` | Terminal | Terminal |

**Selection is not deletion:** deselect/unstage preserves edits; Rollback/Discard
removes them. A GUI's default merge/pull is not necessarily `--ff-only`, and GUI
branch deletion is not necessarily the guarded `git branch -d`.
If a file is separately staged, `git restore FILE` restores its index version;
GUI Rollback/Discard may revert to the last commit instead.
In PyCharm, **Update Project** follows its configured merge/rebase strategy.
See [chapter 02](02-git.md#share-and-receive-changes)
for the differences between commit, push, fetch, and pull.

With explicit staging in PyCharm, enable **Settings → Version Control → Git →
Enable staging area**. Without it, select changes in the Commit window.
Adding a tracked file to `.gitignore` does not untrack it. Use the stop-tracking
row above; previous commits will still contain that file.

Stash is temporary local storage. CLI `-u` includes untracked files, but not
ignored datasets/models. PyCharm's **Shelve Changes** is a separate IDE feature.
Use revert for shared commits; avoid `reset --hard` and force-push as routine cleanup.

## DVC and Python commands

Run these in the project terminal, including PyCharm's terminal. GitHub Desktop
does not provide DVC operations, and its **Push origin**/**Pull origin** buttons
transfer Git commits, not DVC artifact contents.

| Task | Command |
| --- | --- |
| Initialize DVC in a Git project | `uv run dvc init` |
| Configure the lab's default storage | `uv run dvc remote add --local -d storage ../versioning-dvc-store` |
| List configured storage | `uv run dvc remote list` |
| Track/update an independent artifact | `uv run dvc add FILE` |
| Reproduce declared outputs | `uv run dvc repro` |
| Inspect the recipe | `uv run dvc dag` |
| Inspect file consistency | `uv run dvc status` |
| Upload current artifacts | `uv run dvc push` |
| Download into the cache without restoring files | `uv run dvc fetch` |
| Download matching artifacts | `uv run dvc pull` |
| Restore from the local cache | `uv run dvc checkout` |
| Compare data/model metadata | `uv run dvc diff COMMIT` |
| Show current metrics | `uv run dvc metrics show` |
| Compare metrics / parameters | `uv run dvc metrics diff COMMIT` / `uv run dvc params diff COMMIT` |
| Install the recorded environment | `uv sync --locked` |
| Verify the Python example | `uv run python -m unittest discover -s tests -v` |

### Python environment

| Task | Command |
| --- | --- |
| Initialize a new Python project | `uv init --bare` |
| Resolve and install dependencies | `uv sync` |
| Add / remove a dependency | `uv add PACKAGE` / `uv remove PACKAGE` |
| Update one dependency within its constraints | `uv lock --upgrade-package PACKAGE`, then `uv sync` |
| Update dependencies within their constraints | `uv lock --upgrade`, then `uv sync` |
| Run a Python script | `uv run python scripts/train.py` |

Commit both `pyproject.toml` and `uv.lock` when dependencies change.

## Authentication and storage

For Git HTTPS access, use a credential manager or host-issued token; an account
password is not the normal Git credential. SSH uses a key registered with your
account. Git and DVC storage authentication are separate. Keep credentials out
of source files and remote URLs.
See [GitHub authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
and [GitLab SSH](https://docs.gitlab.com/user/ssh/).

The lab's sibling storage folder is for practice, not an independent backup.
For shared S3 storage, with an existing bucket and access configured:

```sh
uv add "dvc[s3]"
uv run dvc remote add -d storage s3://YOUR-BUCKET/YOUR-PREFIX
git add pyproject.toml uv.lock .dvc/config
```

Replace the URL. Shared remote configuration goes in Git; credentials stay in
the backend's credential mechanism or ignored `.dvc/config.local`.
See [DVC remote storage](https://doc.dvc.org/user-guide/data-management/remote-storage).

## Team repository settings

Require review before merging into `main` through GitHub rulesets/branch
protection or GitLab **Settings → Repository → Branch rules**. Policies depend
on your plan and permissions. In GitLab, set **Allowed to push and merge → No one**
to prevent direct pushes when requiring MRs.
See [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
and [GitLab protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/).

If you lack write access, fork the repository, push to your fork, and open a
PR/MR against the original. A second remote is a separate destination; pushing
to GitHub does not also update GitLab.

## Workflow recipes

**Publish a reproducible change:** update standalone data pointers with `dvc add`,
run `dvc repro`, check metrics, then stage code, parameters, pointers, `dvc.lock`,
and small metrics. Commit, `dvc push`, then `git push` and open the PR/MR.

**Recover a recorded version:** start with a clean working tree, switch Git to the
revision, `uv sync --locked`, then `dvc checkout` for a populated cache or `dvc pull`
for remote retrieval. Check `dvc status`.

**Resolve DVC metadata conflicts:** choose the intended dataset or regenerate it
and run `dvc add`. Resolve code and parameters, run `dvc repro` to regenerate
`dvc.lock`, then review and commit the result. Do not combine hashes manually.
Upload the resulting artifacts before pushing Git.

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
| A local branch cannot be deleted after a squash merge | `git branch -d` checks ancestry; confirm the work is merged before considering force deletion |

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

UI documentation: [PyCharm staging](https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html),
[PyCharm undo](https://www.jetbrains.com/help/pycharm/undo-changes.html),
[PyCharm stash](https://www.jetbrains.com/help/pycharm/shelving-and-unshelving-changes.html),
[Desktop stash](https://docs.github.com/en/desktop/making-changes-in-a-branch/stashing-changes-in-github-desktop),
[Desktop tags](https://docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop).
