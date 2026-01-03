"""
Streamlit Path Picker - A custom file and folder browser for Streamlit applications.
"""

import streamlit as st
import os
from pathlib import Path

__version__ = "0.1.0"
__all__ = ["DirPicker", "FilePicker"]


def DirPicker(key="dir_picker", start_path=None):
    """
    Display a folder browser dialog for selecting directories.

    Args:
        key (str): Unique key for the picker instance
        start_path (str, optional): Starting directory path. Defaults to user's home directory.

    Returns:
        str or None: Selected folder path, or None if no selection made

    Example:
        >>> selected_folder = DirPicker(key="my_folder_picker")
        >>> if selected_folder:
        >>>     st.write(f"You selected: {selected_folder}")
    """
    # Initialize session state
    if f'{key}_current_path' not in st.session_state:
        st.session_state[f'{key}_current_path'] = start_path or str(Path.home())
    if f'{key}_path_history' not in st.session_state:
        st.session_state[f'{key}_path_history'] = []
    if f'{key}_selected' not in st.session_state:
        st.session_state[f'{key}_selected'] = None
    if f'{key}_show_dialog' not in st.session_state:
        st.session_state[f'{key}_show_dialog'] = False

    # Display selected folder
    if st.session_state[f'{key}_selected']:
        st.success(f"📁 Selected folder: `{st.session_state[f'{key}_selected']}`")

    # Button to open folder browser
    if st.button("🗂️ Browse Folders", key=f"{key}_browse_btn"):
        st.session_state[f'{key}_show_dialog'] = True
        st.rerun()

    # Show dialog if flag is set
    if st.session_state[f'{key}_show_dialog']:
        _show_dir_picker_dialog(key)

    return st.session_state[f'{key}_selected']


def FilePicker(key="file_picker", start_path=None, file_extensions=None):
    """
    Display a file browser dialog for selecting files.

    Args:
        key (str): Unique key for the picker instance
        start_path (str, optional): Starting directory path. Defaults to user's home directory.
        file_extensions (list, optional): List of file extensions to filter (e.g., ['.txt', '.pdf'])

    Returns:
        str or None: Selected file path, or None if no selection made

    Example:
        >>> selected_file = FilePicker(key="my_file_picker", file_extensions=['.txt', '.pdf'])
        >>> if selected_file:
        >>>     st.write(f"You selected: {selected_file}")
    """
    # Initialize session state
    if f'{key}_current_path' not in st.session_state:
        st.session_state[f'{key}_current_path'] = start_path or str(Path.home())
    if f'{key}_path_history' not in st.session_state:
        st.session_state[f'{key}_path_history'] = []
    if f'{key}_selected' not in st.session_state:
        st.session_state[f'{key}_selected'] = None
    if f'{key}_show_dialog' not in st.session_state:
        st.session_state[f'{key}_show_dialog'] = False
    if f'{key}_file_extensions' not in st.session_state:
        st.session_state[f'{key}_file_extensions'] = file_extensions

    # Display selected file
    if st.session_state[f'{key}_selected']:
        st.success(f"📄 Selected file: `{st.session_state[f'{key}_selected']}`")

    # Button to open file browser
    if st.button("📂 Browse Files", key=f"{key}_browse_btn"):
        st.session_state[f'{key}_show_dialog'] = True
        st.rerun()

    # Show dialog if flag is set
    if st.session_state[f'{key}_show_dialog']:
        _show_file_picker_dialog(key)

    return st.session_state[f'{key}_selected']


@st.dialog("Select Folder", width="large")
def _show_dir_picker_dialog(key):
    """Internal function to display the folder picker dialog."""

    @st.fragment
    def folder_content():
        current = st.session_state[f'{key}_current_path']

        # Initialize text input state if needed
        if f'{key}_path_input_value' not in st.session_state:
            st.session_state[f'{key}_path_input_value'] = current

        # Update text input value when path changes
        if st.session_state[f'{key}_path_input_value'] != current:
            st.session_state[f'{key}_path_input_value'] = current
            if f'{key}_path_input_key' in st.session_state:
                st.session_state[f'{key}_path_input_key'] = current

        # Text input for direct path entry
        def on_path_change():
            new_path = st.session_state[f'{key}_path_input_key']
            if new_path != current and new_path.strip():
                if os.path.isdir(new_path):
                    st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
                    st.session_state[f'{key}_current_path'] = new_path
                    st.session_state[f'{key}_path_input_value'] = new_path

        st.text_input("Enter path:", value=current,
                      key=f'{key}_path_input_key', label_visibility="collapsed",
                      on_change=on_path_change)

        # Search input
        search_query = st.text_input("🔍 Search folders:", key=f"{key}_search_input",
                                     placeholder="Type to filter folders in current location...")

        # Get list of folders in current directory
        try:
            folders = [f for f in os.listdir(current)
                       if os.path.isdir(os.path.join(current, f))]
            folders.sort()

            # Filter folders based on search query
            if search_query:
                folders = [f for f in folders if search_query.lower() in f.lower()]
        except PermissionError:
            st.error("Permission denied to access this folder")
            folders = []

        # Up button to go to parent folder
        parent_path = str(Path(current).parent)
        is_at_root = parent_path == current

        if st.button("⬆️ Up (Parent Folder)", key=f"{key}_up_button",
                     use_container_width=True, disabled=is_at_root):
            st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
            st.session_state[f'{key}_current_path'] = parent_path
            st.rerun(scope="fragment")

        # Create a scrollable container for folders
        with st.container(height=450):
            if folders:
                st.write("**Click a folder to navigate:**")
                for folder in folders:
                    if st.button(f"📂 {folder}", key=f"{key}_folder_{folder}", use_container_width=True):
                        st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
                        st.session_state[f'{key}_current_path'] = os.path.join(current, folder)
                        st.rerun(scope="fragment")
            else:
                st.write("*No subfolders found*")

        # Action buttons
        st.divider()
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⬅️ Back", disabled=len(st.session_state[f'{key}_path_history']) == 0,
                        use_container_width=True, key=f"{key}_back_btn"):
                if st.session_state[f'{key}_path_history']:
                    st.session_state[f'{key}_current_path'] = st.session_state[f'{key}_path_history'].pop()
                    st.rerun(scope="fragment")

        with col2:
            if st.button("✅ Select", type="primary", use_container_width=True, key=f"{key}_select_btn"):
                st.session_state[f'{key}_selected'] = st.session_state[f'{key}_current_path']
                st.session_state[f'{key}_show_dialog'] = False
                st.rerun()

        with col3:
            if st.button("❌ Cancel", use_container_width=True, key=f"{key}_cancel_btn"):
                st.session_state[f'{key}_show_dialog'] = False
                st.rerun()

    folder_content()


