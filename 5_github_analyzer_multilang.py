"""
Multi-Language GitHub Repository Analyzer
Analyzes code quality of entire GitHub repositories (Python, Java, C++, C)
Provides overall quality score and specific recommendations
"""

import os
import sys
import tempfile
import shutil
import joblib
import pandas as pd
from pathlib import Path
import re

try:
    from multi_language_analyzer import MultiLanguageAnalyzer
except ImportError:
    print("❌ Error: multi_language_analyzer.py not found!")
    print("Make sure it's in the same directory.")
    sys.exit(1)


def parse_github_url(url):
    """Extract owner and repo name from GitHub URL"""
    patterns = [
        r'github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$',
        r'github\.com/([^/]+)/([^/]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            owner, repo = match.groups()
            repo = repo.replace('.git', '')
            return owner, repo
    
    return None, None


def download_repo_files(url, temp_dir, requests):
    """Download code files from GitHub repository"""
    owner, repo = parse_github_url(url)
    
    if not owner or not repo:
        print("❌ Invalid GitHub URL format")
        print("Expected: https://github.com/username/repository")
        return []
    
    print(f"\n📦 Repository: {owner}/{repo}")
    print(f"🔍 Fetching files...")
    
    # Get repository contents
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to access repository (Status: {response.status_code})")
            if response.status_code == 404:
                print("   Repository not found or is private")
            return []
    except Exception as e:
        print(f"❌ Network error: {e}")
        return []
    
    # Find all code files recursively
    code_files = []
    extensions = ['.py', '.java', '.cpp', '.cc', '.cxx', '.c', '.h', '.hpp']
    
    def fetch_directory(path=''):
        url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                return
            
            items = resp.json()
            for item in items:
                if item['type'] == 'file':
                    file_ext = Path(item['name']).suffix.lower()
                    if file_ext in extensions:
                        code_files.append({
                            'name': item['name'],
                            'path': item['path'],
                            'download_url': item['download_url']
                        })
                elif item['type'] == 'dir' and not item['name'].startswith('.'):
                    # Recursively fetch subdirectories (limit depth)
                    if path.count('/') < 3:
                        fetch_directory(item['path'])
        except:
            pass
    
    fetch_directory()
    
    print(f"✓ Found {len(code_files)} code files")
    
    if not code_files:
        print("⚠ No code files found")
        return []
    
    # Download files
    print(f"📥 Downloading files...")
    downloaded = []
    
    for i, file_info in enumerate(code_files[:50], 1):  # Limit to 50 files
        try:
            response = requests.get(file_info['download_url'], timeout=10)
            if response.status_code == 200:
                filepath = os.path.join(temp_dir, file_info['name'])
                
                # Handle duplicate names
                counter = 1
                while os.path.exists(filepath):
                    name, ext = os.path.splitext(file_info['name'])
                    filepath = os.path.join(temp_dir, f"{name}_{counter}{ext}")
                    counter += 1
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                downloaded.append(filepath)
                
                if i % 10 == 0:
                    print(f"  Downloaded {i}/{min(len(code_files), 50)} files...")
        except:
            pass
        
        if i >= 50:
            print(f"⚠ Limited to first 50 files")
            break
    
    print(f"✓ Downloaded {len(downloaded)} files successfully")
    return downloaded


def analyze_repository(file_paths, model, feature_names):
    """Analyze all files in the repository"""
    
    if not file_paths:
        return None
    
    print(f"\n🔬 Analyzing {len(file_paths)} files...")
    
    results = []
    
    for filepath in file_paths:
        try:
            analyzer = MultiLanguageAnalyzer(filepath)
            
            # Skip unknown languages
            if analyzer.language == 'unknown':
                continue
            
            features = analyzer.extract_all_features()
            
            # Prepare features for prediction
            features_df = pd.DataFrame([features])
            features_df = features_df[feature_names]
            
            # Predict
            prediction = model.predict(features_df)[0]
            probability = model.predict_proba(features_df)[0]
            confidence = max(probability) * 100
            
            results.append({
                'file': os.path.basename(filepath),
                'language': analyzer.language,
                'prediction': prediction,
                'confidence': confidence,
                'features': features
            })
        except Exception as e:
            pass
    
    return results


def generate_recommendations(results):
    """Generate specific recommendations based on analysis"""
    
    recommendations = []
    issues = {
        'low_comments': 0,
        'no_docstrings': 0,
        'long_functions': 0,
        'single_letter_vars': 0,
        'magic_numbers': 0,
        'long_lines': 0,
        'no_error_handling': 0,
        'deep_nesting': 0
    }
    
    for result in results:
        f = result['features']
        
        if f['comment_ratio'] < 0.05:
            issues['low_comments'] += 1
        if not f['has_docstrings']:
            issues['no_docstrings'] += 1
        if f['very_long_functions'] > 0:
            issues['long_functions'] += 1
        if f['single_letter_vars'] > 5:
            issues['single_letter_vars'] += 1
        if f['magic_numbers'] > 10:
            issues['magic_numbers'] += 1
        if f['long_lines_count'] > 5:
            issues['long_lines'] += 1
        if f['num_try_except'] == 0 and f['total_lines'] > 20:
            issues['no_error_handling'] += 1
        if f['max_indentation'] > 5:
            issues['deep_nesting'] += 1
    
    # Generate recommendations
    total_files = len(results)
    
    if issues['low_comments'] > total_files * 0.5:
        recommendations.append({
            'priority': 'HIGH',
            'issue': 'Insufficient Comments',
            'affected': f"{issues['low_comments']}/{total_files} files",
            'suggestion': 'Add comments explaining complex logic and function purposes'
        })
    
    if issues['no_docstrings'] > total_files * 0.5:
        recommendations.append({
            'priority': 'HIGH',
            'issue': 'Missing Documentation',
            'affected': f"{issues['no_docstrings']}/{total_files} files",
            'suggestion': 'Add docstrings/Javadoc to functions and classes'
        })
    
    if issues['long_functions'] > total_files * 0.3:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Very Long Functions',
            'affected': f"{issues['long_functions']}/{total_files} files",
            'suggestion': 'Break down functions longer than 50 lines into smaller ones'
        })
    
    if issues['single_letter_vars'] > total_files * 0.4:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Poor Variable Naming',
            'affected': f"{issues['single_letter_vars']}/{total_files} files",
            'suggestion': 'Use descriptive variable names instead of single letters'
        })
    
    if issues['magic_numbers'] > total_files * 0.4:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Magic Numbers',
            'affected': f"{issues['magic_numbers']}/{total_files} files",
            'suggestion': 'Replace hardcoded numbers with named constants'
        })
    
    if issues['deep_nesting'] > total_files * 0.3:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Deep Nesting',
            'affected': f"{issues['deep_nesting']}/{total_files} files",
            'suggestion': 'Reduce indentation depth (max 4-5 levels recommended)'
        })
    
    if issues['no_error_handling'] > total_files * 0.5:
        recommendations.append({
            'priority': 'MEDIUM',
            'issue': 'Lack of Error Handling',
            'affected': f"{issues['no_error_handling']}/{total_files} files",
            'suggestion': 'Add try-catch/try-except blocks for error handling'
        })
    
    return recommendations


