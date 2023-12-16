import os
import argparse
import re
import zlib

class CodeProcessor:
    PYTHON = ".py"
    JS = ".js"
    C = ".c"
    CPP = ".cpp"
    H = ".h"

    @staticmethod
    def remove_comments(content, file_type):
        """Remove comments based on file type."""
        comment_patterns = {
            CodeProcessor.PYTHON: [
                (r'\s*#.*', '',0),
                (r'\"\"\"(.*?)\"\"\"', '', re.DOTALL),
                (r"\'\'\'(.*?)\'\'\'", '', re.DOTALL)
            ],
            CodeProcessor.JS: [
                (r'\s*//.*', '',0),
                (r'/\*.*?\*/', '',0)
            ],
            CodeProcessor.C: [
                (r'\s*//.*', '',0),
                (r'/\*.*?\*/', '',0)
            ],
            CodeProcessor.CPP: [
                (r'\s*//.*', '',0),
                (r'/\*.*?\*/', '',0)
            ],
            CodeProcessor.H: [
                (r'\s*//.*', '',0),
                (r'/\*.*?\*/', '',0)
            ]
        }

        patterns = comment_patterns.get(file_type, [])
        for pattern, repl, flags in patterns:
            content = re.sub(pattern, repl, content, flags=flags)
        return content.strip()

    @staticmethod
    def compress(content):
        """Compress code using zlib."""
        return zlib.compress(content.encode())


class DirectoryHandler:
    
    @staticmethod
    def filter_directories(dirs, ignore_strings, ignore_hidden):
        """Filter out directories based on ignore criteria."""
        if ignore_hidden:
            dirs[:] = [d for d in dirs if not d.startswith('.')]
        dirs[:] = [d for d in dirs if not any(ig in d for ig in ignore_strings)]

    def should_print_file(file_path, file_filters, ignore_strings, ignore_hidden, whitelist_file, whitelist_content):
        """Determine if a file should be printed based on new criteria."""
        if ignore_hidden and os.path.basename(file_path).startswith('.'):
            return False
        if file_filters and not any(file_path.endswith(file_type) for file_type in file_filters):
            return False
        if any(ignore_str in file_path for ignore_str in ignore_strings):
            return False
        if whitelist_file and not any(whitelist_str in file_path for whitelist_str in whitelist_file):
            return False
        if whitelist_content:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                if not any(whitelist_str in content for whitelist_str in whitelist_content):
                    return False
            except UnicodeDecodeError:
                return False
        return True
    
    @staticmethod
    def print_file_content(file_path, no_comments, compress):
        """Print the content of a file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            if no_comments:
                file_type = os.path.splitext(file_path)[1]
                content = CodeProcessor.remove_comments(content, file_type)
            print(f"<< START: {file_path} >>")
            if compress:
                compressed_content = CodeProcessor.compress(content)
                print(f"COMPRESSED CODE: ")
                print(compressed_content)
            else:
                print(content)
            print("<< END >>\n")
        except UnicodeDecodeError:
            print(f"Warning: Could not read file due to encoding issues: {file_path}")
            exit(1)

    @staticmethod
    def handle_directory(directory, **kwargs):
        """Handle scanning and printing for directories."""
        for root, dirs, files in os.walk(directory):
            DirectoryHandler.filter_directories(dirs, kwargs['ignore_strings'], kwargs['ignore_hidden'])
            for file in files:
                if DirectoryHandler.should_print_file(os.path.join(root, file), kwargs['file_filters'], kwargs['ignore_strings'], kwargs['ignore_hidden'], kwargs['whitelist_file'], kwargs['whitelist_content']):
                    DirectoryHandler.print_file_content(os.path.join(root, file), kwargs['no_comments'], kwargs['compress'])
                elif kwargs['verbose']:
                    print(f"Skipped file: {file}")

    @staticmethod
    def handle_file(file_path, **kwargs):
        """Handle scanning and printing for individual files."""
        DirectoryHandler.print_file_content(file_path, kwargs['no_comments'], kwargs['compress'])


def main():
    parser = argparse.ArgumentParser(description="Scan directories and print/compile file contents.")
    parser.add_argument("paths", nargs='+', help="List of files or directories to scan.")
    parser.add_argument("-f", "--filetype", nargs='+', default=[], help="Filter by file types (e.g., .txt .log).")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="Ignore files and folders containing these strings.")
    parser.add_argument("--ignore-hidden", action='store_true', help="Ignore hidden directories and files.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Enable verbose mode.")
    parser.add_argument("--no-comments", action='store_true', help="Remove comments from the displayed content based on file type.")
    parser.add_argument("--compress", action='store_true', help="Compress code (for Python files).")
    parser.add_argument("--whitelist-file", nargs='+', default=[], help="Only display files whose paths contain one of these strings.")
    parser.add_argument("--whitelist-content", nargs='+', default=[], help="Only display files containing one of these strings in their content.")
    
        # Custom section for parameter priority
    priority_section = """
Parameter Priority Order for File Selection:
1. --ignore-hidden: Applied first to filter out hidden files and directories.
2. --ignore: Applied to ignore files and folders with specified strings.
3. --whitelist-file: Overrides ignore settings but subject to file type filter.
4. -f/--filetype: Determines which file types are processed.
5. --whitelist-content: Filters files based on content after type and ignore checks.

Post-Selection Processing:
- --no-comments: Removes comments from the content of selected files.
- --compress: Compresses content of selected files.

Note: Verbose mode (-v/--verbose) provides detailed processing information but does not affect file selection or processing."""
    parser.epilog = priority_section

    
    args = parser.parse_args()
    
    for path in args.paths:
        if os.path.isdir(path):
            DirectoryHandler.handle_directory(path, file_filters=args.filetype, ignore_strings=args.ignore, ignore_hidden=args.ignore_hidden, verbose=args.verbose, no_comments=args.no_comments, compress=args.compress, whitelist_file=args.whitelist_file, whitelist_content=args.whitelist_content)
        elif os.path.isfile(path):
            if DirectoryHandler.should_print_file(path, file_filters=args.filetype, ignore_strings=args.ignore, ignore_hidden=args.ignore_hidden, whitelist_file=args.whitelist_file, whitelist_content=args.whitelist_content):
                DirectoryHandler.handle_file(path, file_filters=args.filetype, ignore_strings=args.ignore, ignore_hidden=args.ignore_hidden, no_comments=args.no_comments, compress=args.compress)
        else:
            print(f"Error: {path} is neither a valid file nor a directory.")
            exit(1)

if __name__ == "__main__":
    main()