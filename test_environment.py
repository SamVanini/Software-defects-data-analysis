from pathlib import Path
import importlib

def test_imports():
    required_imports = [
        'polars',
        'numpy',
        'jupyter',
        'dotenv',
        'matplotlib',
        'seaborn',
        'sklearn'
    ]

    missing_imports = []

    for mod in required_imports:
        try:
            importlib.import_module(mod)
            print(f"Package {mod} imported correctly")
        except ImportError as e:
            missing_imports.append(mod)
            print(f"Failed to import package {mod}: {e}")

    if missing_imports:
        print(f"Packages not imported: {' ,'.join(missing_imports)}")
        return False
    else:
        print(f"Required packages successfully imported")
        return True

def test_folders_structure():
    required_files = [
        'requirements.txt',
        'data/sample.csv',
        'notebooks/data_workflow.ipynb'
    ]

    required_folders = [
        'notebooks',
        'output'
    ]

    errors = False

    for file in required_files:
        if Path(file).exists():
            print(f"File {file} found")
        else:
            print(f"File {file} not found")
            errors = True

    for folder in required_folders:
        if Path(folder).exists():
            print(f"Folder {folder} found")
        else:
            print(f"Folder {folder} not found")
            errors = True

    return errors == False

def test_loading_data():
    try:
        import pandas as pd

        df = pd.read_csv('data/sample.csv')

        print(f"Sample data loaded: {len(df)} records found")
        print(f"Columns: {list(df.columns)}")

        if len(df) > 0 and len(df.columns) >= 6:
            print("Everything seems ok")
            return True
        else:
            print("Data frame size or columns number is off")
            return False
    except Exception as e:
        print(f"Loading sample data failed: {e}")
        return False

def main():
    tests = [
        ("Packages import", test_imports),
        ("Folder structure", test_folders_structure),
        ("Data loading", test_loading_data)
    ]

    results = []

    for name, function in tests:
        try:
            result = function()
            results.append((name, result))
        except:
            results.append((name, False))

    passed = sum(True in result for result in results)
    total = len(results)

    for test_name, outcome in results:
        status = "Pass" if outcome else "Fail"
        print(f"{test_name}: {status}")

    if passed == total:
        print("All tests passed! Environment ready to use")
        return 0
    else:
        print(f"{total - passed} test(s) failed. Check environment setup")
        return 1
    
if __name__ ==  "__main__":
    main()