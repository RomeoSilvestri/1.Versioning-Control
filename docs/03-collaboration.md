# 03 · Collaborate on GitHub or GitLab

[← Everyday Git](02-git.md) · [Contents](../README.md) · [Next: DVC →](04-dvc.md)

The Git commands are the same for both hosts. The hosting interface provides
permissions, issues, reviews, and branch policies.

| Concept | GitHub | GitLab |
| --- | --- | --- |
| Hosted Git repository | Repository | Project repository |
| Proposed change | Pull request (PR) | Merge request (MR) |
| Review target | Base branch | Target branch |
| Work to integrate | Compare/head branch | Source branch |
| Main-branch policy | Rulesets / branch protection | Branch rules / protected branches |

## Connect a remote and authenticate

```sh
git remote -v
git remote add origin https://HOST/NAMESPACE/REPOSITORY.git
```

Replace the URL. Cloning normally already creates `origin`; skip `remote add` in
that case. To change a URL, use `git remote set-url origin URL`.
HTTPS uses a credential manager or a host-issued token, subject to organization
policy. GitHub/GitLab account passwords are not the normal Git HTTPS credential.
SSH uses a key associated with your account. Keep private keys and tokens out of
source files and clone URLs. Authentication for Git and for DVC storage is separate.

GitHub Desktop supports its GitHub sign-in workflow. For GitLab, use a credential
manager or SSH for terminal Git, or configure PyCharm's GitLab account integration.
See [GitHub authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github)
and [GitLab SSH](https://docs.gitlab.com/user/ssh/).

## A small review workflow

On a feature branch with a committed change, upload any new DVC artifacts first:

```sh
# For initialized DVC projects with a configured remote:
uv run dvc push
git push -u origin feature/update-dataset
```

`-u` sets the upstream branch; later pushes can use `git push`.
If the change introduces DVC artifacts, upload them with `uv run dvc push`
**before** publishing the Git revision. Otherwise a reviewer may have the pointers
but be unable to retrieve their files.

On GitHub, open **Pull requests → New pull request**, choose `main` as the base
and your feature branch as the compare branch. On GitLab, open **Merge requests →
New merge request**, choose the feature as source and `main` as target.
Use a draft while work is incomplete, describe the resulting behavior, and record
the checks you ran. For data/model changes, include the data revision, changed
parameters, and metrics. This repository includes templates for both hosts.

Address review feedback on the same branch, commit, and push again. When accepted,
merge in the host interface, then update your local checkout:

```sh
git switch main
git pull --ff-only
uv sync --locked
uv run dvc pull
```

The DVC command applies only to initialized DVC projects with an accessible remote.
Git pulls code and metadata; DVC pulls the associated file contents.
Official walkthroughs: [GitHub PRs](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request)
and [GitLab MRs](https://docs.gitlab.com/user/project/merge_requests/creating_merge_requests/).

## Protect main and keep one source of truth

For a team, configure the main branch to require review and prohibit routine
direct pushes and force-pushes. On GitHub, use repository rulesets/branch protection;
on GitLab, use **Settings → Repository → Branch rules**. Available policies depend
on your plan and permissions. On GitLab, explicitly set **Allowed to push and
merge → No one** if changes must go through MRs; do not rely on an empty setting.
See [GitHub protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
and [GitLab protected branches](https://docs.gitlab.com/user/project/repository/branches/protected/).

Use one host as the canonical repository. You can add a second remote named
`gitlab` or `github` for a mirror, but it has independent permissions and reviews;
pushing to one does not update the other. A Git fork is also a separate repository:
push to your fork and open a PR/MR against the original project when you lack write
access there.

## Review from PyCharm

Use the Commit tool window to inspect diffs, the branch selector to switch or
create branches, and the Git log to inspect history. PyCharm can integrate both
GitHub PRs and GitLab MRs when the relevant account/plugin is configured.
The IDE operates on the same repository as terminal Git. DVC commands still run
in the project terminal with `uv run dvc ...`.
See [PyCharm Git integration](https://www.jetbrains.com/help/pycharm/using-git-integration.html).
