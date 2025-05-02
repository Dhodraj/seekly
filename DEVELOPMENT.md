# Seekly Development Guide

This guide covers the development process for Seekly CLI, including version management and publishing releases.

## Environment Setup

Create a development environment that works with your preferred setup:

```bash
# Clone the repository (any method that works for you)
git clone https://github.com/Dhodraj/seekly.git
cd seekly

# Set up your preferred environment
python -m venv venv  # or conda create -n seekly python=3.8
source venv/bin/activate  # or conda activate seekly

# Install development dependencies
pip install -e .
pip install build twine pytest
```

## Testing Changes

Run tests to ensure your changes maintain compatibility across different environments:

```bash
# Run the test suite
python -m unittest discover seekly/tests

# Test the CLI locally
python seekly.py search "test query" --dir ./seekly/tests/test_files
```

## Version Management

Seekly uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

## Publishing to PyPI

### Automated Publishing (Preferred)

The GitHub Actions workflow automatically handles publishing when a new release is created:

1. Update the version in `setup.py`
2. Commit and push your changes
3. Create a new GitHub release
4. The workflow will build and publish to PyPI

### Manual Publishing with API Token (Recommended)

To manually publish using an API token (the modern, secure method):

1. Update the version in `setup.py` to your target version (e.g., "1.1.2")

2. Generate a PyPI API token:
   - Log in to [PyPI](https://pypi.org/)
   - Go to Account Settings → API tokens
   - Create a scoped token for the 'seekly' project

3. Build the distribution packages:
   ```bash
   # Clean previous builds
   rm -rf build/ dist/ *.egg-info/
   
   # Build source and wheel distributions
   python -m build
   ```

4. Verify the built packages:
   ```bash
   twine check dist/*
   ```

5. Upload using your API token:
   ```bash
   # Use environment variable for token (more secure)
   export TWINE_PASSWORD=your_api_token
   export TWINE_USERNAME=__token__
   
   # Upload to PyPI
   twine upload dist/*
   
   # OR upload directly with command line arguments
   twine upload -u __token__ -p your_api_token dist/*
   ```

6. Tag the release in git:
   ```bash
   git tag -a v1.1.2 -m "Version 1.1.2"
   git push origin v1.1.2
   ```

### Testing on TestPyPI

Before publishing to the main PyPI, you can test on TestPyPI:

```bash
# Register on https://test.pypi.org if you haven't already
# Upload to TestPyPI
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ seekly
```

## Updating the pipx_install.py Script

The `pipx_install.py` script should be updated to install from PyPI by default when a stable version exists:

1. Open `pipx_install.py`
2. Update the `get_package_source()` function to prefer PyPI over GitHub when appropriate

## Best Practices

- **Version Control**: Never modify published versions - always create a new version
- **Documentation**: Update documentation to reflect any changes
- **Testing**: Ensure tests pass across different Python versions and platforms
- **Semantic Versioning**: Follow semantic versioning principles consistently
- **Release Notes**: Write clear, user-oriented release notes

## Troubleshooting Publication Issues

If you encounter errors during the publication process:

- **Authentication Errors**: Ensure you're using an API token with `__token__` as the username
- **Version Conflicts**: Verify the version in `setup.py` hasn't been published already
- **Distribution Issues**: Check `twine check dist/*` for warnings or errors
- **Package Structure**: Validate your package structure with `pip install -e .`

Remember that PyPI doesn't allow overwriting existing versions. Always increment the version number when publishing changes.