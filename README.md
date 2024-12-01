# Directory Content Scanner

The Directory Content Scanner is a Python-based utility designed to recursively scan directories, presenting both file paths and their content. It's an invaluable tool for in-depth content exploration and debugging within nested file structures.

## 🚀 Getting Started

### 📋 Prerequisites

- Python 3.x

### 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/kevinveenbirkenbach/directory-content-scanner.git
   ```

2. Navigate to the cloned directory:
   ```bash
   cd directory-content-scanner
   ```

### ⚡ Running Without Full Path Specification

To execute the script directly from the terminal without typing the full path, follow these steps:

#### 1. **Make the Script Executable**
Ensure the script is executable:
```bash
chmod +x scan.py
```

#### 2. **Create a Symbolic Link**
While inside the repository folder, use the following one-liner to create a symbolic link in a directory included in your `$PATH`:

```bash
ln -s "$(pwd)/scan.py" ~/.local/bin/scan-directory
```

This command uses the current directory as the base for the symbolic link and points to `~/.local/bin/scan-directory`.

## 📖 Usage

Run the Python script, specifying the target directory and any desired filters:

```bash
scan-directory /path/to/directory [options]
```

### Options:

To show the help page execute:

```bash
python3 scan.py /path/to/directory --help
```

- `paths`: List of files or directories to scan. This is a positional argument.
- `--file-types`: Filter by file types (e.g., `.txt`, `.log`). Only files with these extensions will be processed.
- `--ignore-file-strings`: Ignore files and folders containing these strings. Useful for excluding specific files or directories.
- `--ignore-hidden`: Ignore hidden directories and files (those starting with a dot).
- `-v`, `--verbose`: Enable verbose mode. This will print additional information about skipped files.
- `--no-comments`: Remove comments from the displayed content based on file type. Comments in supported file types (Python, JS, C, CPP, H) will be stripped.
- `--compress`: Compress code (for supported file types). The content will be displayed in compressed form.
- `--path-contains`: Display files whose paths contain one of these strings. Useful for narrowing down the scan to specific parts of the directory structure.
- `--content-contains`: Display files containing one of these strings in their content. The file's content will be checked, and only matching files will be shown.


## ⚠️ Caution

Exercise caution when scanning directories with large files. The script may produce extensive output. Always assess the data volume before executing the script.

## 🤝 Contributing

Contributions via pull requests are welcome. For significant modifications, kindly open an issue first to discuss the proposed changes.

## ✍️ Author

**Kevin Veen-Birkenbach**  
- 📧 [Email Kevin](mailto:kevin@veen.world)
- 🌐 [Website](https://www.veen.world/)

## 📜 License

This project is licensed under the GNU Affero General Public License v3.0. The complete license text is available in the `LICENSE` file.

## 🙏 Acknowledgements

Special thanks to OpenAI's ChatGPT model for assistance. Dive deeper into the creation process [here](https://chat.openai.com/share/71e9bc9e-d34a-4b03-bf68-4f9e994d156a), [here](https://chat.openai.com/share/3fc66009-ff4e-425e-a4a3-fc703534885d), [here](https://chatgpt.com/share/d08724c6-8f65-4b24-9828-e0f895bd1e1d) and [here](https://chatgpt.com/share/674c665d-acf8-800f-bd42-5eb7bd566f1e).
