# Contributing

Thank you for considering contributing to GroveWatcher! We appreciate your help in making this project better.

## Code of Conduct

Please note that this project is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How to Contribute

### Setting Up Your Development Environment

1. **Fork the Repository**:
   ```bash
   git clone https://github.com/ukw2d/py-grove-watcher.git
   cd py-grove-watcher

2. It's recommended to use a virtual environment to avoid conflicts with other projects.
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install .
3. Create new branch:
    ```bash
    git checkout -b feature-branch-name
4. Implement your changes within the `src/grove_watcher` directory. Ensure all tests pass before committing.
5. Write clear and descriptive commit messages:
    ```bash
    git add .
    git commit -m "Add <feature/functionality>."
6. Push to your fork:
   ```bash
   git push origin feature-branch-name
7. Create a Pull Request (PR) from your fork to the `main` repository.


## Reporting Bugs

If you find a bug, please report it by opening an issue on the [GitHub Issues](https://github.com/ukw2d/py-grove-watcher/issues) page. Be sure to include a detailed description of the bug, steps to reproduce it, and your environment details. This will help us understand and fix the issue more efficiently. Make sure that open an issue with the following details:
- A clear and descriptive title.
- A description of the expected behavior.
- A description of the actual behavior.
- Steps to reproduce the behavior.

## Suggesting Enhancements

If you have an idea for an enhancement, please open an issue on the [GitHub Issues](https://github.com/ukw2d/py-grove-watcher/issues) page. Be sure to include a detailed description of the enhancement, its benefits, and any potential drawbacks. This will help us understand and consider the enhancement more effectively. Make sure that open an issue with the following details:
- A clear and descriptive title.
- A description of the enhancement.
- A description of the benefits of the enhancement.
- A description of the possible drawbacks of the enhancement.

## Pull Request Process

**Ensure Quality:**
- Follow PEP 8 for Python code styling.
  - Use consistent naming conventions throughout the project.
  - Add docstrings to all functions and classes.
  - Ensure all tests in the tests directory pass.
  
**Write Meaningful Commit Messages:**
- Provide clear and concise commit messages that describe the changes made.
  
**Reference Related Issues:**
- In your pull request description, reference any related issues using the syntax #issue_number.
  
**Be Responsive:**
- Be patient and responsive to feedback during the review process.