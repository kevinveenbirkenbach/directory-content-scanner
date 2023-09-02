# Directory Content Scanner

Directory Content Scanner is a tool designed for the recursive scanning of directories, providing outputs for both file paths and their associated content. This tool is especially handy for rapid content exploration and debugging within nested file structures.

## Getting Started

### Prerequisites

- Bash shell (commonly available on Linux and macOS)

### Installation

1. Clone this repository:
   ```
   git clone https://github.com/kevinveenbirkenbach/directory-content-scanner.git
   ```

2. Navigate to the cloned directory:
   ```
   cd directory-content-scanner
   ```

3. Make the script executable:
   ```
   chmod +x scan.sh
   ```

## Usage

Run the script with a directory as its argument:

```
./scan.sh /path/to/directory
```

This will print each file's path followed by its content, separated by equal signs for clarity.

## Warning

Use this tool responsibly. If some of the target directory files are extensive, the script might produce a vast output. Always be aware of the volume of data you're dealing with before executing the script.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author

Kevin Veen-Birkenbach  
- 📧 Email: [kevin@veen.world](mailto:kevin@veen.world)
- 🌍 Website: [https://www.veen.world/](https://www.veen.world/)

## License

This project is licensed under the GNU Affero General Public License v3.0. The full license text is available in the `LICENSE` file of this repository.

## Acknowledgement

These scripts were created with the assistance of OpenAI's ChatGPT model. You can learn more about how they were created [here](https://chat.openai.com/share/71e9bc9e-d34a-4b03-bf68-4f9e994d156a).

