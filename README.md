# Notebook Converter Pro

Convert Jupyter Notebooks into organized Python packages with just a few clicks! 

## 🌐 Live Application

Try it now at: [https://notebook-converter.streamlit.app/](https://notebook-converter.streamlit.app/)

## ✨ Features

- Convert multiple `.ipynb` files simultaneously
- Extract code into clean Python scripts
- Preserve cell outputs in organized text files
- Save generated images from notebook execution
- Get detailed statistics about your notebooks
- Download everything in a structured ZIP package

## 📦 Output Structure

For each processed notebook, you'll receive:
- `<notebook_name>.py` - Consolidated Python code
- `<notebook_name>_outputs.txt` - Cell outputs and execution results
- `<notebook_name>_image_1.png`, etc. - Generated images (if any)

## 🛠️ Local Development

### Prerequisites
- Python 3.7+
- Streamlit

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/notebook-converter.git
cd notebook-converter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## 📝 Notes

- The code extraction concatenates all cells into a single Python file
- IPython magic commands (e.g., `%matplotlib inline`) are included as-is
- HTML and JavaScript outputs from cells are not processed
- All files are processed in-memory for the web version

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](link-to-issues).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.