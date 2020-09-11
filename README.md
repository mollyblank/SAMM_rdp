# SAMM Raw Data Processing

[![Build Status](https://github.com/mollyblank/samm_rdp/workflows/Build%20Master/badge.svg)](https://github.com/mollyblank/samm_rdp/actions)
[![Documentation](https://github.com/mollyblank/samm_rdp/workflows/Documentation/badge.svg)](https://mollyblank.github.io/samm_rdp)
[![Code Coverage](https://codecov.io/gh/mollyblank/samm_rdp/branch/master/graph/badge.svg)](https://codecov.io/gh/mollyblank/samm_rdp)

Cleans REDCap data for the Save Access to Maternal Medicines study. Will outpuot clean data files ready for processing

---

## Features
* Store values and retain the prior value in memory
* ... some other functionality


## Installation
**Stable Release:** `pip install samm_rdp`<br>
**Development Head:** `pip install git+https://github.com/mollyblank/samm_rdp.git`

## Quick Start
```python
from samm_rdp import process

csv_path = "Path to csv file"
timepoints_out_path = "Path to output timepoints file"
patients_out_path = "Path to output patients file"

process.process(csv_path=csv_path, timepoints_out_path=timepoints_out_path, patients_out_path=patients_out_path))
# This will take a little bit of time
```
Alternatively you can run this from the command line with:
```bash
samm_rdp \
  --csv_path "D:\Dropbox (Shift Labs)\Shift Labs Team folder (1)\Grants\SLAB USAID\DATA - Study summary reports - data - analysis\Data processing\Renamed_SAMM_CURRENT_COMPLETE_combined2.csv" \
  --timepoints_out_path "timepoints.csv" \
  --patients_out_path "patients.csv"
```


<!-- 
## Documentation
For full package documentation please visit [mollyblank.github.io/samm_rdp](https://mollyblank.github.io/samm_rdp).
 -->
<!-- 
## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

## The Four Commands You Need To Know
1. `pip install -e .[dev]`

    This will install your package in editable mode with all the required development
    dependencies (i.e. `tox`).

2. `make build`

    This will run `tox` which will run all your tests in both Python 3.7
    and Python 3.8 as well as linting your code.

3. `make clean`

    This will clean up various Python and build generated files so that you can ensure
    that you are working in a clean environment.

4. `make docs`

    This will generate and launch a web browser to view the most up-to-date
    documentation for your Python package.

#### Additional Optional Setup Steps:
* Turn your project into a GitHub repository:
  * Make sure you have `git` installed, if you don't, [follow these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  * Make an account on [github.com](https://github.com)
  * Go to [make a new repository](https://github.com/new)
  * _Recommendations:_
    * _It is strongly recommended to make the repository name the same as the Python
    package name_
    * _A lot of the following optional steps are *free* if the repository is Public,
    plus open source is cool_
  * After a GitHub repo has been created, run the following commands:
    * `git remote add origin git@github.com:mollyblank/samm_rdp.git`
    * `git push -u origin master`
* Register samm_rdp with Codecov:
  * Make an account on [codecov.io](https://codecov.io)
  (Recommended to sign in with GitHub)
  * Select `mollyblank` and click: `Add new repository`
  * Copy the token provided, go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/mollyblank/samm_rdp/settings/secrets),
  add a secret called `CODECOV_TOKEN` with the token you just copied.
  Don't worry, no one will see this token because it will be encrypted.
* Generate and add an access token as a secret to the repository for auto documentation
generation to work
  * Go to your [GitHub account's Personal Access Tokens page](https://github.com/settings/tokens)
  * Click: `Generate new token`
  * _Recommendations:_
    * _Name the token: "Auto-Documentation Generation" or similar so you know what it
    is being used for later_
    * _Select only: `repo:status`, `repo_deployment`, and `public_repo` to limit what
    this token has access to_
  * Copy the newly generated token
  * Go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/mollyblank/samm_rdp/settings/secrets),
  add a secret called `ACCESS_TOKEN` with the personal access token you just created.
  Don't worry, no one will see this password because it will be encrypted.
* Register your project with PyPI:
  * Make an account on [pypi.org](https://pypi.org)
  * Go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/mollyblank/samm_rdp/settings/secrets),
  add a secret called `PYPI_TOKEN` with your password for your PyPI account.
  Don't worry, no one will see this password because it will be encrypted.
  * Next time you push to the branch: `stable`, GitHub actions will build and deploy
  your Python package to PyPI.
  * _Recommendation: Prior to pushing to `stable` it is recommended to install and run
  `bumpversion` as this will,
  tag a git commit for release and update the `setup.py` version number._
* Add branch protections to `master` and `stable`
    * To protect from just anyone pushing to `master` or `stable` (the branches with
    more tests and deploy
    configurations)
    * Go to your [GitHub repository's settings and under the `Branches` tab](https://github.com/mollyblank/samm_rdp/settings/branches), click `Add rule` and select the
    settings you believe best.
    * _Recommendations:_
      * _Require pull request reviews before merging_
      * _Require status checks to pass before merging (Recommended: lint and test)_

#### Suggested Git Branch Strategy
1. `master` is for the most up-to-date development, very rarely should you directly
commit to this branch. GitHub Actions will run on every push and on a CRON to this
branch but still recommended to commit to your development branches and make pull
requests to master.
2. `stable` is for releases only. When you want to release your project on PyPI, simply
make a PR from `master` to `stable`, this template will handle the rest as long as you
have added your PyPI information described in the above **Optional Steps** section.
3. Your day-to-day work should exist on branches separate from `master`. Even if it is
just yourself working on the repository, make a PR from your working branch to `master`
so that you can ensure your commits don't break the development head. GitHub Actions
will run on every push to any branch or any pull request from any branch to any other
branch.
4. It is recommended to use "Squash and Merge" commits when committing PR's. It makes
each set of changes to `master` atomic and as a side effect naturally encourages small
well defined PR's.
5. GitHub's UI is bad for rebasing `master` onto `stable`, as it simply adds the
commits to the other branch instead of properly rebasing from what I can tell. You
should always rebase locally on the CLI until they fix it.

 -->
