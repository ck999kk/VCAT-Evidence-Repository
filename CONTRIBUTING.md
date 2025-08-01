# Contributing to VCAT Evidence Repository

Thank you for your interest in contributing to the VCAT Evidence Repository! We value clean code, reproducible tests, and automated checks.

## Getting Started

1. **Fork** the repository and create a branch for your feature or fix:
   ```bash
   git clone https://github.com/ck999kk/VCAT-Evidence-Repository.git
   cd VCAT-Evidence-Repository
   git checkout -b feature/your-feature-name
   ```
2. **Install dependencies**:
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Make your changes**, ensuring you follow the repository's style and guidelines.

## Automated Checks (CI)

This project uses GitHub Actions to automatically run linters, tests, and validation on each push and pull request. You do not need to watch the screen—CI will inform you of any failures.

### Workflow
- **Lint & Pre-commit hooks**: `pre-commit run --all-files`
- **Unit tests**: `pytest`

If CI passes, your PR is ready for review.

## Writing Code

- Follow existing code style (PEP 8 for Python).
- Keep changes focused and minimal.
- Update documentation or tests when adding new functionality.

## Pull Request Process

1. Push your branch to your fork.
2. Open a Pull Request against `main` branch.
3. CI will run automatically. Fix any issues until checks pass.
4. Request reviews and address feedback.

---
*Enjoy contributing!*
