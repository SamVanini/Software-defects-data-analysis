import pathlib
import importlib

def test_imports():
    ...

def test_folders_structure():
    ...

def test_loading_data():
    ...

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