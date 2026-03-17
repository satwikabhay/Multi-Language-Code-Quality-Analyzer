# Multi-Language Code Quality Analyzer

**ML-based code quality assessment system for Python, Java, C++, and C**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://code-quality-analyzer.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ML](https://img.shields.io/badge/ML-Random%20Forest-00C853?style=for-the-badge)](https://scikit-learn.org/)

---

## 🎯 Overview

An intelligent code quality prediction system that uses **Machine Learning** to automatically assess code quality across multiple programming languages. Built with Random Forest classification achieving **98.33% accuracy** on a dataset of 600 code samples.

**🌐 Try it live:** [code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

---

## ✨ Features

- **Multi-Language Support** - Analyzes Python, Java, C++, and C code files
- **GitHub Integration** - Analyze entire repositories with a single URL
- **Real-time Analysis** - Instant quality predictions with confidence scores
- **Visual Reports** - Interactive charts and detailed metrics
- **Code Recommendations** - Actionable suggestions for improvement
- **19 Quality Metrics** - Comprehensive feature analysis including:
  - Code complexity and structure
  - Documentation coverage
  - Code smells detection
  - Function length analysis

---

## 🚀 Live Demo

**Try the analyzer now:** [https://code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

### Quick Test:
1. Go to "Analyze GitHub Repo"
2. Paste any public repository URL (e.g., `https://github.com/psf/requests`)
3. Click "Analyze" and get instant results!

---

## 📊 Model Performance

| Metric | Score |
|--------|-------|
| **Test Accuracy** | 98.33% |
| **Cross-Validation** | 94.67% ± 13.93% |
| **Training Samples** | 600 (balanced) |
| **Precision** | 98.3% |
| **Recall** | 98.3% |

**Model:** Random Forest Classifier (100 trees, max depth 15)

---

## 🛠️ Tech Stack

- **Machine Learning:** scikit-learn, Random Forest
- **Web Interface:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualizations:** Plotly
- **API Integration:** GitHub REST API

---

## 📁 Project Structure

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
└── requirements.txt                    # Dependencies
```

---

## 💻 Local Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer.git
   cd Multi-Language-Code-Quality-Analyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the web app**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser**
   ```
   http://localhost:8501
   ```

---

## 🎓 How It Works

### 1. Feature Extraction
The system analyzes **19 code quality features**:

**Basic Metrics:**
- Total lines, blank lines, comment lines
- Comment ratio, average line length

**Complexity:**
- Function/class count
- Maximum indentation depth
- Control flow structures (if/else, loops)

**Code Smells:**
- Magic numbers
- Single-letter variables
- Very long functions (>50 lines)
- Missing documentation

### 2. Machine Learning
- **Algorithm:** Random Forest with 100 decision trees
- **Training:** 80/20 train-test split
- **Validation:** 5-fold cross-validation
- **Features:** 19 quantitative metrics

### 3. Language Support
Each language has customized analysis:
- **Python:** PEP 8 compliance, docstring detection
- **Java:** Javadoc support, OOP structure analysis
- **C++:** Doxygen comments, STL usage patterns
- **C:** Function documentation, error handling

---

## 📈 Usage Examples

### Analyze a GitHub Repository

```python
# Through the web interface:
1. Navigate to "Analyze GitHub Repo"
2. Enter: https://github.com/username/repository
3. Click "Analyze"
4. View results with quality score, charts, and recommendations
```

### Analyze a Single File

```python
# Through the web interface:
1. Navigate to "Analyze File"
2. Upload your code file (.py, .java, .cpp, .c)
3. View detailed metrics and suggestions
```

### Command Line Usage

```bash
# Test a single file
python 4_test_multilang.py path/to/your/file.py

# Analyze a GitHub repository
python 5_github_analyzer_multilang.py https://github.com/user/repo
```

---

## 🔬 Training Your Own Model

### 1. Collect Data
```bash
# Clone good quality repositories to cloned_repos/good/
# Clone poor quality repositories to cloned_repos/bad/
python 1_collect_multilang_data.py
```

### 2. Extract Features
```bash
python 2_extract_features_multilang.py
```

### 3. Train Model
```bash
python 3_train_multilang_model.py
```

The trained model will be saved in `model_multilang/`

---

## 🎯 Use Cases

- **Code Review Automation** - Pre-screen pull requests
- **Educational Tool** - Help students learn code quality
- **Portfolio Analysis** - Assess repository quality
- **Refactoring Priority** - Identify files needing improvement
- **Quality Metrics** - Track code quality over time

---

## 🚧 Limitations

- Limited to static analysis (doesn't execute code)
- Trained on 600 samples (primarily C/C++ heavy)
- GitHub API rate limits (50 files per repository)
- Binary files and very large files are skipped

---

## 🔮 Future Enhancements

- [ ] Support for more languages (JavaScript, Go, Rust)
- [ ] Real-time collaboration features
- [ ] Integration with CI/CD pipelines
- [ ] Historical quality tracking
- [ ] Custom quality rules configuration
- [ ] VS Code extension

---

## 🤝 Contributing

Contributions are welcome! This is an educational project, but suggestions and improvements are appreciated.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add some improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Satwik Abhay**

- GitHub: [@satwikabhay](https://github.com/satwikabhay)
- Project Link: [Multi-Language-Code-Quality-Analyzer](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer)
- Live Demo: [code-quality-analyzer.streamlit.app](https://code-quality-analyzer.streamlit.app)

---

## 🙏 Acknowledgments

- **scikit-learn** - Machine learning framework
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **GitHub API** - Repository access

---

## 📚 References

1. Allamanis, M., et al. (2014). "Learning natural coding conventions." *ACM SIGSOFT FSE*
2. Breiman, L. (2001). "Random forests." *Machine Learning, 45(1), 5-32*
3. Fontana, F. A., et al. (2016). "Comparing machine learning techniques for code smell detection." *Empirical Software Engineering*

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

Built with ❤️ using Machine Learning

[Live Demo](https://code-quality-analyzer.streamlit.app) • [Report Bug](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer/issues) • [Request Feature](https://github.com/satwikabhay/Multi-Language-Code-Quality-Analyzer/issues)

</div>
