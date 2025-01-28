import streamlit as st
import json
import base64
import os
import re
from io import BytesIO
import zipfile

# Set page configuration
st.set_page_config(
    page_title="Notebook Converter",
    page_icon="📓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .upload-section {
        border: 2px dashed #cccccc;
        border-radius: 5px;
        padding: 2rem;
        margin: 1rem 0;
    }
    .stat-box {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def get_file_size(file):
    """Get file size in appropriate units."""
    size_bytes = len(file.getvalue())
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} GB"

def extract_notebook_content(notebook_file):
    """Extract code, outputs, and images from a notebook file."""
    notebook_data = json.load(notebook_file)
    
    code_str = ""
    outputs_str = ""
    images_list = []
    image_counter = 1
    code_cells_count = 0
    markdown_cells_count = 0
    
    for cell in notebook_data.get("cells", []):
        cell_type = cell.get("cell_type")
        if cell_type == "code":
            code_cells_count += 1
            # Extract code
            code_str += "".join(cell.get("source", [])) + "\n\n"
            
            # Process outputs
            for out in cell.get("outputs", []):
                output_type = out.get("output_type", "")
                
                if output_type == "stream":
                    outputs_str += "".join(out.get("text", [])) + "\n"
                
                elif output_type in ["display_data", "execute_result"]:
                    data = out.get("data", {})
                    
                    if "text/plain" in data:
                        outputs_str += "".join(data["text/plain"]) + "\n"
                    
                    if "image/png" in data:
                        image_bytes = base64.b64decode(data["image/png"])
                        img_name = f"image_{image_counter}.png"
                        images_list.append((img_name, image_bytes))
                        outputs_str += f"[Image saved: {img_name}]\n"
                        image_counter += 1
        elif cell_type == "markdown":
            markdown_cells_count += 1
    
    stats = {
        "code_cells": code_cells_count,
        "markdown_cells": markdown_cells_count,
        "images": len(images_list),
        "code_lines": len(code_str.split("\n"))
    }
    
    return code_str, outputs_str, images_list, stats

def create_download_zip(processed_files):
    """Create a ZIP file containing all processed notebooks."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for base_name, content in processed_files.items():
            # Add Python file
            zip_file.writestr(f"{base_name}/{base_name}.py", content["code"])
            
            # Add outputs file if it exists
            if content.get("outputs"):
                zip_file.writestr(f"{base_name}/{base_name}_outputs.txt", content["outputs"])
            
            # Add images if they exist
            for img_name, img_content in content.get("images", []):
                zip_file.writestr(f"{base_name}/{base_name}_{img_name}", img_content)
    
    return zip_buffer

def main():
    # Initialize session state for processed files
    if 'processed_files' not in st.session_state:
        st.session_state.processed_files = {}
    if 'total_stats' not in st.session_state:
        st.session_state.total_stats = {
            "total_code_cells": 0,
            "total_markdown_cells": 0,
            "total_images": 0,
            "total_code_lines": 0,
            "total_size": 0
        }
    
    # Header
    st.title("📓 Notebook Converter")
    st.markdown("Transform your Jupyter Notebooks into organized code packages instantly")
    
    # Settings sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        include_outputs = st.toggle("Include outputs", value=True)
        include_images = st.toggle("Include images", value=True)
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool helps you convert Jupyter Notebooks (.ipynb) into:
        - Clean Python scripts
        - Organized output files
        - Extracted images
        """)

    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📤 Upload Notebooks")
        uploaded_files = st.file_uploader(
            "Drop your .ipynb files here",
            type=["ipynb"],
            accept_multiple_files=True,
            help="You can upload multiple notebooks at once"
        )

        if uploaded_files:
            if st.button("🚀 Process Files", use_container_width=True):
                with st.spinner("Processing notebooks..."):
                    # Reset total stats
                    st.session_state.total_stats = {
                        "total_code_cells": 0,
                        "total_markdown_cells": 0,
                        "total_images": 0,
                        "total_code_lines": 0,
                        "total_size": 0
                    }
                    
                    # Process each file
                    for uploaded_file in uploaded_files:
                        base_name = re.sub(r"\.ipynb$", "", uploaded_file.name, flags=re.IGNORECASE)
                        code_str, outputs_str, images_list, stats = extract_notebook_content(uploaded_file)
                        
                        # Update session state
                        st.session_state.processed_files[base_name] = {
                            "code": code_str,
                            "outputs": outputs_str if include_outputs else "",
                            "images": images_list if include_images else [],
                            "stats": stats,
                            "size": get_file_size(uploaded_file)
                        }
                        
                        # Update total stats
                        st.session_state.total_stats["total_code_cells"] += stats["code_cells"]
                        st.session_state.total_stats["total_markdown_cells"] += stats["markdown_cells"]
                        st.session_state.total_stats["total_images"] += stats["images"]
                        st.session_state.total_stats["total_code_lines"] += stats["code_lines"]
                        st.session_state.total_stats["total_size"] += len(uploaded_file.getvalue())
                    
                    st.success("✅ All notebooks processed successfully!")

            # Download all files button
            if st.session_state.processed_files:
                zip_buffer = create_download_zip(st.session_state.processed_files)
                st.download_button(
                    label="📦 Download All Processed Files",
                    data=zip_buffer.getvalue(),
                    file_name="all_notebooks_package.zip",
                    mime="application/zip",
                    use_container_width=True
                )

    with col2:
        if st.session_state.processed_files:
            st.markdown("### 📊 Statistics")
            
            # Overall stats
            total_size_str = get_file_size(BytesIO(b'0' * st.session_state.total_stats["total_size"]))
            st.metric("Total Files", len(st.session_state.processed_files))
            st.metric("Total Size", total_size_str)
            
            # Detailed stats
            st.markdown("#### Detailed Statistics")
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Code Cells", st.session_state.total_stats["total_code_cells"])
                st.metric("Code Lines", st.session_state.total_stats["total_code_lines"])
            with col_b:
                st.metric("Markdown Cells", st.session_state.total_stats["total_markdown_cells"])
                st.metric("Images", st.session_state.total_stats["total_images"])
            
            # Individual file stats
            st.markdown("#### Files Breakdown")
            for base_name, content in st.session_state.processed_files.items():
                with st.expander(f"📔 {base_name}"):
                    st.write(f"Size: {content['size']}")
                    st.write(f"Code cells: {content['stats']['code_cells']}")
                    st.write(f"Markdown cells: {content['stats']['markdown_cells']}")
                    st.write(f"Images: {content['stats']['images']}")
                    st.write(f"Lines of code: {content['stats']['code_lines']}")

if __name__ == "__main__":
    main()