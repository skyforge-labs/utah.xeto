# Contributing to Utah Xeto Libraries

Thank you for your interest in contributing to the Utah Xeto Libraries! These libraries implement the State of Utah DFCM Haystack tagging standards.

## Development Setup

1. **Prerequisites**
   - Familiarity with [Xeto](https://github.com/Project-Haystack/xeto) data modeling language
   - Understanding of [Project Haystack](https://project-haystack.org/) standards
   - Knowledge of Utah DFCM building automation standards
   - [Haxall](https://github.com/haxall/haxall) runtime for testing libraries

2. **Getting Started**
   - Clone the repository
   - Install [Haxall](https://github.com/haxall/haxall) for local development
   - Review the [README.md](README.md) for library overview
   - Check existing issues for contribution opportunities

3. **Development Tools**
   - Use `xeto build` to compile and validate your libraries
   - Use `xeto repo` to list available libraries
   - Test your changes by installing libraries in a Haxall project

## Contribution Guidelines

### Code Style
- **Composition first**: Build types by composing lower-level specs from `ph.*`, `utah`, and `utah.points` rather than redefining semantics
- **Consistent naming**: Utah-specific types prefixed with `Utah` (e.g., `UtahAhu`, `UtahChWFlow`)
- **Stable conventions**: Use consistent `navName`, units, precision, and history settings

### Library Structure
Each Utah library should include:
- Clear type definitions with comprehensive documentation
- README.md explaining the library's purpose and major types
- Consistent naming and history conventions

### Pull Request Process

1. **Fork** the repository
2. **Create a feature branch** from `main`
3. **Make your changes** following the guidelines above
4. **Update documentation** if adding new types or libraries
5. **Test your changes** (currently manual validation)
6. **Submit a pull request** with a clear description

### Types of Contributions
- **New equipment types**: Following Utah DFCM standards
- **Point definitions**: Utah-standard point types with proper metadata
- **Documentation improvements**: README updates, type documentation
- **Bug fixes**: Corrections to existing type definitions

## Code Review
All submissions require review. Reviewers will check for:
- Compliance with Utah DFCM standards
- Consistent naming and conventions
- Proper type composition
- Documentation completeness

## Questions?
- Open an [issue](https://github.com/skyforge-labs/utah.xeto/issues) for questions
- Check existing documentation and issues first

Thank you for helping build Utah's building automation standards!
