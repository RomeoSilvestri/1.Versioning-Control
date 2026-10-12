# 03 · Collaborate on GitHub or GitLab

[← Everyday Git](02-git.md) · [Contents](../README.md) · [Next: DVC →](04-dvc.md)

GitHub and GitLab host repositories and provide a place to review changes before
merging them. The Git operations are the same on both hosts.

| Concept | GitHub | GitLab |
| --- | --- | --- |
| Hosted repository | Repository | Project repository |
| Proposed change | Pull request (PR) | Merge request (MR) |
| Branch receiving the change | Base branch | Target branch |
| Branch containing the change | Compare branch | Source branch |

## Connect your repository

If you cloned the project, `origin` is normally already configured. Check it with:

```sh
git remote -v
```

For an existing local project without a remote, create an empty repository on
your chosen host, then connect it:

```sh
git remote add origin https://HOST/NAMESPACE/REPOSITORY.git
```

Replace the URL. In PyCharm, use **Git → Manage Remotes**. GitHub Desktop's
**Publish repository** can create and connect a GitHub repository directly.

Use the app sign-in from [chapter 01](01-setup.md#authentication).
GitHub Desktop can manage GitLab clones, but its GitHub login does not authenticate
you to GitLab. Use PyCharm's GitLab integration, or configure Git credentials/SSH
as described in the [reference](06-reference.md#authentication-and-storage).

## Propose and review a change

1. Create a feature branch from an updated `main`.
2. Edit, check, and commit the change.
3. If data or models changed, run `uv run dvc push` before pushing Git.
4. Push the branch and open a PR/MR.
5. Address feedback on the same branch, commit, and push again.
6. Merge the accepted PR/MR on the host, then update your local `main`.

For example, publish a committed feature branch with:

```sh
git push -u origin feature/update-dataset
```

On GitHub, open **Pull requests → New pull request**, with `main` as the base
and your feature as the compare branch. On GitLab, use **Merge requests → New
merge request**, with the feature as source and `main` as target.
Describe the change and the checks you ran. For data/model changes, include the
changed data, parameters, and metrics. Use a draft while the work is incomplete.

| Step | PyCharm | GitHub Desktop |
| --- | --- | --- |
| Push the feature | **Git → Push** | **Publish branch**, then **Push origin** |
| Open a review | **Pull Requests** / **Merge Requests** tool window, or the host website | For GitHub, **Preview Pull Request → Create Pull Request**; for GitLab, use its website |
| Update after merge | Branch selector → `main` → **Checkout**, then **Git → Pull** | **Current Branch → main**, then **Fetch origin → Pull origin** |

The terminal equivalent after a remote merge is:

```sh
git switch main
git pull --ff-only
uv sync --locked
```

For a DVC project, also run `uv run dvc pull` to retrieve the matching data and
models. Git shares code and metadata; DVC shares artifact contents through its
own storage. [Chapter 04](04-dvc.md) explains that storage.

## Team convention

Choose GitHub or GitLab as the project's main host. Agree on using feature
branches and reviews before merging into `main`. For a team repository, configure
branch protection to enforce that workflow; setup links are in
[chapter 06](06-reference.md#team-repository-settings).

Documentation: [GitHub PRs](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request),
[GitLab MRs](https://docs.gitlab.com/user/project/merge_requests/creating_merge_requests/),
[Desktop pull requests](https://docs.github.com/en/desktop/working-with-your-remote-repository-on-github-or-github-enterprise/creating-an-issue-or-pull-request-from-github-desktop).
