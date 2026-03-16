"""
Multi-Language Feature Extraction
Extracts features from Python, JavaScript, C++, and C code files
"""

import pandas as pd
from pathlib import Path
import sys

# Import the multi-language analyzer
try:
    from multi_language_analyzer import MultiLanguageAnalyzer
except ImportError:
    print("Error: multi_language_analyzer.py not found!")
    print("Make sure it's in the same directory.")
    sys.exit(1)


def extract_features_from_directory(directory_path, label, language_filter=None):
    """
    Extract features from all code files in a directory
    
    Args:
        directory_path: Path to directory containing code files
        label: 0 for bad code, 1 for good code
        language_filter: Optional list of languages to include
    
    Returns:
        List of feature dictionaries
    """
    features_list = []
    
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"⚠ Warning: {directory_path} does not exist, skipping...")
        return features_list
    
    # Supported extensions
    extensions = {
        '.py': 'python',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'javascript',
        '.tsx': 'javascript',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.hpp': 'cpp',
        '.c': 'c',
        '.h': 'c'
    }
    
    # Collect all matching files
    all_files = []
    for ext in extensions.keys():
        all_files.extend(directory.glob(f'*{ext}'))
    
    print(f"\n  Found {len(all_files)} files in {directory_path}")
    
    processed = 0
    skipped = 0
    
    for filepath in all_files:
        try:
            # Analyze file
            analyzer = MultiLanguageAnalyzer(str(filepath))
            
            # Skip unknown languages
            if analyzer.language == 'unknown':
                skipped += 1
                continue
            
            # Apply language filter if specified
            if language_filter and analyzer.language not in language_filter:
                skipped += 1
                continue
            
            # Extract features
            features = analyzer.extract_all_features()
            features['label'] = label
            features_list.append(features)
            
            processed += 1
            
            # Progress update every 50 files
            if processed % 50 == 0:
                print(f"    Processed {processed} files...")
                
        except Exception as e:
            skipped += 1
            if processed == 0:  # Show first error for debugging
                print(f"    Error analyzing {filepath.name}: {e}")
    
    print(f"  ✓ Successfully processed {processed} files ({skipped} skipped)")
    
    return features_list


def main():
    print("=" * 70)
    print("MULTI-LANGUAGE FEATURE EXTRACTION")
    print("=" * 70)
    
    print("\nThis script extracts features from code files in:")
    print("  • data_multilang/good_code/")
    print("  • data_multilang/bad_code/")
    print("\n" + "=" * 70)
    
    all_features = []
    
    # Extract features from good code
    print("\n📊 ANALYZING GOOD CODE...")
    good_features = extract_features_from_directory(
        'data_multilang/good_code',
        label=1  # Good code
    )
    all_features.extend(good_features)
    
    # Extract features from bad code
    print("\n📊 ANALYZING BAD CODE...")
    bad_features = extract_features_from_directory(
        'data_multilang/bad_code',
        label=0  # Bad code
    )
    all_features.extend(bad_features)
    
    # Check if we have data
    if len(all_features) == 0:
        print("\n❌ ERROR: No features extracted!")
        print("\nMake sure you have:")
        print("  1. Run 1_collect_multilang_data.py first")
        print("  2. Files in data_multilang/good_code/ and data_multilang/bad_code/")
        return
    
    # Create DataFrame
    df = pd.DataFrame(all_features)
    
    # Save to CSV
    output_file = 'data_multilang/features.csv'
    df.to_csv(output_file, index=False)
    
    # Print summary
    print("\n" + "=" * 70)
    print("EXTRACTION COMPLETE!")
    print("=" * 70)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Total files analyzed: {len(all_features)}")
    print(f"   Good code samples:    {len(good_features)}")
    print(f"   Bad code samples:     {len(bad_features)}")
    
    # Breakdown by language
    print(f"\n📚 BREAKDOWN BY LANGUAGE:")
    for language in df['language'].unique():
        count = len(df[df['language'] == language])
        good_count = len(df[(df['language'] == language) & (df['label'] == 1)])
        bad_count = len(df[(df['language'] == language) & (df['label'] == 0)])
        print(f"   {language:12s}: {count:3d} total ({good_count} good, {bad_count} bad)")
    
    print(f"\n💾 Features saved to: {output_file}")
    print(f"   Columns: {len(df.columns)}")
    print(f"   Rows:    {len(df)}")
    
    # Show sample features
    print(f"\n📋 FEATURE COLUMNS:")
    feature_cols = [col for col in df.columns if col not in ['file_name', 'label', 'language']]
    for i, col in enumerate(feature_cols, 1):
        print(f"   {i:2d}. {col}")
    
    print("\n" + "=" * 70)
    print("NEXT STEP:")
    print("=" * 70)
    print("Run: python 3_train_multilang_model.py")
    print("=" * 70)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
