# 05 · A complete local lab

[← DVC](04-dvc.md) · [Contents](../README.md) · [Next: Quick reference →](06-reference.md)

**Goal:** create two versions, recover the first exactly, then retrieve the latest
from a fresh clone. Allow about 20–30 minutes. Run the commands in PowerShell
from the indicated directory. No hosted repository is required.

The example fits `y = slope * x + intercept`: the first 80% of rows train the
model and the rest evaluate it. Version 2 adds 20 rows with shifted targets,
making the model and metrics change. The task is intentionally small and deterministic.

With the default `train_fraction` of `0.8`, the checkpoints are:

| Dataset | Total rows | Train / test rows | Test MSE (approximately) |
| --- | --- | --- | --- |
| v1 | 40 | 32 / 8 | 0.0741703 |
| v2 | 60 | 48 / 12 | 1.0712060 |

## Use PyCharm or GitHub Desktop for the lab's Git steps

The command blocks below are the complete terminal path. You can replace their
Git actions with the desktop equivalents while keeping all `uv`, Python, and DVC
commands in the project terminal. Open the lab folder in PyCharm; after `git init`,
register that same folder in Desktop with **File → Add Local Repository**.
This is a local Git exercise: use **Commit**, and leave **Publish repository** /
**Publish branch** for the hosted workflow in chapter 03.

| Lab step | Desktop alternative |
| --- | --- |
| 2: Stage and commit | PyCharm's **Commit** window or Desktop's **Changes**: select the source files and DVC metadata listed in the commands, inspect diffs, and commit |
| 2 and 3: Tag the committed result | PyCharm **Git → New Tag** with a message; Desktop **History → right-click the new commit → Create Tag** |
| 3: Create/switch branches | PyCharm's branch selector or Desktop's **Current Branch → New Branch**; name it `feature/dataset-v2` and base it on `main` |
| 3: Commit and merge v2 | Commit the three changed metadata/metric files, run `dvc push`, switch to `main`, and merge `feature/dataset-v2` |
| 4: Inspect v1, then return | Check out `baseline-v1` through PyCharm's **Tags** or Desktop's tagged commit in **History → Checkout Commit**; then use the branch selector to return to `main` |
| 5: Create the fresh local clone | Run the provided `git clone` command, then open the clone in either app |

GUI commits must include the `.dvc` metadata and generated `dvc.lock`, not the
ignored CSV/model contents. Every GUI version switch still needs the following
`uv sync --locked` and DVC checkout/pull from the command block. See the
[full action mapping](06-reference.md#git-commands-and-desktop-equivalents).

## 1. Create a practice project and its first artifacts

Before running the commands, read the example in the tutorial folder:
`create_lab.py` copies the practice project; `make_data.py` generates the dataset;
`train.py` fits the model and writes metrics. Read `params.json` and `dvc.yaml`
alongside `train.py` to see what DVC records.

From the **tutorial repository root**:

```sh
uv sync --locked
uv run python scripts/create_lab.py ../versioning-lab
cd ../versioning-lab
git init -b main
uv run dvc init
uv run python scripts/make_data.py --version 1
uv run dvc add data/raw/samples.csv
uv run dvc repro
uv run dvc metrics show
uv run dvc status
```

If you already ran the README quickstart, continue at step 2 in that lab directory.
The helper refuses existing destinations and does not copy Git history or local
state. In PyCharm, open this new folder and reuse its uv environment.

Expected: 40 data rows, 32 training rows, 8 test rows, `models/model.json`,
`metrics.json`, `data/raw/samples.csv.dvc`, and `dvc.lock`.
Open the pointer and lockfile: Git will record hashes, not the dataset/model bytes.

## 2. Commit, tag, and upload the baseline

Still in **versioning-lab**; check your Git name/email as in chapter 01:

```sh
uv run python -m unittest discover -s tests -v
git add README.md LICENSE .gitattributes .gitignore pyproject.toml uv.lock docs scripts tests
git add .dvc .dvcignore data/raw/samples.csv.dvc params.json dvc.yaml dvc.lock metrics.json
git diff --staged --stat
git commit -m "Record reproducible baseline"
git tag -a baseline-v1 -m "Dataset v1 and its matching model"
uv run dvc remote add --local -d storage ../versioning-dvc-store
uv run dvc push
git status --short
```

Expected: an empty Git status and a storage directory next to the lab. Use
`git ls-files` to confirm the CSV and model are absent, while their metadata is
tracked. Both the baseline dataset and model are now available outside the cache.

## 3. Change data on a feature branch

```sh
git switch -c feature/dataset-v2
uv run python scripts/make_data.py --version 2
uv run dvc status
uv run dvc add data/raw/samples.csv
uv run dvc repro
uv run dvc diff baseline-v1
uv run dvc metrics diff baseline-v1
git add data/raw/samples.csv.dvc dvc.lock metrics.json
git diff --staged
git commit -m "Train on dataset v2"
uv run dvc push
git switch main
git merge feature/dataset-v2
git tag -a dataset-v2 -m "Dataset v2 and its matching model"
```

Expected: 60 rows, a 48/12 split, different model coefficients, and higher test
MSE. The first `dvc status` detects the edited input even though Git ignores the
CSV. The local merge demonstrates the mechanics; on GitHub/GitLab, publish the
branch and use the review workflow in chapter 03 instead.

## 4. Recover the baseline and return

Start with a clean Git status:

```sh
git switch --detach baseline-v1
uv sync --locked
uv run dvc status
uv run dvc checkout
uv run dvc metrics show
uv run dvc status
git switch main
uv sync --locked
uv run dvc checkout
uv run dvc status
```

Before checkout, Git has switched metadata and metrics, while ignored data and
models may still belong to v2. After checkout, v1 has 40 rows and the 32/8 split
again. Returning to `main` and checking out restores v2. Nothing needs to be
retrained to recover these cached versions.

## 5. Simulate a teammate with an empty cache

From **versioning-lab**, move to its parent and clone:

```sh
cd ..
git clone versioning-lab versioning-clone
cd versioning-clone
uv sync --locked
uv run dvc remote add --local -d storage ../versioning-dvc-store
uv run dvc pull
uv run dvc metrics show
uv run dvc status
uv run dvc repro
git status --short
```

Expected: v2's dataset and model are restored; the stage is skipped and Git status
is empty. The clone did not receive `.dvc/cache` or `.dvc/config.local` from Git.
It succeeded because the Git revision and accessible DVC storage together identify
and provide the artifacts. To retrieve v1 here, switch to `baseline-v1` and run
`uv run dvc pull`; v1 was uploaded in step 2.

**Checkpoint:** you should be able to explain which command shares code, which
shares artifacts, and why changing a Git revision requires a DVC checkout/pull.
Keep the sibling storage directory while practicing recovery from either clone.
