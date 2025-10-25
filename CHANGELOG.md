# Changelog

## [1.0.0] - 2025-10-25
### Added
- First stable release of **Mailbrig** 🎉
- Unified interface for multiple email providers:
  - **SMTP**
  - **SendGrid**
  - **Mailgun**
  - **Brevo (Sendinblue)**
  - **Amazon SES**
- Centralized API for sending emails with automatic provider selection
- CLI tool (`mailbrig`) for quick provider testing and configuration
- Environment-based configuration via `.env` file or system variables
- Easy extension with custom providers through abstract `ProviderInterface`
- Full test coverage with validation of provider responses
- Comprehensive documentation and usage examples

### Changed
- Project structure migrated to `pyproject.toml` (PEP 621)  
- Published initial version `0.1.0` to [PyPI](https://pypi.org/project/mailbridge) before stable 1.0.0

### Notes
- This marks the **first production-ready stable release**
- Future changes will follow [Semantic Versioning](https://semver.org/)
- Backward compatibility will be maintained across all `1.x.x` versions
