# Dependency locks

`pyproject.toml` owns direct dependencies. The committed lock files own exact,
hashed installation closures:

- `runtime.lock` contains the runtime and build requirements.
- `development.lock` contains the runtime closure plus tests and lock tooling.

Regenerate deliberately from the repository development environment:

```bash
.venv/bin/python -m piptools compile --allow-unsafe --extra bootstrap \
  --generate-hashes --resolver=backtracking \
  --output-file requirements/runtime.lock pyproject.toml

.venv/bin/python -m piptools compile --allow-unsafe --extra bootstrap \
  --extra development --generate-hashes \
  --resolver=backtracking --output-file requirements/development.lock \
  pyproject.toml
```

Normal bootstrap installs a committed lock with `--require-hashes`; it never
resolves a new dependency version.
