# 02 · Everyday Git

[← Setup](01-setup.md) · [Contents](../README.md) · [Next: Collaboration →](03-collaboration.md)

## The three places a change lives

Your working tree contains the files you edit. The staging area contains the
changes selected for your next commit. A commit is a saved snapshot, linked to
its parent history. `HEAD` identifies the current commit; a branch is a movable
name for a line of work. A commit is local until you push it.

```text
working tree --git add--> staging area --git commit--> local history
                                                         |
                                                      git push
                                                         v
                                                   GitHub / GitLab
```

Start with inspection, then stage a coherent change:

```sh
git status --short
git diff
git add scripts/train.py params.json
git diff --staged
git commit -m "Adjust training split and document the result"
git log --oneline --graph --decorate -10
```

`git diff` shows unstaged edits to tracked files; `git diff --staged` shows the
next commit. New untracked files appear in `git status`. Prefer explicit paths
or `git add -p` for selected hunks. A useful commit message describes the change.

## Branch, synchronize, and merge

Start from a clean working tree and an updated default branch:

```sh
git switch main
git pull --ff-only
git switch -c feature/update-dataset
```

Make changes, verify them, then commit. A branch gives the work a name without
duplicating the project folder. Push it and request review as in
[chapter 03](03-collaboration.md).

To incorporate newer work from the shared main branch:

```sh
git fetch origin
git switch feature/update-dataset
git merge origin/main
```

`fetch` updates your view of the remote; `merge` integrates it into your branch.
`pull --ff-only` updates a branch only when no merge is needed. If it refuses,
inspect the divergent history before choosing how to integrate it.

For a local exercise with no reviewer, return to `main` and merge the feature:

```sh
git switch main
git merge --ff-only feature/update-dataset
git branch -d feature/update-dataset
```

For shared repositories, merge through a pull/merge request instead. After it is
merged remotely, switch to `main`, run `git pull --ff-only`, then delete the local
feature branch. `-d` may refuse after a squash merge because the original commits
are not ancestors of `main`; inspect the result before deciding to force deletion.

## Resolve a conflict

A conflict means Git cannot choose how competing edits should be combined.
Use `git status` to find the files. Edit each conflict block to the intended final
content and remove `<<<<<<<`, `=======`, and `>>>>>>>` markers. Then:

```sh
git add path/to/resolved-file
git diff --staged
git commit
```

Run the relevant checks before committing. To cancel an in-progress merge, use
`git merge --abort`. PyCharm's three-way merge editor can help compare both sides.
For generated DVC metadata, follow the conflict guidance in [chapter 04](04-dvc.md).

## Undo the right thing

| Situation | Command | Effect |
| --- | --- | --- |
| Staged the wrong file | `git restore --staged FILE` | Unstage it; keep the edited file |
| Want to discard an unstaged edit | `git restore FILE` | Replace it with the staged version, or HEAD if unchanged in staging |
| Need to undo a shared commit | `git revert COMMIT` | Create a new commit reversing that change |
| Need to find a previous local position | `git reflog` | Inspect recent HEAD movements |

`git restore FILE` discards the affected working-tree edits: inspect `git diff`
first. Avoid `reset --hard`, `clean -fd`, and force-push as routine cleanup.
`revert` preserves shared history. See [git restore](https://git-scm.com/docs/git-restore)
and [git revert](https://git-scm.com/docs/git-revert).

For unfinished work before switching branches:

```sh
git stash push -u -m "WIP before switching branches"
git stash list
git stash pop
```

`-u` includes untracked files, but not ignored DVC data or model contents.
Stash is temporary local storage, not a backup.

## Mark and inspect a version

```sh
git tag -a v0.1.0 -m "First reproducible baseline"
git show v0.1.0
git switch --detach v0.1.0
git switch main
```

Detached HEAD is suitable for inspection. Create a branch with `git switch -c
fix/from-baseline` before making work you want to keep. Push a specific tag with
`git push origin v0.1.0`. In a DVC project, switching Git versions must be followed
by restoring the matching data and model; a Git tag alone does not contain them.

Further reading: [Pro Git](https://git-scm.com/book/en/v2).
