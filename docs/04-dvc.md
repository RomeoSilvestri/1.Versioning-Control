# 04 · Version datasets and models with DVC

[← Collaboration](03-collaboration.md) · [Contents](../README.md) · [Next: Lab →](05-hands-on-lab.md)

## Git tracks metadata; DVC tracks contents

DVC connects data and model versions to Git commits. Their contents live in a
local **cache** and can be uploaded to a separate **DVC remote**. GitHub/GitLab
host the Git history; the DVC remote holds the artifact contents.

| Keep in Git | Keep out of Git |
| --- | --- |
| Code, docs, `pyproject.toml`, `uv.lock`, parameters | `.venv/`, `.idea/`, credentials |
| `.dvc/config`, `.dvc/.gitignore`, `.dvcignore` | `.dvc/cache/`, `.dvc/tmp/`, `.dvc/config.local` |
| `*.dvc`, `dvc.yaml`, generated `dvc.lock` | DVC-tracked datasets and models |
| Small `metrics.json` in this example | Generated files not intended for versioning |

Small public fixtures can stay in Git. DVC is useful for large files, binary
artifacts, or files you want to store separately. This tutorial uses tiny files
so you can practice the complete workflow locally.

## Track a dataset

In an existing Git project, install DVC with `uv add dvc` if it is not already
a dependency. Initialize DVC once, then track an existing file:

```sh
uv run dvc init
uv run dvc add data/raw/samples.csv
git add .dvc .dvcignore .gitignore data/raw/samples.csv.dvc
git commit -m "Track the baseline dataset"
```

`dvc add` caches the file and writes `samples.csv.dvc`, a small pointer with its
hash and path. Git records that pointer instead of the dataset contents.
Commit any `.gitignore` that DVC creates too; this tutorial already ignores the
generated CSVs and models.

When you update the dataset, run `dvc add` again to record its new contents.

## Record how the model is produced

The included [`dvc.yaml`](../dvc.yaml) defines a single training step:

- **Command:** run `scripts/train.py`.
- **Inputs:** the script, dataset, and `train_fraction` in `params.json`.
- **Outputs:** the model and metrics.

```sh
uv run dvc repro
uv run dvc metrics show
git add scripts/train.py params.json dvc.yaml dvc.lock metrics.json
git commit -m "Record model recipe and metrics"
```

`repro` runs the step when a declared input changes and skips it when up to date.
It generates `dvc.lock`, which records the input/output hashes and parameter
values. `uv run` supplies the project's Python environment.

The model is cached through the pipeline. Do not also run `dvc add` on it.
The small metrics file uses `cache: false` in this example, so Git stores it
directly alongside the pipeline metadata.

After changing the dataset: run `dvc add`, then `dvc repro`, review metrics, and
commit the updated pointer, lockfile, and metrics together. After changing code
or parameters: run `dvc repro` and commit those changes with the updated outputs'
metadata.

## Share data and models

Configure a remote once. The lab uses a directory next to the project:

```sh
uv run dvc remote add --local -d storage ../versioning-dvc-store
uv run dvc push
```

`-d` makes it the default DVC remote. `--local` keeps this machine's storage path
in ignored `.dvc/config.local`, so each clone configures it separately.
This folder is sufficient for the lab; a team needs shared storage accessible
to everyone. See the [reference](06-reference.md#authentication-and-storage)
for storage setup beyond the lab.

| Command | Use |
| --- | --- |
| `uv run dvc push` | Upload the current version's cached artifacts |
| `uv run dvc pull` | Download and restore the artifacts matching the current Git version |
| `uv run dvc checkout` | Restore matching artifacts already in the local cache |
| `uv run dvc status` | Check whether local files match their recorded version |

Upload artifacts before pushing the Git commit that references them. A Git
push alone does not upload data/models, and a Git pull alone does not restore them.
Run DVC commands in the terminal, including PyCharm's terminal.

## Recover a version

Start with no uncommitted changes. Once the lab has created `baseline-v1`:

```sh
git switch --detach baseline-v1
uv sync --locked
uv run dvc checkout
uv run dvc status
```

Git restores code, parameters, metrics, and metadata. DVC then restores the
matching dataset/model. If the cache is empty, use `dvc pull` with a configured
remote instead of `dvc checkout`.

Return to the latest version:

```sh
git switch main
uv sync --locked
uv run dvc checkout
```

The same DVC step is needed after switching branches in PyCharm or GitHub Desktop.
Use checkout/pull to recover recorded artifacts; use repro to produce outputs
after changing their inputs. The [lab](05-hands-on-lab.md) demonstrates both.

Documentation: [DVC introduction](https://doc.dvc.org/start),
[pipeline files](https://doc.dvc.org/user-guide/project-structure/dvcyaml-files),
[remote storage](https://doc.dvc.org/user-guide/data-management/remote-storage),
[pull](https://doc.dvc.org/command-reference/pull).
