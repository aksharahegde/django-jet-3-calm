# Releasing django-jet-calm on PyPI

## Release checklist

1. Bump version in `jet/__init__.py`, `pyproject.toml`, `setup.py`, and `package.json`.
2. Update `CHANGELOG.md` and commit.
3. Push to `main`, tag, and publish a GitHub release (keep release notes/description as a changelog link):
   ```bash
   git tag -a vX.Y.Z -m "Release X.Y.Z"
   git push origin main vX.Y.Z
   gh release create vX.Y.Z \
     --title "vX.Y.Z" \
     --notes "Release notes: https://github.com/aksharahegde/django-jet-3-calm/blob/main/CHANGELOG.md"
   ```
4. Build and upload to PyPI from your machine (see below).

## Build and publish locally

```bash
rm -rf dist build *.egg-info
python -m pip install --upgrade build twine
python -m build
twine check dist/*
twine upload dist/*
```

Use a PyPI API token when prompted, or configure `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-...
```

Confirm the wheel contains static assets and locales:

```bash
unzip -l dist/django_jet_calm-*-py3-none-any.whl | grep -E 'bundle.min.js|jet/locale|jet/templates'
```

## Links

- **Package:** https://pypi.org/project/django-jet-calm/
- **Install:** `pip install django-jet-calm==5.4.7`
