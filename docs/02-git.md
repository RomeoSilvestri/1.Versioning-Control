# 02 · Everyday Git

[← Setup](01-setup.md) · [Contents](../README.md) · [Next: Collaboration →](03-collaboration.md)

Use PyCharm or GitHub Desktop for daily Git work. The commands below explain
the same operations in the terminal. Open the same repository folder in either
app; in PyCharm, **Find Action** helps locate menu items.

## Save a change with a commit

Git separates three things: the files you edit (**working tree**), the changes
selected for the next commit (**staging area**), and the saved snapshots
(**commit history**). A commit stays on your computer until you push it.

```text
edit files → select changes → commit locally → push to GitHub / GitLab
             git add         git commit       git push
```

From the project root:

```sh
git status
git diff
git add scripts/train.py params.json
git diff --staged
git commit -m "Adjust training split"
git log --oneline -10
```

- `status` lists new, modified, and staged files.
- `diff` shows unstaged edits; `diff --staged` shows what the next commit contains.
- `add` selects the current contents of a file. Stage it again if you edit it afterward.
- `commit` saves the selected changes with a message describing them.
- `log` shows previous commits.

| Task | PyCharm | GitHub Desktop |
| --- | --- | --- |
| Review and select changes | **Commit** window → select files → **Show Diff** | **Changes** → select files and inspect their diffs |
| Commit | Enter a message → **Commit** | Enter a **Summary** → **Commit to BRANCH** |
| Browse history | **Git → Log** | **History** |

Select new files too: PyCharm lists them under **Unversioned Files**.
Renames and deletions also appear as changes to commit.

Keep `.venv/`, `.idea/`, credentials, and generated artifacts out of commits.
`.gitignore` excludes files that Git has not already tracked. In this tutorial,
DVC handles the dataset and model contents; Git tracks their metadata.

## Share and receive changes

| Command | What it does |
| --- | --- |
| `git push -u origin BRANCH` | Upload commits; `-u` connects the local branch to its remote branch |
| `git push` | Upload later commits on a branch with an upstream configured |
| `git fetch origin` | Download remote history without changing your current files |
| `git pull --ff-only` | Fetch and update your branch; stop if local and remote work have diverged |

`origin` is the remote repository's name, usually configured by `git clone`.
Replace `BRANCH` with your current branch name. Saving a file, committing it,
and pushing it are separate steps. Pull receives changes; it does not upload yours.

| Task | PyCharm | GitHub Desktop |
| --- | --- | --- |
| Fetch | **Git → Fetch** | **Fetch origin** |
| Pull | **Git → Pull** | **Fetch origin**, then **Pull origin** |
| Push | **Git → Push** | **Publish branch** initially, then **Push origin** |

The GUI pull follows the app's configured behavior. The CLI examples use
`--ff-only` to stop rather than automatically combine divergent histories;
see [the reference](06-reference.md) if this happens.

For DVC changes, commit first, run `uv run dvc push`, then push Git so others
can retrieve the artifacts referenced by your commit.

## Work on a branch

A branch is a named line of work in the same project folder. Start from an
updated `main` with no uncommitted changes:

```sh
git switch main
git pull --ff-only
git switch -c feature/update-dataset
```

`switch` changes branches; `switch -c` creates a new branch and switches to it.
Edit, check, and commit your work there, then push and open a review as described
in [chapter 03](03-collaboration.md).

**PyCharm:** branch selector → `main` → **Checkout**, pull, then **New Branch**.
**GitHub Desktop:** **Current Branch → main**, fetch/pull, then **New Branch**
with `main` as the base.

To include newer work from the remote `main` in your feature branch:

```sh
git fetch origin
git merge origin/main
```

`merge` combines another branch's work into the branch you currently have open.
In PyCharm, use **Git → Merge**; in Desktop, use **Current Branch → Choose a
branch to merge into BRANCH** and select the branch to include.

For a local exercise, switch back to `main` and merge your feature:

```sh
git switch main
git merge feature/update-dataset
```

For a shared project, merge the pull/merge request on GitHub or GitLab, then
switch to `main` and pull. You can delete a finished branch afterward; the
commands and GUI actions are in [chapter 06](06-reference.md).

## Resolve a conflict

A conflict occurs when Git cannot combine competing edits automatically.
Use `git status` to find the affected files.

**PyCharm:** open **Resolve Conflicts → Resolve Manually**, review the result,
and save it. **GitHub Desktop:** open the conflicting files in PyCharm, resolve
them, and return to Desktop to complete the merge.

In the terminal, edit the files to the intended result and remove the conflict
markers (`<<<<<<<`, `=======`, `>>>>>>>`). Then check and commit:

```sh
git add path/to/resolved-file
git diff --staged
git commit -m "Resolve merge conflict"
```

## Undo a change

| Need | CLI | PyCharm | GitHub Desktop |
| --- | --- | --- | --- |
| Exclude a file from the next commit, keeping edits | `git restore --staged FILE` | Deselect the file, or **Unstage** in staging mode | Deselect the file |
| Discard uncommitted edits | `git restore FILE` | **Commit → right-click file → Rollback** | **Changes → right-click file → Discard Changes** |
| Reverse a shared commit | `git revert COMMIT` | **Git → Log → right-click commit → Revert Commit** | **History → right-click commit → Revert Changes in Commit** |

Inspect changes before discarding them: this removes your edits. Revert adds
a new reversing commit and preserves shared history. For other recovery tools,
see [chapter 06](06-reference.md).

## Mark a version with a tag

A tag gives a fixed name to a commit. The lab uses one to recover its baseline:

```sh
git tag -a baseline-v1 -m "First reproducible baseline"
```

**PyCharm:** **Git → New Tag**, provide the name and message.
**GitHub Desktop:** **History → right-click commit → Create Tag**.

To inspect it, start with no uncommitted changes:

```sh
git switch --detach baseline-v1
git switch main
```

The first command opens the tagged commit; the second returns to your branch.
Detached mode is for inspection here. In PyCharm, use **branch selector → Tags
→ tag → Checkout**. In Desktop, right-click the tagged commit in **History**
and choose **Checkout Commit**. Return through either app's branch selector.

In a DVC project, also restore the matching data/model after switching versions;
Git alone updates only the tracked files. [Chapter 04](04-dvc.md) covers this.

Documentation: [Pro Git](https://git-scm.com/book/en/v2),
[PyCharm commits](https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html),
[Desktop commits](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop),
[PyCharm branches](https://www.jetbrains.com/help/pycharm/manage-branches.html),
[Desktop synchronization](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop).
