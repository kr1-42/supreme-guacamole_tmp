# Contributing to Art Catalog Manager

First off, thank you for considering contributing to Art Catalog Manager! It's people like you that make this tool better for everyone.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Style Guidelines](#style-guidelines)
  - [Git Commit Messages](#git-commit-messages)
  - [Python Style Guide](#python-style-guide)
- [Project Structure](#project-structure)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Environment:**
 - OS: [e.g., Windows 10, Ubuntu 20.04]
 - Python Version: [e.g., 3.9.5]
 - Application Version: [e.g., 1.0.0]

**Additional context**
Add any other context about the problem here.
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Use a clear and descriptive title**
- **Provide a detailed description** of the suggested enhancement
- **Explain why this enhancement would be useful** to most users
- **List any similar features** in other applications (if applicable)

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following our style guidelines
3. **Test your changes** thoroughly
4. **Update documentation** if you're adding or modifying features
5. **Write clear commit messages** following our guidelines
6. **Submit a pull request** with a comprehensive description

**Pull Request Template:**

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] I have tested these changes locally
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
```

## Development Setup

1. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/supreme-guacamole_tmp.git
   cd supreme-guacamole_tmp
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make your changes and test:**
   ```bash
   python main.py  # Test desktop app
   python webapp/app.py  # Test web app
   ```

## Style Guidelines

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

**Examples:**
```
Add artist profile export feature

- Implement CSV export functionality
- Add export button to artist list
- Update documentation

Fixes #123
```

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length of 88 characters (following Black formatter defaults)
- Use descriptive variable names
- Add docstrings to all functions and classes
- Keep functions focused and single-purpose

**Example:**

```python
def calculate_artist_payment(sale_amount: float, commission_rate: float) -> float:
    """
    Calculate the payment amount for an artist after commission.
    
    Args:
        sale_amount: The total sale price of the artwork
        commission_rate: The commission percentage (0-100)
    
    Returns:
        The payment amount due to the artist
    
    Raises:
        ValueError: If commission_rate is not between 0 and 100
    """
    if not 0 <= commission_rate <= 100:
        raise ValueError("Commission rate must be between 0 and 100")
    
    commission = sale_amount * (commission_rate / 100)
    return sale_amount - commission
```

### Code Organization

- **Import Order:**
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
  
  Separate each group with a blank line.

- **File Organization:**
  1. Module docstring
  2. Imports
  3. Constants
  4. Classes
  5. Functions
  6. Main execution block (if applicable)

## Project Structure

Understanding the project structure will help you navigate the codebase:

```
art-catalog-manager/
├── core/                 # Business logic and data access
│   ├── database.py       # Database operations
│   ├── schema.py         # Database schema
│   └── repositories/     # Data repositories
├── ui/                   # Desktop interface (PyQt5)
│   ├── main_window.py    # Main window
│   ├── dialogs/          # Dialog windows
│   └── widgets/          # Custom widgets
├── webapp/               # Web interface (Flask)
│   ├── app.py            # Flask application
│   ├── templates/        # HTML templates
│   └── static/           # CSS/JS assets
└── scripts/              # Utility scripts
```

### Key Components

- **Database Layer** (`core/database.py`, `core/repositories/`): Handles all database operations
- **UI Layer** (`ui/`): Desktop interface components
- **Web Layer** (`webapp/`): Web interface components
- **Schema** (`core/schema.py`): Database table definitions

## Questions?

Feel free to open an issue with your question or reach out to the maintainers directly.

---

Thank you for contributing to Art Catalog Manager! 🎨
