import os
import argparse

def filter_directories(dirs, ignore_strings, ignore_hidden, verbose):
    """Filter out directories based on ignore criteria."""
    if ignore_hidden:
        dirs[:] = [d for d in dirs if not d.startswith('.')]
    dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore_strings)]
    if verbose:
        print(f"Filtered directories: {dirs}")

def should_print_file(file, file_filters, ignore_strings, ignore_hidden):
    """Determine if a file should be printed based on filters."""
    
    # Ignore hidden files
    if ignore_hidden and file.startswith('.'):
        return False

    # Filter by file type
    if file_filters:
        if not any(file.endswith(file_type) for file_type in file_filters):
            return False

    # Ignore files based on ignore_strings
    if any(ignore_str in file for ignore_str in ignore_strings):
        return False

    return True


def scan_and_print(directory, file_filters, ignore_strings, ignore_hidden, verbose):
    for root, dirs, files in os.walk(directory):
        filter_directories(dirs, ignore_strings, ignore_hidden, verbose)
        
        for file in files:
            if should_print_file(file, file_filters, ignore_strings, ignore_hidden):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    print(f"======== File Path: {file_path} ========")
                    print(content)
                    print("==================================\n")
                except UnicodeDecodeError:
                    print(f"Warning: Could not read file due to encoding issues: {file_path}")
                    exit(1)
                        
            elif verbose:
                print(f"Skipped file: {file}")

def main():
    parser = argparse.ArgumentParser(description="Scan directories and print file contents.")
    parser.add_argument("directories", nargs='+', help="List of directories to scan.")
    parser.add_argument("-f", "--filetype", nargs='+', default=[], help="Filter by file types (e.g., .txt .log).")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="Ignore files and folders containing these strings.")
    parser.add_argument("--ignore-hidden", action='store_true', help="Ignore hidden directories.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable verbose mode.")
    args = parser.parse_args()

    for directory in args.directories:
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            exit(1)
        scan_and_print(directory, args.filetype, args.ignore, args.ignore_hidden, args.verbose)

if __name__ == "__main__":
    main()
