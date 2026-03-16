"""
Multi-Language Model Training
Trains Random Forest classifier on multi-language code features
"""

import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np


def train_model():
    print("=" * 70)
    print("MULTI-LANGUAGE MODEL TRAINING")
    print("=" * 70)
    
    # Load features
    features_file = 'data_multilang/features.csv'
    
    if not os.path.exists(features_file):
        print(f"\n❌ ERROR: {features_file} not found!")
        print("\nPlease run these first:")
        print("  1. python 1_collect_multilang_data.py")
        print("  2. python 2_extract_features_multilang.py")
        return
    
    print(f"\n📂 Loading features from: {features_file}")
    df = pd.read_csv(features_file)
    
    print(f"✓ Loaded {len(df)} samples")
    
    # Show dataset composition
    print(f"\n📊 DATASET COMPOSITION:")
    print(f"   Total samples: {len(df)}")
    print(f"   Good code:     {len(df[df['label'] == 1])} ({len(df[df['label'] == 1])/len(df)*100:.1f}%)")
    print(f"   Bad code:      {len(df[df['label'] == 0])} ({len(df[df['label'] == 0])/len(df)*100:.1f}%)")
    
    print(f"\n   By language:")
    for lang in df['language'].unique():
        count = len(df[df['language'] == lang])
        print(f"     {lang:12s}: {count} ({count/len(df)*100:.1f}%)")
    
    # Prepare features and labels
    feature_columns = [col for col in df.columns 
                      if col not in ['file_name', 'label', 'language']]
    
    X = df[feature_columns]
    y = df['label']
    
    print(f"\n🔧 FEATURES:")
    print(f"   Number of features: {len(feature_columns)}")
    print(f"   Feature names: {', '.join(feature_columns[:5])}...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        stratify=y  # Maintain class balance
    )
    
    print(f"\n📊 DATA SPLIT:")
    print(f"   Training samples:   {len(X_train)}")
    print(f"   Testing samples:    {len(X_test)}")
    print(f"   Train/Test ratio:   {len(X_train)/len(X_test):.1f}:1")
    
    # Train model
    print(f"\n🤖 TRAINING RANDOM FOREST MODEL...")
    print(f"   Parameters:")
    print(f"     - Estimators (trees): 100")
    print(f"     - Max depth: 15")
    print(f"     - Random state: 42")
    print(f"     - Using all CPU cores")
    
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        random_state=42,
        n_jobs=-1,  # Use all cores
        verbose=0
    )
    
    model.fit(X_train, y_train)
    print(f"✓ Training complete!")
    
    # Evaluate on training set
    train_predictions = model.predict(X_train)
    train_accuracy = accuracy_score(y_train, train_predictions)
    
    # Evaluate on test set
    test_predictions = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    
    # Cross-validation
    print(f"\n🔄 CROSS-VALIDATION (5-fold)...")
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    
    # Print results
    print(f"\n" + "=" * 70)
    print("TRAINING RESULTS")
    print("=" * 70)
    
    print(f"\n📈 ACCURACY:")
    print(f"   Training Accuracy:   {train_accuracy:.2%}")
    print(f"   Testing Accuracy:    {test_accuracy:.2%}")
    print(f"   Cross-Val Accuracy:  {cv_scores.mean():.2%} (+/- {cv_scores.std()*2:.2%})")
    
    # Classification report
    print(f"\n📋 DETAILED METRICS (Test Set):")
    print(classification_report(
        y_test, 
        test_predictions,
        target_names=['Bad Code', 'Good Code'],
        digits=3
    ))
    
    # Confusion matrix
    cm = confusion_matrix(y_test, test_predictions)
    print(f"📊 CONFUSION MATRIX:")
    print(f"                 Predicted")
    print(f"              Bad    Good")
    print(f"   Actual Bad  {cm[0][0]:3d}    {cm[0][1]:3d}")
    print(f"         Good  {cm[1][0]:3d}    {cm[1][1]:3d}")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\n🎯 TOP 10 MOST IMPORTANT FEATURES:")
    for i, row in feature_importance.head(10).iterrows():
        print(f"   {row['feature']:25s}: {row['importance']:.4f}")
    
    # Save model
    os.makedirs('model_multilang', exist_ok=True)
    
    model_file = 'model_multilang/classifier.pkl'
    features_file = 'model_multilang/features.pkl'
    metadata_file = 'model_multilang/metadata.pkl'
    
    joblib.dump(model, model_file)
    joblib.dump(feature_columns, features_file)
    joblib.dump({
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std(),
        'n_samples': len(df),
        'n_features': len(feature_columns),
        'languages': df['language'].unique().tolist()
    }, metadata_file)
    
    print(f"\n💾 MODEL SAVED:")
    print(f"   {model_file}")
    print(f"   {features_file}")
    print(f"   {metadata_file}")
    
    # Performance assessment
    print(f"\n" + "=" * 70)
    print("PERFORMANCE ASSESSMENT")
    print("=" * 70)
    
    if test_accuracy >= 0.90:
        rating = "EXCELLENT ⭐⭐⭐⭐⭐"
        color = "🟢"
    elif test_accuracy >= 0.80:
        rating = "VERY GOOD ⭐⭐⭐⭐"
        color = "🟢"
    elif test_accuracy >= 0.70:
        rating = "GOOD ⭐⭐⭐"
        color = "🟡"
    else:
        rating = "NEEDS IMPROVEMENT ⭐⭐"
        color = "🔴"
    
    print(f"\n{color} Model Performance: {rating}")
    print(f"\nTest Accuracy: {test_accuracy:.2%}")
    
    if test_accuracy < 0.85:
        print(f"\n💡 SUGGESTIONS TO IMPROVE:")
        print(f"   • Collect more training data (currently {len(df)} samples)")
        print(f"   • Balance dataset across languages")
        print(f"   • Add more diverse code samples")
    
    print(f"\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Test on files:  python 4_test_multilang.py <file_path>")
    print("2. Analyze repos:  python 5_github_analyzer_multilang.py <repo_url>")
    print("=" * 70)


if __name__ == "__main__":
    try:
        train_model()
    except KeyboardInterrupt:
        print("\n\nTraining interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