@st.dialog("Select File", width="large")
def _show_file_picker_dialog(key):
    """Internal function to display the file picker dialog."""

    @st.fragment
    def file_content():
        current = st.session_state[f'{key}_current_path']
        file_extensions = st.session_state[f'{key}_file_extensions']

        # Initialize text input state if needed
        if f'{key}_path_input_value' not in st.session_state:
            st.session_state[f'{key}_path_input_value'] = current

        # Update text input value when path changes
        if st.session_state[f'{key}_path_input_value'] != current:
            st.session_state[f'{key}_path_input_value'] = current
            if f'{key}_path_input_key' in st.session_state:
                st.session_state[f'{key}_path_input_key'] = current

        # Text input for direct path entry
        def on_path_change():
            new_path = st.session_state[f'{key}_path_input_key']
            if new_path != current and new_path.strip():
                if os.path.isdir(new_path):
                    st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
                    st.session_state[f'{key}_current_path'] = new_path
                    st.session_state[f'{key}_path_input_value'] = new_path

        st.text_input("Enter path:", value=current,
                      key=f'{key}_path_input_key', label_visibility="collapsed",
                      on_change=on_path_change)

        # Search input
        search_query = st.text_input("🔍 Search:", key=f"{key}_search_input",
                                     placeholder="Type to filter files and folders...")

        # Get list of folders and files in current directory
        try:
            all_items = os.listdir(current)
            folders = [f for f in all_items if os.path.isdir(os.path.join(current, f))]
            files = [f for f in all_items if os.path.isfile(os.path.join(current, f))]

            # Filter by file extensions if provided
            if file_extensions:
                files = [f for f in files if any(f.endswith(ext) for ext in file_extensions)]

            folders.sort()
            files.sort()

            # Filter based on search query
            if search_query:
                folders = [f for f in folders if search_query.lower() in f.lower()]
                files = [f for f in files if search_query.lower() in f.lower()]
        except PermissionError:
            st.error("Permission denied to access this folder")
            folders = []
            files = []

        # Up button to go to parent folder
        parent_path = str(Path(current).parent)
        is_at_root = parent_path == current

        if st.button("⬆️ Up (Parent Folder)", key=f"{key}_up_button",
                     use_container_width=True, disabled=is_at_root):
            st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
            st.session_state[f'{key}_current_path'] = parent_path
            st.rerun(scope="fragment")

        # Create a scrollable container for folders and files
        with st.container(height=450):
            # Display folders
            if folders:
                st.write("**Folders:**")
                for folder in folders:
                    if st.button(f"📂 {folder}", key=f"{key}_folder_{folder}", use_container_width=True):
                        st.session_state[f'{key}_path_history'].append(st.session_state[f'{key}_current_path'])
                        st.session_state[f'{key}_current_path'] = os.path.join(current, folder)
                        st.rerun(scope="fragment")

            # Display files
            if files:
                st.write("**Files:**")
                for file in files:
                    if st.button(f"📄 {file}", key=f"{key}_file_{file}", use_container_width=True):
                        st.session_state[f'{key}_selected'] = os.path.join(current, file)
                        st.session_state[f'{key}_show_dialog'] = False
                        st.rerun()

            if not folders and not files:
                st.write("*No items found*")

        # Action buttons
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅️ Back", disabled=len(st.session_state[f'{key}_path_history']) == 0,
                        use_container_width=True, key=f"{key}_back_btn"):
                if st.session_state[f'{key}_path_history']:
                    st.session_state[f'{key}_current_path'] = st.session_state[f'{key}_path_history'].pop()
                    st.rerun(scope="fragment")

        with col2:
            if st.button("❌ Cancel", use_container_width=True, key=f"{key}_cancel_btn"):
                st.session_state[f'{key}_show_dialog'] = False
                st.rerun()

    file_content()