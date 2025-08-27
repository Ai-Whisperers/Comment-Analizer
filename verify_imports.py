#!/usr/bin/env python
"""
Verification script to check if all imports work correctly after fixes
Run this after installing the package with: pip install -e .
"""

import sys
from pathlib import Path

def verify_imports():
    """Verify that all critical imports work correctly"""
    
    print("=" * 60)
    print("IMPORT VERIFICATION SCRIPT")
    print("=" * 60)
    print()
    
    results = []
    
    # Test imports that should work after proper installation
    test_imports = [
        ("Components", "from src.components import CostOptimizationUI, EnhancedResultsUI, OptimizedFileUploadUI"),
        ("Services", "from src.services.session_manager import SessionManager"),
        ("File Upload Service", "from src.services.file_upload_service import FileUploadService"),
        ("Sentiment Analysis", "from src.sentiment_analysis.enhanced_analyzer import EnhancedAnalyzer"),
        ("Enhanced Analysis", "from src.enhanced_analysis import EnhancedAnalysis"),
        ("Improved Analysis", "from src.improved_analysis import ImprovedAnalysis"),
        ("Excel Export", "from src.professional_excel_export import ProfessionalExcelExporter"),
        ("Data Processing", "from src.data_processing.comment_reader import CommentReader"),
        ("Language Detection", "from src.data_processing.language_detector import LanguageDetector"),
        ("Pattern Detection", "from src.pattern_detection.pattern_detector import PatternDetector"),
        ("API Components", "from src.api.cache_manager import CacheManager"),
    ]
    
    for name, import_statement in test_imports:
        try:
            exec(import_statement)
            results.append((name, "✅ SUCCESS"))
            print(f"✅ {name}: Import successful")
        except ImportError as e:
            results.append((name, f"❌ FAILED: {str(e)}"))
            print(f"❌ {name}: Import failed - {str(e)}")
        except Exception as e:
            results.append((name, f"⚠️ ERROR: {str(e)}"))
            print(f"⚠️ {name}: Unexpected error - {str(e)}")
    
    print()
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    success_count = sum(1 for _, status in results if "SUCCESS" in status)
    total_count = len(results)
    
    print(f"Total imports tested: {total_count}")
    print(f"Successful imports: {success_count}")
    print(f"Failed imports: {total_count - success_count}")
    
    if success_count == total_count:
        print("\n🎉 All imports working correctly!")
        print("The pathway fixes have been successfully applied.")
        return True
    else:
        print("\n⚠️ Some imports are still failing.")
        print("Please ensure you've run: pip install -e .")
        print("from the project root directory.")
        return False

def check_sys_path_clean():
    """Check if any files still have sys.path modifications"""
    
    print()
    print("=" * 60)
    print("CHECKING FOR REMAINING sys.path MODIFICATIONS")
    print("=" * 60)
    print()
    
    files_to_check = [
        "src/main.py",
        "tests/conftest.py",
        "tests/test_data_processing.py",
        "tests/test_pattern_detection.py",
        "tests/test_api_integration.py",
        "test_enhanced_features.py"
    ]
    
    issues_found = []
    
    for file_path in files_to_check:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                content = full_path.read_text(encoding='utf-8')
                if 'sys.path.insert' in content or 'sys.path.append' in content:
                    # Check if it's not in a comment
                    for line_num, line in enumerate(content.split('\n'), 1):
                        if ('sys.path.insert' in line or 'sys.path.append' in line) and not line.strip().startswith('#'):
                            issues_found.append((file_path, line_num))
                            print(f"⚠️ Found sys.path modification in {file_path}:{line_num}")
                else:
                    print(f"✅ {file_path}: Clean (no sys.path modifications)")
            except Exception as e:
                print(f"❌ Error reading {file_path}: {e}")
        else:
            print(f"ℹ️ {file_path}: File not found (skipped)")
    
    if not issues_found:
        print("\n🎉 No sys.path modifications found! Code is clean.")
        return True
    else:
        print(f"\n⚠️ Found {len(issues_found)} files with sys.path modifications.")
        print("These should be removed for proper package structure.")
        return False

def main():
    """Main verification function"""
    
    print("\nStarting pathway verification...\n")
    
    # Check for sys.path modifications
    sys_path_clean = check_sys_path_clean()
    
    # Verify imports
    imports_working = verify_imports()
    
    # Final summary
    print()
    print("=" * 60)
    print("FINAL STATUS")
    print("=" * 60)
    
    if sys_path_clean and imports_working:
        print("✅ All pathway fixes successfully implemented!")
        print("✅ The codebase is ready for deployment.")
        print("\nNext steps:")
        print("1. Run the application: python run.py")
        print("2. Run tests: pytest")
        return 0
    else:
        print("⚠️ Some issues remain.")
        if not imports_working:
            print("\nTo fix import issues:")
            print("1. Run: pip install -e .")
            print("2. Verify installation: pip list | grep comment-analyzer")
        if not sys_path_clean:
            print("\nTo fix sys.path issues:")
            print("Review the files listed above and remove sys.path modifications")
        return 1

if __name__ == "__main__":
    sys.exit(main())