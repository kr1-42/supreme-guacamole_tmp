# Changelog

All notable changes to the Art Catalog Manager project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced README.md with professional formatting and comprehensive documentation
- MIT License for open-source distribution
- Contributing guidelines (CONTRIBUTING.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- Changelog (CHANGELOG.md) for tracking project history

### Changed
- Improved project presentation and documentation structure
- Enhanced web application documentation (webapp.md)

## [1.0.0] - 2024-01-31

### Added
- Desktop application with PyQt5 interface
- Web application with Flask interface
- Artist management system
- Artwork catalog with image support
- Exhibition planning and tracking
- Sales tracking and payment calculations
- Live database viewer with Datasette
- QR code generation for mobile access
- Dark theme for desktop application
- SQLite database backend
- Automatic database backup system
- Image gallery with preview functionality

### Features
- **Artist Management**
  - Add, edit, and delete artist profiles
  - Track contact information and biography
  - Store notes and additional details

- **Artwork Catalog**
  - Comprehensive artwork tracking
  - High-resolution image support
  - Pricing and status management
  - Category and medium classification

- **Exhibition Management**
  - Create and manage exhibitions
  - Associate artworks with exhibitions
  - Track exhibition dates and locations

- **Sales Tracking**
  - Record sales transactions
  - Automatic payment split calculations
  - Sales history and reporting

- **Database Features**
  - SQLite database for reliability
  - Automatic backup system
  - Live database viewer via Datasette
  - QR code sharing for mobile access

### Technical
- Python 3.8+ support
- Cross-platform compatibility (Windows, macOS, Linux)
- Virtual environment setup
- Comprehensive dependency management

## Version History

### Version Numbering
We use [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes

### Release Notes

For detailed release notes and upgrade instructions, please see individual version tags in the repository.

---

## How to Contribute to This Changelog

When contributing to the project, please update this changelog following these guidelines:

1. **Add new entries under the `[Unreleased]` section**
2. **Use the following categories:**
   - `Added` for new features
   - `Changed` for changes in existing functionality
   - `Deprecated` for soon-to-be removed features
   - `Removed` for now removed features
   - `Fixed` for any bug fixes
   - `Security` for security-related changes

3. **Write clear, concise descriptions**
4. **Reference issue/PR numbers when applicable**

### Example Entry Format:
```markdown
### Added
- New feature for exporting artist data to CSV format (#42)
- Support for bulk artwork import via JSON files (#45)

### Fixed
- Resolved issue with image preview on high-DPI displays (#38)
- Fixed database connection leak in web application (#40)
```

---

[Unreleased]: https://github.com/kr1-42/supreme-guacamole_tmp/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/kr1-42/supreme-guacamole_tmp/releases/tag/v1.0.0
