import os
import argparse
import re
import zlib

def remove_comments(content, file_type):
    """Remove comments from the content based on file type."""
    if file_type == ".py":
        # Remove Python single line comments
        content = re.sub(r'^\s*#.*\n?', '', content, flags=re.MULTILINE)
        # Remove triple double-quote and triple single-quote docstrings
        content = re.sub(r'\"\"\"(.*?)\"\"\"', '', content, flags=re.DOTALL)
        content = re.sub(r"\'\'\'(.*?)\'\'\'", '', content, flags=re.DOTALL)
    elif file_type == ".js" or file_type == ".c" or file_type == ".cpp" or file_type == ".h":
        # Remove C-style comments (// and /* */)
        content = re.sub(r'\s*//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Add more file types and their comment styles as needed
    return content.strip()

def compress_code(content):
    """Compress code using zlib."""
    return zlib.compress(content.encode())

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

def print_file_content(file_path, no_comments, compress):
    """Print the content of a file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        if no_comments:
            file_type = os.path.splitext(file_path)[1]
            content = remove_comments(content, file_type)
        print(f"======== File Path: {file_path} ========")
        if compress:
            compressed_content = compress_code(content)
            print(f"======== Compressed Code ========")
            print(compressed_content)
        else:
            print(content)
        print("==================================\n")
    except UnicodeDecodeError:
        print(f"Warning: Could not read file due to encoding issues: {file_path}")
        exit(1)

def handle_directory(directory, file_filters, ignore_strings, ignore_hidden, verbose, no_comments, compress):
    """Handle scanning and printing for directories."""
    for root, dirs, files in os.walk(directory):
        filter_directories(dirs, ignore_strings, ignore_hidden)
        for file in files:
            if should_print_file(file, file_filters, ignore_strings, ignore_hidden):
                print_file_content(os.path.join(root, file), no_comments, compress)
            elif verbose:
                print(f"Skipped file: {file}")

def handle_file(file_path, file_filters, ignore_strings, ignore_hidden, no_comments, compress):
    """Handle scanning and printing for individual files."""
    print_file_content(file_path, no_comments, compress)

def main():
    parser = argparse.ArgumentParser(description="Scan directories and print/compile file contents.")
    parser.add_argument("paths", nargs='+', help="List of files or directories to scan.")
    parser.add_argument("-f", "--filetype", nargs='+', default=[], help="Filter by file types (e.g., .txt .log).")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="Ignore files and folders containing these strings.")
    parser.add_argument("--ignore-hidden", action='store_true', help="Ignore hidden directories and files.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable verbose mode.")
    parser.add_argument("--no-comments", action='store_true', help="Remove comments from the displayed content based on file type.")
    parser.add_argument("--compress", action='store_true', help="Compress code (for Python files).")
    args = parser.parse_args()

    for path in args.paths:
        if os.path.isdir(path):
            handle_directory(path, args.filetype, args.ignore, args.ignore_hidden, args.verbose, args.no_comments, args.compress)
        elif os.path.isfile(path):
            handle_file(path, args.filetype, args.ignore, args.ignore_hidden, args.no_comments, args.compress)
        else:
            print(f"Error: {path} is neither a valid file nor a directory.")
            exit(1)

if __name__ == "__main__":
    main()
