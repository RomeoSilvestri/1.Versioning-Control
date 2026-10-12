# 04 · Version datasets and models with DVC

[← Collaboration](03-collaboration.md) · [Contents](../README.md) · [Next: Lab →](05-hands-on-lab.md)

## What Git stores, and what DVC stores

Git is useful for source and small reviewable text. DVC records hashes of datasets
and model artifacts in Git-tracked metadata. The actual contents live in a local
cache and, when shared, a separate DVC remote. GitHub/GitLab are the Git remote;
a storage folder, object store, or other supported backend is the DVC remote.

| Keep in Git | Keep out of Git |
| --- | --- |
| Code, docs, `pyproject.toml`, `uv.lock`, parameters | `.venv/`, `.idea/`, tokens, private keys |
| `.dvc/config`, `.dvc/.gitignore`, `.dvcignore` | `.dvc/cache/`, `.dvc/tmp/`, `.dvc/config.local` |
| `*.dvc`, `dvc.yaml`, generated `dvc.lock` | DVC-tracked dataset/model contents |
| Small `metrics.json` in this example | Machine-specific storage and credentials |

Small public fixtures can stay in Git. DVC is useful when files are large, binary,
frequently replaced, or need storage separate from the source repository.
Do not version the same output with both `dvc add` and a pipeline stage.

## Initialize and track an input file

In a Git project with DVC installed (`uv add dvc` for a new project):

```sh
uv run dvc init
uv run dvc add data/raw/samples.csv
git add .dvc .dvcignore .gitignore data/raw/samples.csv.dvc
git commit -m "Track the baseline dataset with DVC"
```

The file must exist before `dvc add`. That command caches its contents and writes
`samples.csv.dvc`, a small pointer containing its hash, size, and relative path.
If needed, DVC also creates a nearby `.gitignore`; commit it too. The tutorial's
root `.gitignore` already ignores generated CSVs and models.

If a file was previously tracked by Git, first use `git rm --cached FILE`, which
keeps its working copy, then `dvc add FILE`. This affects future commits; old Git
history still contains the file.
See [DVC's introduction](https://doc.dvc.org/start).

## Store and retrieve contents

The lab uses a sibling directory as storage, avoiding cloud setup:

```sh
uv run dvc remote add --local -d storage ../versioning-dvc-store
uv run dvc remote list
uv run dvc push
```

`--local` records machine-specific configuration in ignored `.dvc/config.local`.
`-d` selects the default remote. A clone will need to configure this local remote
again. A relative path is resolved against the DVC project root.
This storage survives deleting the working copy, but a folder on the same disk is
only a teaching remote, not an independent backup.

For a team, use shared storage accessible to everyone. For example, with the
appropriate backend dependency installed:

```sh
uv add "dvc[s3]"
uv run dvc remote add -d storage s3://YOUR-BUCKET/YOUR-PREFIX
git add pyproject.toml uv.lock .dvc/config
```

Configure credentials through the backend's credential mechanisms or ignored local
settings. The example URL is a placeholder, not a provisioned bucket.
See [remote storage](https://doc.dvc.org/user-guide/data-management/remote-storage)
and [`remote add`](https://doc.dvc.org/command-reference/remote/add).

| Command | Action |
| --- | --- |
| `uv run dvc push` | Upload cached contents referenced by the current version |
| `uv run dvc fetch` | Download contents into the cache only |
| `uv run dvc checkout` | Restore matching files from the local cache |
| `uv run dvc pull` | Fetch and then check out matching files |
| `uv run dvc status` | Check workspace consistency against DVC metadata |

Run `dvc push` for each version you want to share. Pushing Git alone does not
upload artifacts; pulling DVC alone does not select a different Git revision.

## Record how an artifact was produced

The included [`dvc.yaml`](../dvc.yaml) defines one stage: run `scripts/train.py`
with a dataset and `train_fraction` from `params.json`, produce a cached JSON
model, and record a small metric file with `cache: false` so it can be kept in Git.

```sh
uv run dvc repro
uv run dvc dag
uv run dvc metrics show
git add scripts/train.py params.json dvc.yaml dvc.lock metrics.json
git commit -m "Record model recipe and baseline metrics"
```

DVC generates `dvc.lock` with the resolved input/output hashes and parameter
values. Re-running without changes skips an up-to-date stage; changing a declared
dependency or parameter makes it eligible to run again. `uv run dvc repro` makes
the stage's `python` command use the project environment. DVC does not install
Python dependencies itself.

When data changes, run `dvc add` again to update its standalone pointer, then
`dvc repro` and commit both the data pointer and pipeline record. A model produced
by this stage is already tracked through `dvc.lock`; do not `dvc add` it separately.

This is a local recipe for reproducing a version, not a production scheduler.
Reproducibility also depends on declared inputs, deterministic code, and the
runtime; a Python lockfile does not freeze hardware or operating systems.
See [DVC pipeline files](https://doc.dvc.org/user-guide/project-structure/dvcyaml-files)
and [parameter formats](https://doc.dvc.org/command-reference/params).

## Recover and compare versions

With a clean working tree and a real tag named `baseline-v1`:

```sh
git switch --detach baseline-v1
uv sync --locked
uv run dvc checkout
uv run dvc status
```

If the cache is missing, use `dvc pull` with a configured remote instead.
`checkout` restores dataset/model bytes; `repro` executes or restores the recipe
and may update metadata. Use checkout/pull to recover a recorded artifact.

Compare a previous Git revision with your current workspace:

```sh
uv run dvc diff baseline-v1
uv run dvc params diff baseline-v1
uv run dvc metrics diff baseline-v1
```

Return with `git switch main`, `uv sync --locked`, and `uv run dvc checkout` (or
`pull`). These steps also apply after a branch switch or `git revert`.

For metadata conflicts, choose the intended dataset version or regenerate the
intended dataset and run `dvc add`. Resolve code and parameters, run `dvc repro`
to regenerate `dvc.lock`, then review and commit all related files. Do not invent
hashes by manually combining lockfile entries. Push the resulting artifacts
before sharing the merge.
