import os
import argparse

def filter_directories(dirs, ignore_strings, ignore_hidden):
    """Filter out directories based on ignore criteria."""
    if ignore_hidden:
        dirs[:] = [d for d in dirs if not d.startswith('.')]
    dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore_strings)]

def should_print_file(file, file_filters, ignore_strings, ignore_hidden):
    """Determine if a file should be printed based on filters."""
    if ignore_hidden and file.startswith('.'):
        return False
    if file_filters and not any(file.endswith(file_type) for file_type in file_filters):
        return False
    if any(ignore_str in file for ignore_str in ignore_strings):
        return False
    return True

def print_file_content(file_path):
    """Print the content of a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"======== File Path: {file_path} ========")
        print(content)
        print("==================================\n")
    except UnicodeDecodeError:
        print(f"Warning: Could not read file due to encoding issues: {file_path}")
        exit(1)

def handle_directory(directory, file_filters, ignore_strings, ignore_hidden, verbose):
    """Handle scanning and printing for directories."""
    for root, dirs, files in os.walk(directory):
        filter_directories(dirs, ignore_strings, ignore_hidden)
        for file in files:
            if should_print_file(file, file_filters, ignore_strings, ignore_hidden):
                print_file_content(os.path.join(root, file))
            elif verbose:
                print(f"Skipped file: {file}")

def handle_file(file_path, file_filters, ignore_strings, ignore_hidden):
    """Handle scanning and printing for individual files."""
    if should_print_file(os.path.basename(file_path), file_filters, ignore_strings, ignore_hidden):
        print_file_content(file_path)

def main():
    parser = argparse.ArgumentParser(description="Scan directories and print file contents.")
    parser.add_argument("paths", nargs='+', help="List of files or directories to scan.")
    parser.add_argument("-f", "--filetype", nargs='+', default=[], help="Filter by file types (e.g., .txt .log).")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="Ignore files and folders containing these strings.")
    parser.add_argument("--ignore-hidden", action='store_true', help="Ignore hidden directories and files.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable verbose mode.")
    args = parser.parse_args()

    for path in args.paths:
        if os.path.isdir(path):
            handle_directory(path, args.filetype, args.ignore, args.ignore_hidden, args.verbose)
        elif os.path.isfile(path):
            handle_file(path, args.filetype, args.ignore, args.ignore_hidden)
        else:
            print(f"Error: {path} is neither a valid file nor a directory.")
            exit(1)

if __name__ == "__main__":
    main()
