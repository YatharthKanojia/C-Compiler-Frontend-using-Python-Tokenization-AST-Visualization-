INTRODUCTION : This project is a basic compiler frontend designed to perform lexical analysis and parse C++ source code into an Abstract Syntax Tree (AST) using Python. It supports a graphical interface where users can:
* Tokenize .cpp files
* View token output
* Generate and visualize the AST (text + graphical form)
Built with Lark, Tkinter, and NetworkX, the tool is especially useful for learning how real-world compilers process source code at the lexical and syntactic level.

FEATURES : 
* C++ Lexer (Tokenizer): Extracts keywords, identifiers, literals, and operators.
*  Parser & AST Generator: Parses code and creates a structured Abstract Syntax Tree.
*  AST Visualization: Renders the AST as a clean, hierarchical tree using NetworkX and Matplotlib.
*  Graphical User Interface (GUI): Easy-to-use interface built with Tkinter for interactive use.
*  Error Handling: Handles file input and parsing errors gracefully.

PREREQUISTIES:
1. System Requirements
* Operating System: Windows, macOS, or Linux
* Python Version: Python 3.8 or above
  
2.Python Libraries
You need to install the following Python libraries:
        => pip install lark-parser networkx matplotlib
If you're using the GUI (Tkinter), it typically comes pre-installed with Python. If not, install it manually:
Tkinter is usually included with Python. If not, re-install Python from the official site and ensure “tcl/tk and IDLE” is selected during installation.

3. Optional Tools (For Developers)
* An IDE or Code Editor (e.g., VS Code, PyCharm)
* Graphical Output Support (for matplotlib.pyplot)
  
FILES:
1. compiler_core.py :
* Core logic of the compiler frontend:
* Defines grammar rules using the Lark library for tokenization.
* Implements custom AST node classes and transformation logic.
* Provides tokenization, AST generation, and tree plotting functions.
* Includes a function to display the AST in a tree layout using NetworkX and Matplotlib.

2. compiler_ui.py (or main script with Tkinter UI)
* Provides a Graphical User Interface using Tkinter:
* Allows users to choose a .cpp file via a file dialog.
* Displays the list of generated tokens in a scrollable text area.
* Shows the AST in text form and as a graphical plot.
* Calls functions from compiler_core.py for processing.

3. abc.cpp
* Sample C++ file used to demonstrate the functionality of tokenization and AST generation.
* You can replace this with any .cpp file to test the tool.

