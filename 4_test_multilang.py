"""
Multi-Language File Tester
Test code quality on individual files
"""

import sys
import joblib
import pandas as pd
from pathlib import Path

try:
    from multi_language_analyzer import MultiLanguageAnalyzer
except ImportError:
    print("Error: multi_language_analyzer.py not found!")
    sys.exit(1)


def test_file(filepath):
    """Test a single code file"""
    
    # Check if file exists
    if not Path(filepath).exists():
        print(f"❌ File not found: {filepath}")
        return
    
    # Load model
    try:
        model = joblib.load('model_multilang/classifier.pkl')
        feature_names = joblib.load('model_multilang/features.pkl')
        metadata = joblib.load('model_multilang/metadata.pkl')
    except FileNotFoundError:
        print("❌ Model not found!")
        print("\nPlease train the model first:")
        print("  python 3_train_multilang_model.py")
        return
    
    # Analyze file
    try:
        analyzer = MultiLanguageAnalyzer(filepath)
        features = analyzer.extract_all_features()
    except Exception as e:
        print(f"❌ Error analyzing file: {e}")
        return
    
    # Check if language is supported
    if analyzer.language == 'unknown':
        print(f"❌ Unsupported file type: {Path(filepath).suffix}")
        print(f"\nSupported languages: {', '.join(metadata['languages'])}")
        return
    
    # Prepare features for prediction
    features_df = pd.DataFrame([features])
    features_df = features_df[feature_names]
    
    # Predict
    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0]
    confidence = max(probability) * 100
    
    # Print results
    print("\n" + "=" * 70)
    print("CODE QUALITY ANALYSIS")
    print("=" * 70)
    
    print(f"\n📄 File: {Path(filepath).name}")
    print(f"🔤 Language: {analyzer.language.upper()}")
    print(f"📏 Lines: {features['total_lines']}")
    
    # Quality verdict
    if prediction == 1:
        verdict = "🟢 GOOD QUALITY CODE"
        emoji = "✅"
    else:
        verdict = "🔴 POOR QUALITY CODE"
        emoji = "❌"
    
    print(f"\n{emoji} {verdict}")
    print(f"📊 Confidence: {confidence:.1f}%")
    
    # Key metrics
    print(f"\n📊 KEY METRICS:")
    print(f"   Comment ratio:      {features['comment_ratio']*100:.1f}%")
    print(f"   Has docstrings:     {'Yes' if features['has_docstrings'] else 'No'}")
    print(f"   Functions:          {features['num_functions']}")
    print(f"   Classes:            {features['num_classes']}")
    print(f"   Avg function length: {features['avg_func_length']:.1f} lines")
    print(f"   Max indentation:    {features['max_indentation']} levels")
    
    # Code smells
    print(f"\n⚠️  CODE SMELLS:")
    print(f"   Single-letter vars: {features['single_letter_vars']}")
    print(f"   Magic numbers:      {features['magic_numbers']}")
    print(f"   Long functions:     {features['very_long_functions']}")
    print(f"   Long lines (>80):   {features['long_lines_count']}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    recommendations = []
    
    if features['comment_ratio'] < 0.05:
        recommendations.append("Add more comments to explain complex logic")
    
    if not features['has_docstrings']:
        recommendations.append("Add docstrings to functions and classes")
    
    if features['very_long_functions'] > 0:
        recommendations.append(f"Break down {features['very_long_functions']} long function(s) into smaller ones")
    
    if features['single_letter_vars'] > 5:
        recommendations.append("Use more descriptive variable names")
    
    if features['magic_numbers'] > 10:
        recommendations.append("Replace magic numbers with named constants")
    
    if features['num_try_except'] == 0 and features['total_lines'] > 20:
        recommendations.append("Add error handling with try-except blocks")
    
    if features['long_lines_count'] > 5:
        recommendations.append("Keep lines under 80 characters for better readability")
    
    if len(recommendations) == 0:
        print("   ✅ No major issues found!")
    else:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    print("\n" + "=" * 70)


def main():
    if len(sys.argv) < 2:
        print("=" * 70)
        print("MULTI-LANGUAGE CODE QUALITY TESTER")
        print("=" * 70)
        print("\nUsage: python 4_test_multilang.py <file_path>")
        print("\nExamples:")
        print("  python 4_test_multilang.py code/example.py")
        print("  python 4_test_multilang.py code/app.js")
        print("  python 4_test_multilang.py code/main.cpp")
        print("  python 4_test_multilang.py code/program.c")
        print("\nSupported: Python, JavaScript, C++, C")
        print("=" * 70)
        return
    
    filepath = sys.argv[1]
    test_file(filepath)


if __name__ == "__main__":
    main()