def print_analysis_report(results, recommendations):
    """Print comprehensive analysis report"""
    
    print("\n" + "=" * 70)
    print("REPOSITORY ANALYSIS REPORT")
    print("=" * 70)
    
    # Overall statistics
    good_count = sum(1 for r in results if r['prediction'] == 1)
    bad_count = len(results) - good_count
    avg_confidence = sum(r['confidence'] for r in results) / len(results)
    
    overall_score = (good_count / len(results)) * 100
    
    print(f"\n📊 OVERALL QUALITY SCORE: {overall_score:.1f}%")
    print(f"   Total files analyzed: {len(results)}")
    print(f"   Good quality files:   {good_count} ({good_count/len(results)*100:.1f}%)")
    print(f"   Poor quality files:   {bad_count} ({bad_count/len(results)*100:.1f}%)")
    print(f"   Average confidence:   {avg_confidence:.1f}%")
    
    # Quality rating
    if overall_score >= 80:
        rating = "EXCELLENT ⭐⭐⭐⭐⭐"
        color = "🟢"
    elif overall_score >= 60:
        rating = "GOOD ⭐⭐⭐⭐"
        color = "🟡"
    elif overall_score >= 40:
        rating = "FAIR ⭐⭐⭐"
        color = "🟠"
    else:
        rating = "NEEDS IMPROVEMENT ⭐⭐"
        color = "🔴"
    
    print(f"\n{color} RATING: {rating}")
    
    # Language breakdown
    print(f"\n📚 BREAKDOWN BY LANGUAGE:")
    languages = {}
    for result in results:
        lang = result['language']
        if lang not in languages:
            languages[lang] = {'total': 0, 'good': 0, 'bad': 0}
        languages[lang]['total'] += 1
        if result['prediction'] == 1:
            languages[lang]['good'] += 1
        else:
            languages[lang]['bad'] += 1
    
    for lang, counts in sorted(languages.items()):
        print(f"   {lang.upper():8s}: {counts['total']:2d} files "
              f"({counts['good']} good, {counts['bad']} bad)")
    
    # File-by-file breakdown
    print(f"\n" + "=" * 70)
    print("FILE-BY-FILE BREAKDOWN")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        status = "✓ GOOD" if result['prediction'] == 1 else "✗ BAD"
        lang = result['language'].upper()
        print(f"{i:2d}. [{lang:6s}] {result['file']:35s} {status} ({result['confidence']:.0f}%)")
    
    # Recommendations
    if recommendations:
        print(f"\n" + "=" * 70)
        print("🔧 RECOMMENDATIONS FOR IMPROVEMENT")
        print("=" * 70)
        
        for i, rec in enumerate(recommendations, 1):
            priority_colors = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
            color = priority_colors.get(rec['priority'], '')
            
            print(f"\n{i}. {color} {rec['priority']} PRIORITY: {rec['issue']}")
            print(f"   Affected: {rec['affected']}")
            print(f"   → {rec['suggestion']}")
    else:
        print(f"\n" + "=" * 70)
        print("✅ NO MAJOR ISSUES FOUND - EXCELLENT CODE QUALITY!")
        print("=" * 70)
    
    print("\n" + "=" * 70)


