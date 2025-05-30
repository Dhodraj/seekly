# Seekly CLI

<p align="center">
  <img src="assets/seekly.jpg" alt="Seekly Logo" width="200"/>
</p>

A command-line tool for natural language search across your codebase using semantic code understanding.

## Overview

Seekly CLI enables semantic search for files using natural language queries. It leverages advanced embedding models to understand code semantics and finds the most relevant files based on their meaning, not just keywords.

## Features

- **Natural Language Search**: Find files using semantic queries (e.g., "find file with custom sorting algorithm")
- **Code-Aware Embeddings**: Uses models specifically trained for code understanding
- **Function-Level Search**: Extracts and indexes individual functions for precise results
- **Language Agnostic**: Works with multiple programming languages and file types
- **Fast Matching**: Caches embeddings for quick subsequent searches
- **Flexible CLI**: Simple interface with customizable parameters
- **System-wide Search**: Can search from any directory, including the root directory of your system

## Installation

**Recommended Installation Method:**
```bash
# One-line installation with curl (works on all systems including externally managed environments)
curl -sSL https://raw.githubusercontent.com/Dhodraj/seekly/master/pipx_install.py | python3
```

This method works reliably across all systems, including externally managed Python environments like those in modern Debian/Ubuntu systems.

### Alternative Installation Methods

<details>
<summary>Click to expand other installation options</summary>

```bash
# Using wget
wget -qO- https://raw.githubusercontent.com/Dhodraj/seekly/master/pipx_install.py | python3

# Or install directly with pipx (good for externally managed environments)
pipx install seekly

# Or standard pip installation (not recommended for externally managed environments)
pip install seekly

# For development
git clone https://github.com/Dhodraj/seekly.git
cd seekly
pip install -e .
```
</details>

## Uninstallation

**Recommended Uninstallation Method:**
```bash
# Uninstall with pipx (works reliably across all systems)
pipx uninstall seekly

# Remove all Seekly data from your system
rm -rf ~/.seekly  # Linux/macOS
# OR
rd /s /q %USERPROFILE%\.seekly  # Windows
```

This uninstallation method works consistently across all system configurations and is especially recommended for externally managed Python environments.

<details>
<summary>Click to expand other uninstallation options</summary>

```bash
# Only if installed with pip on systems that allow direct pip management
pip uninstall -y seekly
```
</details>

## Usage

### With pip installation

After installing with pip, you can use Seekly from anywhere:

```bash
# Search in a specific directory
seekly search "find files with logging functionality" --dir /path/to/your/project

# Search from the root directory (/)
seekly search "important configuration file" --dir /

# Show information about cache and model status
seekly info
```

### Interactive Mode

If you run the search command without a query, Seekly enters interactive mode:

```bash
seekly search
Seekly Interactive Search
Enter your query (or 'exit' to quit):
> 
```

### Running directly from the project

```bash
# Navigate to the project directory
cd /path/to/seekly

# Run the search
python seekly.py search "find files with logging functionality" --dir /path/to/your/project
```

### Command Options

```bash
# Search with custom parameters
seekly search "custom sorting algorithm" --dir ./code --top-k 10 --similarity 0.6

# Clear cache data
seekly clear --all
```

### Command Help

```bash
# Show general help
seekly --help

# Show help for a specific command
seekly search --help
seekly clear --help
seekly info --help
```

## Arguments and Options

- **search**: Search for files matching a natural language query
  - `query`: The natural language query (optional; if omitted, enters interactive mode)
  - `--dir, -d`: Target directory (default: current directory)
  - `--top-k, -k`: Maximum number of results to show (default: 10)
  - `--similarity, -s`: Minimum similarity score (default: 0.4)
  - `--snippets/--no-snippets`: Show/hide code snippets in results (default: show)
  - `--all/--limit`: Show all matching results vs limiting to top-k (default: all)

- **clear**: Clear cached data to free up disk space
  - `--yes, -y`: Skip confirmation prompt
  - `--all, -a`: Clear both model and embeddings cache
  - `--embeddings, -e`: Clear only embedding cache
  - `--model, -m`: Clear only model cache
  - `--dir, -d`: Clear cache for specific directory only

- **info**: Show information about Seekly status
  - (No options)

- **open**: Open a file that matches your description
  - `query`: The file description to search for
  - `--dir, -d`: Target directory (default: current directory)
  - `--editor, -e`: Editor to use (defaults to system default)

## Supported File Types

Seekly supports a wide range of file extensions across multiple categories:

- **Programming Languages**: Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Rust, Swift, Kotlin, and many more
- **Web Development**: HTML, CSS, SCSS, SASS, SVG, Vue, Svelte
- **Documentation**: Markdown, RST, TXT, ADoc, TeX
- **Configuration**: JSON, YAML, TOML, INI, and various config formats
- **DevOps & CI/CD**: Terraform, Dockerfiles, pipeline definitions

Run `seekly list` to see all supported extensions, or `seekly list --group` to view them by language family.

## Example Output

```
$ seekly search "custom sorting algorithm" --dir /home
Searching for: 'custom sorting algorithm' in /home
Found 3 results in 0.85 seconds:

1. ★ user/projects/algorithms/bubble_sort.py: 0.9234

   Relevant code:
   1: def bubble_sort(arr):
   2:     n = len(arr)
   3:     for i in range(n):
   4:         for j in range(0, n - i - 1):
   5:             if arr[j] > arr[j + 1]:
   6:                 arr[j], arr[j + 1] = arr[j + 1], arr[j]
   7:     return arr

2.   user/docs/quick_sort.js: 0.8752

   Relevant code:
   1: function quickSort(arr) {
   2:     if (arr.length <= 1) {
   3:         return arr;
   4:     }
```

## System Requirements

- Python 3.8 or higher
- Internet connection (for the first run to download the model)
- Sufficient storage for model files (~300MB)

## Development

### Project Structure

```
seekly/
├── seekly.py           # Main CLI script and entry point
├── requirements.txt    # Dependencies
├── setup.py            # pip installation script
├── seekly/
│   ├── __init__.py     # Package initialization and constants
│   ├── model.py        # Model handling
│   ├── file_processor.py  # File reading and function extraction
│   ├── search.py       # Search functionality
│   └── tests/          # Test files and fixtures
```

### Running Tests

```bash
python -m unittest discover -s seekly/tests
```

## Future Enhancements

- Line-specific search results
- Fine-tuning for specific codebases
- Advanced query reformulation
- Machine learning-based result ranking

## License

MIT

## Acknowledgments

This project leverages advanced embedding models from Hugging Face and SentenceTransformers.
