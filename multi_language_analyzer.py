"""
Multi-Language Code Quality Analyzer
Supports: Python, Java, C++, C

This module analyzes source code files and extracts 19 quality features
regardless of programming language. It adapts its analysis based on the
file extension and language-specific syntax.
"""

import os
import re
from pathlib import Path


class MultiLanguageAnalyzer:
    """
    Analyzes code quality across multiple programming languages.
    
    Features extracted:
    - Basic metrics: line counts, lengths
    - Documentation: comments, docstrings
    - Complexity: functions, classes, indentation
    - Control flow: if/else, loops, error handling
    - Code smells: magic numbers, poor naming
    """
    
    def __init__(self, filepath):
        """
        Initialize analyzer for a code file.
        
        Args:
            filepath (str): Path to the code file to analyze
        """
        self.filepath = filepath
        self.lines = []
        self.code_lines = []
        self.language = self.detect_language()
        self.load_file()
    
    def detect_language(self):
        """
        Detect programming language from file extension.
        
        Returns:
            str: Language name ('python', 'java', 'cpp', 'c', or 'unknown')
        """
        ext = Path(self.filepath).suffix.lower()
        
        language_map = {
            '.py': 'python',
            '.java': 'java',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.hpp': 'cpp',
            '.h': 'c',      # Could be C or C++, we treat as C
            '.c': 'c'
        }
        
        return language_map.get(ext, 'unknown')
    
    def load_file(self):
        """
        Read file contents into memory.
        
        Stores both all lines (including blank) and code lines (non-blank).
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8', errors='ignore') as f:
                self.lines = f.readlines()
            # Code lines = lines that aren't empty
            self.code_lines = [line for line in self.lines if line.strip()]
        except Exception as e:
            print(f"Warning: Could not read {self.filepath}: {e}")
            self.lines = []
            self.code_lines = []
    
    # ==================== BASIC METRICS ====================
    
    def count_lines(self):
        """Total lines in file (including blank lines)"""
        return len(self.lines)
    
    def count_blank_lines(self):
        """Count of blank/empty lines"""
        return sum(1 for line in self.lines if not line.strip())
    
    # ==================== COMMENT ANALYSIS ====================
    
    def count_comment_lines(self):
        """
        Count comment lines (language-specific).
        
        Python: # and triple-quotes
        Java/C++/C: // and /* */
        """
        if self.language == 'python':
            return self._count_python_comments()
        elif self.language in ['java', 'cpp', 'c']:
            return self._count_c_style_comments()
        return 0
    
    def _count_python_comments(self):
        """Count Python comments (# and docstrings)"""
        count = 0
        in_multiline = False
        
        for line in self.lines:
            stripped = line.strip()
            
            # Check for docstring markers
            if '"""' in stripped or "'''" in stripped:
                in_multiline = not in_multiline
                count += 1
            elif in_multiline:
                count += 1
            elif stripped.startswith('#'):
                count += 1
        
        return count
    
    def _count_c_style_comments(self):
        """Count C-style comments (// and /* */)"""
        count = 0
        in_multiline = False
        
        for line in self.lines:
            stripped = line.strip()
            
            # Multi-line comment start/end
            if '/*' in stripped:
                in_multiline = True
                count += 1
            elif '*/' in stripped:
                in_multiline = False
                count += 1
            elif in_multiline:
                count += 1
            elif stripped.startswith('//'):
                count += 1
        
        return count
    
    def comment_ratio(self):
        """Percentage of lines that are comments"""
        total = self.count_lines()
        return self.count_comment_lines() / total if total > 0 else 0
    
    # ==================== LINE LENGTH METRICS ====================
    
    def avg_line_length(self):
        """Average characters per line (excluding blank lines)"""
        if not self.code_lines:
            return 0
        return sum(len(line) for line in self.code_lines) / len(self.code_lines)
    
    def max_line_length(self):
        """Length of the longest line"""
        return max((len(line) for line in self.code_lines), default=0)
    
    def count_long_lines(self):
        """
        Count lines exceeding recommended length.
        
        Python/Java: 80 characters
        C/C++: 100 characters
        """
        max_length = 100 if self.language in ['c', 'cpp'] else 80
        return sum(1 for line in self.code_lines if len(line) > max_length)
    
    # ==================== INDENTATION/COMPLEXITY ====================
    
    def max_indentation_depth(self):
        """
        Maximum nesting level in the code.
        
        Python: 4 spaces per level
        Java/C++/C: 2-4 spaces per level (we use 4)
        """
        max_depth = 0
        indent_size = 4  # Spaces per indentation level
        
        for line in self.code_lines:
            if line.strip():
                leading_spaces = len(line) - len(line.lstrip())
                depth = leading_spaces // indent_size
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    # ==================== FUNCTION/CLASS COUNTING ====================
    
    def count_functions(self):
        """
        Count function definitions (language-specific).
        
        Python: def function_name(
        Java: public/private/protected returnType functionName(
        C++: returnType functionName(
        C: returnType functionName(
        """
        if self.language == 'python':
            return sum(1 for line in self.code_lines if line.strip().startswith('def '))
        
        elif self.language == 'java':
            # Java methods have modifiers: public void methodName(
            count = 0
            for line in self.code_lines:
                stripped = line.strip()
                # Look for method signatures (simplified)
                if ('(' in stripped and ')' in stripped and 
                    any(mod in stripped for mod in ['public', 'private', 'protected', 'static', 'void', 'int', 'String'])):
                    if not stripped.startswith('//') and not stripped.startswith('if') and not stripped.startswith('for'):
                        count += 1
            return count
        
        elif self.language in ['c', 'cpp']:
            # C/C++ functions: returnType functionName(
            count = 0
            for line in self.code_lines:
                stripped = line.strip()
                # Basic pattern: has parentheses, not a control structure
                if ('(' in stripped and ')' in stripped and 
                    not stripped.startswith('//') and
                    not any(keyword in stripped for keyword in ['if', 'for', 'while', 'switch'])):
                    count += 1
            return count
        
        return 0
    
    def count_classes(self):
        """
        Count class/struct definitions.
        
        Python: class ClassName:
        Java: class ClassName {
        C++: class ClassName {
        C: struct StructName {
        """
        if self.language in ['python', 'java']:
            return sum(1 for line in self.code_lines if line.strip().startswith('class '))
        
        elif self.language == 'cpp':
            count = 0
            for line in self.code_lines:
                stripped = line.strip()
                if stripped.startswith('class ') or stripped.startswith('struct '):
                    count += 1
            return count
        
        elif self.language == 'c':
            # C doesn't have classes, count structs
            return sum(1 for line in self.code_lines if line.strip().startswith('struct '))
        
        return 0
    
    # ==================== CONTROL FLOW ====================
    
    def count_control_structures(self):
        """Count if/else statements"""
        count = 0
        
        for line in self.code_lines:
            stripped = line.strip()
            
            if self.language == 'python':
                if (stripped.startswith('if ') or 
                    stripped.startswith('elif ') or 
                    stripped.startswith('else:')):
                    count += 1
            
            else:  # Java, C, C++
                if ('if (' in stripped or 
                    'else if' in stripped or 
                    stripped.startswith('else')):
                    count += 1
        
        return count
    
    def count_loops(self):
        """Count for/while loops"""
        count = 0
        
        for line in self.code_lines:
            stripped = line.strip()
            
            if self.language == 'python':
                if stripped.startswith(('for ', 'while ')):
                    count += 1
            
            elif self.language == 'java':
                # Java has for, while, and enhanced for
                if ('for (' in stripped or 
                    'while (' in stripped or
                    'for(' in stripped):
                    count += 1
            
            else:  # C, C++
                if ('for (' in stripped or 'while (' in stripped):
                    count += 1
        
        return count
    
    def count_try_except(self):
        """
        Count error handling blocks.
        
        Python: try/except
        Java: try/catch
        C++: try/catch
        C: (no built-in exception handling)
        """
        count = 0
        
        for line in self.code_lines:
            stripped = line.strip()
            
            if self.language == 'python':
                if stripped.startswith('try:'):
                    count += 1
            
            elif self.language in ['java', 'cpp']:
                if stripped.startswith('try') or 'try {' in stripped:
                    count += 1
            
            # C doesn't have try/catch
        
        return count
    
    # ==================== DOCUMENTATION ====================
    
    def has_docstrings(self):
        """
        Check if file has documentation strings.
        
        Python: triple quotes
        Java: Javadoc (/** */)
        C++/C: Doxygen (/** */ or ///)
        
        Returns:
            int: 1 if has documentation, 0 otherwise
        """
        content = ''.join(self.lines)
        
        if self.language == 'python':
            return 1 if ('"""' in content or "'''" in content) else 0
        
        elif self.language in ['java', 'cpp', 'c']:
            # Javadoc/Doxygen comments
            return 1 if ('/**' in content or '///' in content) else 0
        
        return 0
    
    # ==================== CODE SMELLS ====================
    
    def count_single_letter_vars(self):
        """
        Count single-letter variable names (excluding common loop counters).
        
        Python: x = 5
        Java: int x = 5;
        C/C++: int x = 5;
        """
        count = 0
        
        if self.language == 'python':
            pattern = r'^[a-z]\s*='
            for line in self.code_lines:
                if re.search(pattern, line.strip()):
                    # Exclude common loop counters
                    if not re.search(r'for\s+[ijk]\s+in', line):
                        count += 1
        
        elif self.language == 'java':
            # Pattern: type x = ...
            pattern = r'\b(int|long|double|float|char|String)\s+[a-z]\s*='
            for line in self.code_lines:
                if re.search(pattern, line):
                    count += 1
        
        elif self.language in ['c', 'cpp']:
            pattern = r'\b(int|char|float|double|long|short)\s+[a-z]\s*='
            for line in self.code_lines:
                if re.search(pattern, line):
                    count += 1
        
        return count
    
    def count_magic_numbers(self):
        """
        Count hardcoded numbers (2+ digits, excluding 0, 1, -1).
        
        Example: if (x > 100) has one magic number
        """
        pattern = r'\b\d{2,}\b'  # Match 2+ digit numbers
        count = 0
        
        for line in self.code_lines:
            stripped = line.strip()
            
            # Skip comment lines
            is_comment = (
                stripped.startswith('#') or 
                stripped.startswith('//') or
                stripped.startswith('*')
            )
            
            if not is_comment:
                matches = re.findall(pattern, line)
                count += len(matches)
        
        return count
    
    # ==================== FUNCTION LENGTH ANALYSIS ====================
    
    def function_lengths(self):
        """
        Calculate lengths of all functions in the file.
        
        Returns:
            list: List of function lengths in lines
        """
        lengths = []
        current_func_lines = 0
        in_function = False
        brace_count = 0
        
        for line in self.code_lines:
            stripped = line.strip()
            
            if self.language == 'python':
                # Python uses indentation
                if stripped.startswith('def '):
                    if in_function and current_func_lines > 0:
                        lengths.append(current_func_lines)
                    in_function = True
                    current_func_lines = 0
                elif in_function:
                    if stripped and not stripped.startswith(('def ', 'class ')):
                        current_func_lines += 1
                    elif stripped.startswith(('def ', 'class ')):
                        lengths.append(current_func_lines)
                        current_func_lines = 0
                        in_function = stripped.startswith('def ')
            
            else:
                # Java/C/C++ use braces
                if '{' in line:
                    brace_count += line.count('{')
                    if not in_function and brace_count > 0:
                        in_function = True
                        current_func_lines = 0
                
                if in_function:
                    current_func_lines += 1
                
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0 and in_function:
                        lengths.append(current_func_lines)
                        in_function = False
                        current_func_lines = 0
        
        # Don't forget last function
        if in_function and current_func_lines > 0:
            lengths.append(current_func_lines)
        
        return lengths
    
    def avg_function_length(self):
        """Average lines per function"""
        lengths = self.function_lengths()
        return sum(lengths) / len(lengths) if lengths else 0
    
    def max_function_length(self):
        """Length of longest function"""
        lengths = self.function_lengths()
        return max(lengths) if lengths else 0
    
    def count_very_long_functions(self):
        """Count functions longer than 50 lines"""
        return sum(1 for length in self.function_lengths() if length > 50)
    
    # ==================== EXTRACT ALL FEATURES ====================
    
    def extract_all_features(self):
        """
        Extract all 19 features from the code file.
        
        Returns:
            dict: Dictionary containing all features
        """
        return {
            # File info
            'file_name': os.path.basename(self.filepath),
            'language': self.language,
            
            # Basic metrics (4 features)
            'total_lines': self.count_lines(),
            'blank_lines': self.count_blank_lines(),
            'comment_lines': self.count_comment_lines(),
            'comment_ratio': self.comment_ratio(),
            
            # Line length (3 features)
            'avg_line_length': self.avg_line_length(),
            'max_line_length': self.max_line_length(),
            'long_lines_count': self.count_long_lines(),
            
            # Structure (3 features)
            'max_indentation': self.max_indentation_depth(),
            'num_functions': self.count_functions(),
            'num_classes': self.count_classes(),
            
            # Control flow (3 features)
            'num_if_else': self.count_control_structures(),
            'num_loops': self.count_loops(),
            'num_try_except': self.count_try_except(),
            
            # Documentation (1 feature)
            'has_docstrings': self.has_docstrings(),
            
            # Code smells (2 features)
            'single_letter_vars': self.count_single_letter_vars(),
            'magic_numbers': self.count_magic_numbers(),
            
            # Function complexity (3 features)
            'avg_func_length': self.avg_function_length(),
            'max_func_length': self.max_function_length(),
            'very_long_functions': self.count_very_long_functions()
        }


# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        analyzer = MultiLanguageAnalyzer(filepath)
        features = analyzer.extract_all_features()
        
        print("\n" + "=" * 70)
        print(f"ANALYSIS: {os.path.basename(filepath)}")
        print("=" * 70)
        print(f"Language: {features['language'].upper()}")
        print(f"\nFeatures extracted:")
        for key, value in features.items():
            if key not in ['file_name', 'language']:
                print(f"  {key:25s}: {value}")
    else:
        print("Usage: python multi_language_analyzer.py <file_path>")
        print("\nSupported: Python (.py), Java (.java), C++ (.cpp), C (.c)")
