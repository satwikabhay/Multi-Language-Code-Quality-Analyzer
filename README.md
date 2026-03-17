# Multi-Language Code Quality Analyzer

**ML-based code quality assessment system for Python, Java, C++, and C**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://code-quality-analyzer.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-Random%20Forest-00C853?style=for-the-badge)](https://scikit-learn.org/)

---

## Overview

An intelligent code quality prediction system that uses Machine Learning to automatically assess code quality across multiple programming languages. Built with Random Forest classification achieving **98.33% accuracy** on a dataset of 600 code samples.

**Live Application:** [code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

---

## Features

- **Multi-Language Support** - Analyzes Python, Java, C++, and C code files
- **GitHub Integration** - Analyze entire repositories with a single URL
- **Real-time Analysis** - Instant quality predictions with confidence scores
- **Visual Reports** - Interactive charts and detailed metrics
- **Code Recommendations** - Actionable suggestions for improvement
- **19 Quality Metrics** - Comprehensive feature analysis

---

## Live Demo

**Application URL:** [https://code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

### Quick Start:
1. Navigate to "Analyze GitHub Repo"
2. Enter repository URL (e.g., `https://github.com/psf/requests`)
3. Click "Analyze" to view results

---

## Model Performance

| Metric | Score |
|--------|-------|
| **Test Accuracy** | 98.33% |
| **Cross-Validation** | 94.67% ± 13.93% |
| **Training Samples** | 600 (balanced) |
| **Precision** | 98.3% |
| **Recall** | 98.3% |

**Model Architecture:** Random Forest Classifier (100 trees, max depth 15)

---

## Technology Stack

- **Machine Learning:** scikit-learn, Random Forest
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly
- **API Integration:** GitHub REST API

---

## Project Structure

```
Multi-Language-Code-Analyzer/
├── app.py                              # Streamlit web interface
├── multi_language_analyzer.py          # Core analysis engine
├── 0_generate_bad_code.py              # Bad code sample generator
├── 1_collect_multilang_data.py         # Data collection script
├── 2_extract_features_multilang.py     # Feature extraction
├── 3_train_multilang_model.py          # Model training
├── 4_test_multilang.py                 # File testing script
├── 5_github_analyzer_multilang.py      # GitHub integration
├── model_multilang/                    # Trained model files
├── data_multilang/                     # Training data
└── requirements.txt                    # Python dependencies
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer.git
   cd Multi-Language-Code-Quality-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the application**
   ```
   Open browser to: http://localhost:8501
   ```

---

## Methodology

### Feature Extraction

The system analyzes 19 code quality features:

**Basic Metrics:**
- Total lines, blank lines, comment lines
- Comment-to-code ratio
- Average and maximum line length

**Complexity Metrics:**
- Function and class count
- Maximum indentation depth
- Control flow structures

**Code Smell Detection:**
- Magic number usage
- Single-letter variable names
- Long functions (>50 lines)
- Missing documentation

### Machine Learning Pipeline

- **Algorithm:** Random Forest with 100 decision trees
- **Training Split:** 80% training, 20% testing
- **Validation:** 5-fold cross-validation
- **Feature Set:** 19 quantitative code metrics

### Language-Specific Analysis

- **Python:** PEP 8 compliance, docstring detection
- **Java:** Javadoc support, OOP structure analysis
- **C++:** Doxygen comments, STL usage patterns
- **C:** Function documentation, error handling

---

## Usage

### Web Interface

**Analyze GitHub Repository:**
1. Navigate to "Analyze GitHub Repo"
2. Enter repository URL
3. Click "Analyze"
4. Review quality score and recommendations

**Analyze Single File:**
1. Navigate to "Analyze File"
2. Upload code file
3. View detailed metrics

### Command Line Interface

```bash
# Test individual file
python 4_test_multilang.py path/to/file.py

# Analyze GitHub repository
python 5_github_analyzer_multilang.py https://github.com/user/repo
```

---

## Training Custom Models

### 1. Data Collection
```bash
# Clone repositories to cloned_repos/good/ and cloned_repos/bad/
python 1_collect_multilang_data.py
```

### 2. Feature Extraction
```bash
python 2_extract_features_multilang.py
```

### 3. Model Training
```bash
python 3_train_multilang_model.py
```

Trained model will be saved in `model_multilang/`

---

## Applications

- Code review automation
- Educational tool for software engineering courses
- Portfolio and repository quality assessment
- Refactoring prioritization
- Code quality tracking over time

---

## Limitations

- Static analysis only (does not execute code)
- GitHub API rate limits apply (50 files per repository)
- Trained primarily on C/C++ samples
- Binary and very large files are excluded

---

## Future Enhancements

- Support for additional languages (JavaScript, Go, Rust)
- CI/CD pipeline integration
- Historical quality tracking
- Custom rule configuration
- IDE extensions

---

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

**Satwik Abhay**

- GitHub: [@satwikabhay](https://github.com/satwikabhay)
- Project: [Multi-Language-Code-Quality-Analyzer](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer)
- Live Demo: [code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

---

## Acknowledgments

- scikit-learn for the machine learning framework
- Streamlit for the web application framework
- Plotly for interactive visualizations
- GitHub API for repository access

---

## References

1. Allamanis, M., et al. (2014). "Learning natural coding conventions." ACM SIGSOFT Foundations of Software Engineering
2. Breiman, L. (2001). "Random forests." Machine Learning, 45(1), 5-32
3. Fontana, F. A., et al. (2016). "Comparing machine learning techniques for code smell detection." Empirical Software Engineering

---

<div align="center">

**Star this repository if you found it helpful**

[Live Demo](https://code-quality-analyzer.streamlit.app) | [Report Bug](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer/issues) | [Request Feature](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer/issues)

</div>