def main():
    print("=" * 70)
    print("MULTI-LANGUAGE GITHUB REPOSITORY ANALYZER")
    print("=" * 70)
    print("\nAnalyzes: Python, Java, C++, C")
    print("Provides: Quality score + Recommendations")
    print("=" * 70)
    
    # Load model
    print("\n🤖 Loading trained model...")
    try:
        model = joblib.load('model_multilang/classifier.pkl')
        feature_names = joblib.load('model_multilang/features.pkl')
        print("✓ Model loaded successfully")
    except:
        print("❌ Error: Model not found!")
        print("Please run 3_train_multilang_model.py first")
        return
    
    # Get GitHub URL
    print("\n" + "=" * 70)
    if len(sys.argv) > 1:
        github_url = sys.argv[1]
    else:
        print("\nExamples:")
        print("  https://github.com/psf/requests")
        print("  https://github.com/google/gson")
        print("  https://github.com/curl/curl")
        github_url = input("\nEnter GitHub repository URL: ").strip()
    
    if not github_url:
        print("❌ No URL provided")
        return
    
    # Check requests library
    try:
        import requests
    except ImportError:
        print("\n❌ 'requests' library not installed")
        print("Install with: pip install requests")
        return
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download repository files
        file_paths = download_repo_files(github_url, temp_dir, requests)
        
        if not file_paths:
            print("\n❌ Could not download files from repository")
            return
        
        # Analyze files
        results = analyze_repository(file_paths, model, feature_names)
        
        if not results:
            print("\n❌ Analysis failed")
            return
        
        # Generate recommendations
        recommendations = generate_recommendations(results)
        
        # Print report
        print_analysis_report(results, recommendations)
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    print("\n💡 TIP: Use these recommendations to improve your code quality!")
    print("=" * 70)


if __name__ == "__main__":
    main()
