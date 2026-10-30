# Project 2 - CI/CD pipeline (GitHub Actions)

**Goal:** every change is linted, tested, scanned and packaged automatically.

The workflow file lives at the repo root, because GitHub only reads workflows from
`.github/workflows/`:

```
.github/workflows/devops-capstone-ci.yml
```

## Pipeline

```
push / pull request
        |
   [ test ]  flake8 -> pytest
        |
   [ build ] docker build -> Trivy scan (fail on CRITICAL)
        |
   only on push to main:  login to ghcr.io -> push image (:latest and :sha)
```

## What this shows
- Triggers with `paths` filters (the pipeline runs only when this project changes)
- Job dependencies (`needs`) - the build never runs if tests fail
- Dependency and Docker layer caching
- Security scanning in the pipeline ("shift left")
- Publishing an image to a registry with the built-in `GITHUB_TOKEN`
- Least privilege: `permissions` are set explicitly

## Use it
1. Push this project to your repository (see the main README).
2. Open the **Actions** tab on GitHub and watch the run.
3. After a push to `main`, find the image under your profile -> **Packages**.
4. Make a test fail on purpose (change an assert in `app/tests/test_main.py`),
   push on a branch, open a Pull Request, and see the red check.

## If the push of the workflow file is rejected
GitHub needs the `workflow` permission to accept workflow files:
```powershell
gh auth refresh -s workflow
```

## Interview questions this prepares you for
- CI vs CD? What does `needs` do? Why cache?
- Why scan images and what is `ignore-unfixed`?
- Why use `GITHUB_TOKEN` instead of a personal password?

## Next improvement (try it yourself)
Add a `deploy` job that runs only after the image is pushed.
