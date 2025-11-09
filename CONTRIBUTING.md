# Contributing to Eviden Insight Reporter

Thank you for considering contributing to the Eviden Insight Reporter (Created by Algorzen)! This document provides guidelines and instructions for contributing.

## 🎯 How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages/stack traces
- Sample data (if applicable)

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Describe the feature clearly
- Explain the use case
- Consider backward compatibility

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/rizzshi/DataSphere.git
   cd AiInsight
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style guidelines below
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Run on sample data
   python main.py data/sample_dataset.csv --verbose
   
   # Test Streamlit UI
   streamlit run streamlit_app.py
   ```

5. **Commit with clear messages**
   ```bash
   git add .
   git commit -m "Add feature: description of feature"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## 📝 Code Style Guidelines

### Python Style

We follow **PEP 8** with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces
- **Naming**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Documentation

Every module, class, and function should have docstrings:

```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description of function
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When something goes wrong
    """
    pass
```

### Comments

- Use comments for complex logic
- Keep comments up-to-date with code
- Avoid obvious comments

```python
# Good
# Calculate weighted average using exponential decay
result = calculate_weighted_avg(values, decay=0.95)

# Bad
# Set x to 5
x = 5
```

### Type Hints

Use type hints where appropriate:

```python
from typing import Dict, List, Optional

def process_data(df: pd.DataFrame, options: Optional[Dict] = None) -> List[str]:
    """Process data with optional configurations"""
    pass
```

## 🏗️ Project Structure

When adding new features, follow this structure:

```
src/
├── module_name.py       # Your new module
│   ├── Class definitions
│   ├── Helper functions
│   └── Convenience function
└── __init__.py          # Export public API
```

Each module should:
- Have a clear purpose
- Be < 500 lines
- Export a convenience function
- Have comprehensive docstrings

## 🧪 Testing

### Manual Testing

Before submitting PR:

1. **Test with sample data**
   ```bash
   python main.py data/sample_dataset.csv
   ```

2. **Test with your own data**
   ```bash
   python main.py path/to/your/data.csv
   ```

3. **Test Streamlit UI**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Test edge cases**
   - Empty datasets
   - Missing values
   - Very large datasets
   - Different file formats

### Future: Automated Tests

We plan to add pytest-based tests. Example structure:

```python
# tests/test_eda_engine.py
import pytest
from src.eda_engine import perform_eda

def test_perform_eda_basic():
    df = generate_test_dataframe()
    result = perform_eda(df)
    assert 'dataset_info' in result
    assert result['dataset_info']['rows'] > 0
```

## 📋 Checklist for Pull Requests

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Manual testing completed
- [ ] No breaking changes (or documented)
- [ ] README updated if needed
- [ ] No sensitive data in commits
- [ ] Commit messages are clear

## 🎨 Adding New Features

### Adding a New Dataset Type

1. Edit `src/eda_engine.py`:
   ```python
   def _detect_dataset_type(self) -> str:
       # Add your detection logic
       your_keywords = ['keyword1', 'keyword2']
       your_score = sum(any(kw in col for kw in your_keywords) 
                       for col in cols_lower)
   ```

2. Edit `src/kpi_extractor.py`:
   ```python
   def extract_your_kpis(self) -> Dict:
       """Extract KPIs for your dataset type"""
       kpis = {}
       # Your KPI logic
       return kpis
   ```

3. Update fallback narrative in `src/ai_narrator.py`

### Adding New Visualizations

1. Add method to `EDAEngine` class:
   ```python
   def generate_your_plot(self) -> str:
       """Generate your custom plot"""
       plt.figure(figsize=(10, 6))
       # Your plotting logic
       output_path = self.output_dir / "your_plot.png"
       plt.savefig(output_path, dpi=300, bbox_inches='tight')
       plt.close()
       return str(output_path)
   ```

2. Call it in `run_full_eda()`:
   ```python
   'your_plot': self.generate_your_plot()
   ```

3. Add to PDF in `src/pdf_generator.py`

## 🌟 Areas for Contribution

We especially welcome contributions in:

### High Priority
- [ ] Unit tests with pytest
- [ ] More dataset type detectors
- [ ] Additional KPI extractors
- [ ] Custom visualization templates
- [ ] Performance optimizations

### Medium Priority
- [ ] Database connectors (PostgreSQL, MySQL)
- [ ] API data source support
- [ ] Email report delivery
- [ ] Dashboard mode
- [ ] Multi-language support

### Nice to Have
- [ ] Custom branding templates
- [ ] Advanced statistical tests
- [ ] Time series forecasting
- [ ] Anomaly detection
- [ ] Interactive charts

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help newcomers
- Focus on the code, not the person

### Communication

- Use GitHub Issues for bugs/features
- Use GitHub Discussions for questions
- Tag issues appropriately
- Be patient with maintainers

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📞 Questions?

If you have questions about contributing:
- Open a GitHub Discussion
- Review existing PRs for examples
- Check the documentation

## 🎉 Thank You!

Every contribution, no matter how small, helps make Eviden Insight Reporter better!

---

**Built with ❤️ by the Algorzen Community**

© 2025 Algorzen | Rishi Singh
