# Contributing to Hyperliquid Dashboard

Thank you for your interest in contributing to the Hyperliquid Dashboard! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues**: Before creating a new issue, search the existing issues to see if the bug has already been reported.
2. **Create a detailed bug report**: Include:
   - Clear and descriptive title
   - Steps to reproduce the issue
   - Expected behavior
   - Actual behavior
   - Environment details (OS, browser, Python/Node versions)
   - Screenshots if applicable

### Suggesting Enhancements

1. **Check existing feature requests**: Search existing issues to see if your enhancement has already been suggested.
2. **Create a feature request**: Include:
   - Clear description of the feature
   - Use cases and benefits
   - Mockups or examples if applicable

### Code Contributions

#### Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- Basic knowledge of FastAPI and React

#### Development Setup

1. **Fork the repository**
2. **Clone your fork**:
   ```bash
   git clone https://github.com/yourusername/hyperliquid-dashboard.git
   cd hyperliquid-dashboard
   ```

3. **Set up the backend**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Set up the frontend**:
   ```bash
   cd ../frontend
   npm install
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Coding Standards

##### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings for functions and classes
- Keep functions small and focused
- Use meaningful variable and function names

##### JavaScript/React (Frontend)
- Follow ESLint configuration
- Use functional components with hooks
- Follow React best practices
- Use meaningful component and variable names
- Add PropTypes or TypeScript types where applicable

#### Testing

- Write tests for new functionality
- Ensure all existing tests pass
- Test both backend API endpoints and frontend components

#### Commit Guidelines

Use conventional commit messages:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(backend): add new API endpoint for user positions
fix(frontend): resolve chart rendering issue
docs: update README with new setup instructions
```

#### Pull Request Process

1. **Ensure your code follows the project's coding standards**
2. **Add tests for new functionality**
3. **Update documentation if needed**
4. **Make sure all tests pass**
5. **Create a pull request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots for UI changes
   - Test results

6. **Wait for review**: Maintainers will review your PR and provide feedback

### Review Process

- All contributions require review before merging
- Maintainers may request changes
- Once approved, your PR will be merged

## 🏗️ Project Structure

### Backend (`/backend`)
- `main.py`: Main FastAPI application
- `main2.py`: Additional backend functionality
- `requirements.txt`: Python dependencies

### Frontend (`/frontend`)
- `src/`: React source code
- `public/`: Static assets
- `package.json`: Node.js dependencies and scripts

## 🐛 Common Issues

### Backend Issues
- **Import errors**: Ensure all dependencies are installed
- **WebSocket connection issues**: Check CORS configuration
- **API rate limits**: Implement proper rate limiting

### Frontend Issues
- **Build errors**: Clear node_modules and reinstall
- **Chart rendering**: Check Chart.js configuration
- **Styling issues**: Verify Tailwind CSS setup

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check the README and code comments

## 🎯 Areas for Contribution

- **Performance improvements**: Optimize API responses and frontend rendering
- **New features**: Additional chart types, trading tools, etc.
- **Documentation**: Improve README, add API documentation
- **Testing**: Add unit and integration tests
- **UI/UX**: Improve user interface and experience
- **Security**: Security audits and improvements

## 📝 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

Thank you for contributing to the Hyperliquid Dashboard! 🚀 