# Streamlit Explorer

A custom file and folder browser component for Streamlit applications, providing an intuitive interface for selecting files and directories with a Windows File Explorer-like experience.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit Version](https://img.shields.io/badge/streamlit-1.31.0%2B-red)
![License](https://img.shields.io/badge/license-MIT-green)

## ✨ Features

- 📁 **DirPicker**: Browse and select folders with ease
- 📄 **FilePicker**: Browse and select files with optional extension filtering
- 🔍 **Real-time Search**: Filter folders and files as you type
- ⬆️ **Smart Navigation**: 
  - Up button to go to parent folder
  - Back button to return to previous location
  - Direct path entry for quick navigation
- 📏 **Scrollable Interface**: Fixed-height container (450px) with smooth scrolling
- 🎨 **Clean UI**: Modern, user-friendly interface that integrates seamlessly with Streamlit
- 🔄 **Fragment-based Rendering**: Only refreshes the dialog, not the entire page
- 🔑 **Multiple Instances**: Use multiple pickers on the same page with unique keys

## 📦 Installation

```bash
pip install streamlit-explorer
```

## 🚀 Quick Start

### DirPicker - Select Folders

```python
import streamlit as st
from streamlit_explorer import DirPicker

st.title("Folder Selection Example")

# Simple usage
selected_folder = DirPicker(key="folder_picker")

if selected_folder:
    st.write(f"You selected: {selected_folder}")
```

### FilePicker - Select Files

```python
import streamlit as st
from streamlit_explorer import FilePicker

st.title("File Selection Example")

# Simple usage
selected_file = FilePicker(key="file_picker")

if selected_file:
    st.write(f"You selected: {selected_file}")
    
    # Read and display the file
    with open(selected_file, 'r') as f:
        content = f.read()
        st.text(content)
```

## 📖 Usage Examples

### Basic Folder Selection

```python
import streamlit as st
from streamlit_explorer import DirPicker

selected_folder = DirPicker(key="my_folder")

if selected_folder:
    st.success(f"Selected: {selected_folder}")
```

### File Selection with Extension Filter

```python
import streamlit as st
from streamlit_explorer import FilePicker

# Filter for specific file types
selected_file = FilePicker(
    key="python_picker",
    file_extensions=['.py', '.pyw']
)

if selected_file:
    st.success(f"Selected Python file: {selected_file}")
```

### Custom Starting Path

```python
import streamlit as st
from streamlit_explorer import DirPicker, FilePicker

# Start from a specific directory
folder = DirPicker(
    key="custom_folder",
    start_path="/home/user/projects"
)

file = FilePicker(
    key="custom_file",
    start_path="/home/user/documents"
)
```

### Multiple Pickers on Same Page

```python
import streamlit as st
from streamlit_explorer import DirPicker, FilePicker

col1, col2 = st.columns(2)

with col1:
    st.subheader("Select Input Folder")
    input_folder = DirPicker(key="input_folder")

with col2:
    st.subheader("Select Output Folder")
    output_folder = DirPicker(key="output_folder")

st.subheader("Select Configuration File")
config_file = FilePicker(
    key="config_file",
    file_extensions=['.json', '.yaml', '.yml']
)
```

### Complete Application Example

```python
import streamlit as st
from streamlit_explorer import DirPicker, FilePicker
import os

st.title("📁 File Processing Application")

# Select source folder
st.header("1. Select Source Folder")
source_folder = DirPicker(key="source")

if source_folder:
    st.info(f"Source: {source_folder}")
    
    # Select destination folder
    st.header("2. Select Destination Folder")
    dest_folder = DirPicker(key="destination")
    
    if dest_folder:
        st.info(f"Destination: {dest_folder}")
        
        # Select files to process
        st.header("3. Select Files to Process")
        
        col1, col2 = st.columns(2)
        
        with col1:
            csv_file = FilePicker(
                key="csv_file",
                start_path=source_folder,
                file_extensions=['.csv']
            )
        
        with col2:
            excel_file = FilePicker(
                key="excel_file",
                start_path=source_folder,
                file_extensions=['.xlsx', '.xls']
            )
        
        # Process button
        if csv_file and excel_file:
            if st.button("Process Files", type="primary"):
                st.success("Processing started!")
                # Your processing logic here
```

## 🎯 API Reference

### DirPicker

```python
DirPicker(key: str, start_path: str = None) -> str | None
```

**Parameters:**
- `key` (str, required): Unique identifier for the picker instance. Must be unique across all pickers in your app.
- `start_path` (str, optional): Starting directory path. Defaults to user's home directory if not specified.

**Returns:**
- `str`: Absolute path to the selected folder
- `None`: If no folder has been selected yet

**Example:**
```python
folder = DirPicker(key="my_folder", start_path="/home/user")
```

### FilePicker

```python
FilePicker(key: str, start_path: str = None, file_extensions: list = None) -> str | None
```

**Parameters:**
- `key` (str, required): Unique identifier for the picker instance. Must be unique across all pickers in your app.
- `start_path` (str, optional): Starting directory path. Defaults to user's home directory if not specified.
- `file_extensions` (list, optional): List of file extensions to filter. Extensions should include the dot (e.g., `['.txt', '.pdf']`). If not specified, all files are shown.

**Returns:**
- `str`: Absolute path to the selected file
- `None`: If no file has been selected yet

**Example:**
```python
file = FilePicker(
    key="my_file",
    start_path="/home/user/documents",
    file_extensions=['.txt', '.md', '.pdf']
)
```

## 🎨 Features in Detail

### Navigation Controls

1. **Direct Path Entry**: Type or paste any valid path directly into the text input at the top
2. **Search Box**: Filter folders/files in real-time as you type (case-insensitive)
3. **Up Button (⬆️)**: Navigate to the parent directory (disabled at root)
4. **Back Button (⬅️)**: Return to the previous location in your navigation history
5. **Folder Buttons**: Click any folder to navigate into it
6. **File Buttons** (FilePicker only): Click any file to select it

### Scrollable Container

- Fixed height of 450px for the file/folder list
- Smooth scrolling for directories with many items
- Navigation controls remain accessible outside the scroll area

### Search Functionality

- Real-time filtering as you type
- Case-insensitive matching
- Searches both files and folders (in FilePicker)
- Clears automatically when navigating to a new folder

### File Extension Filtering

When using FilePicker with the `file_extensions` parameter:
- Only files with matching extensions are displayed
- Multiple extensions can be specified
- Folders are always shown for navigation
- Extensions must include the dot (`.txt`, not `txt`)

### Error Handling

- Gracefully handles permission denied errors
- Displays clear error messages
- Continues to function even when some directories are inaccessible

## 📋 Requirements

- Python >= 3.8
- Streamlit >= 1.31.0

## 🔧 Installation from Source

```bash
# Clone the repository
git clone https://github.com/OlegRezinski/streamlit_explorer.git
cd streamlit_explorer

# Install in development mode
pip install -e .
```

## 🐛 Known Issues and Limitations

- Only works with local file systems (no network drives or cloud storage)
- Requires appropriate file system permissions
- May have performance issues with directories containing thousands of items

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to:
- Update tests as appropriate
- Follow the existing code style
- Update documentation for any changed functionality

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💬 Support

- 📫 Report issues: [GitHub Issues](https://github.com/OlegRezinski/streamlit_explorer/issues)
- 💡 Feature requests: [GitHub Discussions](https://github.com/OlegRezinski/streamlit_explorer/discussions)
- 📖 Documentation: [GitHub Wiki](https://github.com/OlegRezinski/streamlit_explorer/wiki)

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Inspired by Windows File Explorer and native file pickers

## 📊 Changelog

### Version 0.1.0 (Initial Release)
- ✨ DirPicker for folder selection
- ✨ FilePicker for file selection
- 🔍 Real-time search functionality
- ⬆️ Smart navigation (Up, Back, Direct path entry)
- 📏 Scrollable interface with 450px container
- 🎨 Clean, modern UI
- 🔄 Fragment-based rendering for better performance

## 🗺️ Roadmap

- [ ] Add drag-and-drop support
- [ ] Support for selecting multiple files/folders
- [ ] Customizable themes
- [ ] Breadcrumb navigation
- [ ] File preview functionality
- [ ] Sort options (by name, date, size)
- [ ] Network drive support
- [ ] Cloud storage integration

---

Made with ❤️ by [Your Name](https://github.com/yourusername)

**Star ⭐ this repository if you find it useful!**