# CoBrowser

CoBrowser is a tool for secure backend automation involving sensitive user information.

## Running locally

Install the dependencies:

```
pip3 install -e .
```

Run the application:

```
python3 -m cobrowser.api.main
```

## Manual Pre-Commit Hooks

```
pre-commit run --all-files  # Run on all files
pre-commit run              # Run only on staged files
```
