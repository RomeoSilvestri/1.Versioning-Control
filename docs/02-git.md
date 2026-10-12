# 02 · Everyday Git

[← Setup](01-setup.md) · [Contents](../README.md) · [Next: Collaboration →](03-collaboration.md)

Use PyCharm or GitHub Desktop for routine Git work; the commands explain the
underlying operations and remain useful in the terminal. Open the **same local
repository folder** in both apps. Menu labels can vary by version; in PyCharm,
use **Find Action** to locate an action if its menu has moved. The
[quick reference](06-reference.md#git-commands-and-desktop-equivalents) collects
the CLI and both GUI paths in one table.

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

`git status` tells you which files are untracked, modified, or staged. `git diff`
shows unstaged edits to tracked files; `git diff --staged` shows the next commit.
`git add` selects the current contents for that commit; editing a file afterward
requires staging the new edits again. Use explicit paths or `git add -p` for
selected hunks. `git commit` records the staged snapshot locally; `-m` supplies
its message. `git log` lists recorded commits. A useful message describes the change.

**In PyCharm:** open the **Commit** tool window, select files (including new files
under **Unversioned Files**), inspect **Show Diff**, enter a message, and click
**Commit**. The default interface selects changes through changelists. For an
explicit Git staging area, enable **Settings → Version Control → Git → Enable
staging area**, then stage files/chunks and inspect **Staged** before committing.
See [PyCharm commits and staging](https://www.jetbrains.com/help/pycharm/commit-and-push-changes.html).

**In GitHub Desktop:** open **Changes**, select the file checkboxes and inspect
their diffs. Select individual changed lines for a partial commit. Enter a
**Summary** and click **Commit to BRANCH**. File selection is the practical
equivalent of choosing what to stage, rather than a separate staging editor.
Open **History** to inspect commits. See
[Desktop commits](https://docs.github.com/en/desktop/making-changes-in-a-branch/committing-and-reviewing-changes-to-your-project-in-github-desktop).

Renames and deletions are versioned changes too: `git mv OLD NEW` renames a
tracked file and stages the change; `git rm FILE` removes it and stages the
deletion. You can instead rename/delete in PyCharm or your file manager, then
select the resulting changes for a GUI commit. `.gitignore` excludes untracked
files, not files already recorded by Git; `git rm --cached FILE` stops tracking
a file while keeping its local copy.

## Commit, push, fetch, and pull are different operations

| Command | What it does |
| --- | --- |
| `git commit -m "Message"` | Save the selected snapshot in local history; no upload occurs |
| `git push -u origin BRANCH` | Send local commits to the remote branch; `-u` sets its upstream for later plain `git push`/`git pull` |
| `git fetch origin` | Download remote commits and update remote-tracking references, without changing your checked-out files |
| `git pull --ff-only` | Fetch and advance the current branch from its upstream; refuse if histories have diverged |

Saving a file does not commit it. Committing does not push it. Fetching does not
apply remote changes to your files. Pull updates your local branch; it does not
send your work to the remote. `origin` is a remote name, usually created by clone.

| Operation | PyCharm | GitHub Desktop |
| --- | --- | --- |
| Fetch | **Git → Fetch** | **Fetch origin** |
| Pull | **Git → Pull**; select the remote/branch and **Modify options → `--ff-only`** | **Fetch origin**, then **Pull origin** when incoming commits are available |
| Push | **Git → Push**; inspect target branch and outgoing commits, then **Push** | **Publish branch** for a new branch, then **Push origin** for later commits |

PyCharm's **Update Project** uses its selected merge/rebase strategy; it is not
automatically a fast-forward-only pull. Desktop's **Pull origin** also does not
provide the same explicit `--ff-only` guard. Use the terminal when that exact
behavior matters. **Commit and Push** combines two operations in PyCharm; for a
DVC change, commit first, run `uv run dvc push`, then push Git.
See [PyCharm synchronization](https://www.jetbrains.com/help/pycharm/sync-with-a-remote-repository.html),
[Desktop synchronization](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/syncing-your-branch-in-github-desktop),
and [Desktop pushes](https://docs.github.com/en/desktop/making-changes-in-a-branch/pushing-changes-to-github-from-github-desktop).

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

For this sequence in PyCharm, use the **branch selector → main → Checkout**, pull,
then **New Branch**. In Desktop, use **Current Branch → main**, fetch/pull, then
**New Branch** with `main` as its base. Both interfaces switch you to the new branch.

To incorporate newer work from the shared main branch:

```sh
git fetch origin
git switch feature/update-dataset
git merge origin/main
```

`fetch` updates your view of the remote; `merge` integrates it into your branch.
`pull --ff-only` updates a branch only when no merge is needed. If it refuses,
inspect the divergent history before choosing how to integrate it.

For a merge in PyCharm, check out the receiving branch, then use **Git → Merge**
and select the source branch; **Modify options → `--ff-only`** applies the same
guard when wanted. In Desktop, select the receiving branch, then **Current Branch
→ Choose a branch to merge into BRANCH**, choose the source, and merge. The default
GUI merge may create a merge commit; use CLI for an explicit `--ff-only` merge in
Desktop. See [PyCharm merges](https://www.jetbrains.com/help/pycharm/apply-changes-from-one-branch-to-another.html).

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

PyCharm's branch selector offers **Delete**, while Desktop uses **Branch → Delete**
for the selected branch. Inspect what is being removed: PyCharm's GUI deletion can
delete unmerged branches, unlike the `git branch -d` guard. Desktop may also offer
remote-branch deletion; leave that unchecked if only deleting the local branch.
See [PyCharm branches](https://www.jetbrains.com/help/pycharm/manage-branches.html)
and [Desktop branches](https://docs.github.com/en/desktop/making-changes-in-a-branch/managing-branches-in-github-desktop).

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
`git merge --abort`. In PyCharm, select **Resolve Conflicts → Resolve Manually**,
review the three-way result, and finish the merge. Desktop shows the conflicting
files; open them in PyCharm or your editor, save the resolution, then return to
Desktop to complete the merge. See
[PyCharm conflict resolution](https://www.jetbrains.com/help/pycharm/resolve-conflicts.html).
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

In PyCharm, **Rollback** on an uncommitted file discards edits; **Git → Log →
right-click commit → Revert Commit** creates a reversing commit. In Desktop,
**Changes → right-click file → Discard Changes** discards edits, while **History →
right-click commit → Revert Changes in Commit** preserves history with a new commit.
Simply deselecting a file excludes it from the next GUI commit and keeps its edits;
it does not discard them. With explicit staging enabled, use PyCharm's **Unstage**
for `git restore --staged`. **Undo Commit** is for revising local history, so use
**Revert** for already shared commits. See
[PyCharm undo actions](https://www.jetbrains.com/help/pycharm/undo-changes.html) and
[Desktop revert](https://docs.github.com/en/desktop/managing-commits/reverting-a-commit-in-github-desktop).

With a separately staged version, `git restore FILE` restores from the index;
GUI Rollback/Discard may discard changes back to the last commit instead. Use
CLI when you specifically need to preserve that staged version.

For unfinished work before switching branches:

```sh
git stash push -u -m "WIP before switching branches"
git stash list
git stash pop
```

`-u` includes untracked files, but not ignored DVC data or model contents.
Stash is temporary local storage, not a backup.

In PyCharm's Commit window, use **Git → Stash Changes** from the context menu,
then the **Stash** tab's **Pop** to restore and remove the stash. **Shelve Changes**
is a separate IDE mechanism, not a Git stash. In Desktop, right-click the changed
files header and choose **Stash All Changes**; restore from **Stashed Changes →
Restore** on that branch. Desktop manages one stashed set at a time. Use CLI for
multiple named stashes or to explicitly include untracked files with `-u`.
See [PyCharm stash/shelf](https://www.jetbrains.com/help/pycharm/shelving-and-unshelving-changes.html)
and [Desktop stash](https://docs.github.com/en/desktop/making-changes-in-a-branch/stashing-changes-in-github-desktop).

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

In PyCharm, use **Git → New Tag**, fill in **Message** for an annotated tag, and
create it. Use **branch selector → Tags → TAG → Checkout** to inspect that version.
In Desktop, use **History → right-click commit → Create Tag**; to inspect its files,
right-click that tagged commit and choose **Checkout Commit**. Return to `main`
with either app's branch selector. Selecting a commit in the log/history alone
only displays it; checkout changes the files. See
[PyCharm tags](https://www.jetbrains.com/help/pycharm/use-tags-to-mark-specific-commits.html),
[Desktop tags](https://docs.github.com/en/desktop/managing-commits/managing-tags-in-github-desktop),
and [Desktop checkout](https://docs.github.com/en/desktop/managing-commits/checking-out-a-commit-in-github-desktop).

Further reading: [Pro Git](https://git-scm.com/book/en/v2).
