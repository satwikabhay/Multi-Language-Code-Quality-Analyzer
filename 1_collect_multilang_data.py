"""
Multi-Language Data Collection
Collects Python, Java, C++, and C files from cloned repositories
"""

import os
import shutil
from pathlib import Path


def collect_files():
    print("=" * 70)
    print("MULTI-LANGUAGE DATA COLLECTION")
    print("=" * 70)
    print("\nCollecting: Python, Java, C++, C")
    print("=" * 70)
    
    # File extensions to collect
    extensions = {
        '.py': 'Python',
        '.java': 'Java',
        '.cpp': 'C++',
        '.cc': 'C++',
        '.cxx': 'C++',
        '.c': 'C',
        '.h': 'C/C++ header'
    }
    
    # Process good code
    print("\n📦 COLLECTING GOOD CODE...")
    good_source = 'cloned_repos/good'
    good_dest = 'data_multilang/good_code'
    
    if not os.path.exists(good_source):
        print(f"❌ {good_source} not found!")
        print("Please clone repositories to cloned_repos/good/ first")
        return
    
    os.makedirs(good_dest, exist_ok=True)
    good_collected = collect_from_directory(good_source, good_dest, extensions)
    
    # Process bad code
    print("\n📦 COLLECTING BAD CODE...")
    bad_source = 'cloned_repos/bad'
    bad_dest = 'data_multilang/bad_code'
    
    if not os.path.exists(bad_source):
        print(f"❌ {bad_source} not found!")
        print("Please clone repositories to cloned_repos/bad/ first")
        return
    
    os.makedirs(bad_dest, exist_ok=True)
    bad_collected = collect_from_directory(bad_source, bad_dest, extensions)
    
    # Summary
    print("\n" + "=" * 70)
    print("COLLECTION COMPLETE!")
    print("=" * 70)
    
    total_good = len(list(Path(good_dest).glob('*')))
    total_bad = len(list(Path(bad_dest).glob('*')))
    
    print(f"\n📊 SUMMARY:")
    print(f"   Good code files: {total_good}")
    print(f"   Bad code files:  {total_bad}")
    print(f"   TOTAL:           {total_good + total_bad}")
    
    # Breakdown by language
    print(f"\n   Good code breakdown:")
    for ext, lang in extensions.items():
        count = len(list(Path(good_dest).glob(f'*{ext}')))
        if count > 0:
            print(f"     {lang:15s}: {count}")
    
    print(f"\n   Bad code breakdown:")
    for ext, lang in extensions.items():
        count = len(list(Path(bad_dest).glob(f'*{ext}')))
        if count > 0:
            print(f"     {lang:15s}: {count}")
    
    if total_good + total_bad > 0:
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print("1. Run: python 2_extract_features_multilang.py")
        print("2. Run: python 3_train_multilang_model.py")
        print("=" * 70)


def collect_from_directory(source_dir, dest_dir, extensions):
    """Collect code files from source to destination"""
    
    collected = 0
    
    # Walk through source directory
    for root, dirs, files in os.walk(source_dir):
        # Skip certain directories
        skip_dirs = ['test', 'tests', '__pycache__', 'node_modules', 
                     '.git', 'build', 'target', 'bin', 'obj']
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        
        for file in files:
            # Check if file has a valid extension
            ext = Path(file).suffix.lower()
            if ext in extensions:
                source_path = Path(root) / file
                
                # Skip very large files (>500KB)
                try:
                    if source_path.stat().st_size > 500000:
                        continue
                except:
                    continue
                
                # Create unique filename
                relative_path = source_path.relative_to(source_dir)
                unique_name = str(relative_path).replace(os.sep, '_')
                dest_path = Path(dest_dir) / unique_name
                
                # Copy file
                try:
                    shutil.copy2(source_path, dest_path)
                    collected += 1
                    
                    if collected % 50 == 0:
                        print(f"  Collected {collected} files...")
                    
                    # Limit per category
                    if collected >= 300:
                        print(f"  ✓ Reached limit of 300 files")
                        break
                        
                except Exception as e:
                    pass
        
        if collected >= 300:
            break
    
    print(f"  ✓ Collected {collected} files")
    return collected


if __name__ == "__main__":
    try:
        collect_files()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
