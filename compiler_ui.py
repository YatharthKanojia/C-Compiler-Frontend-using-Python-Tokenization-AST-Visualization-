import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from compiler_core import tokenize_file, tokenize_and_parse, print_ast_as_tree, plot_ast

class CompilerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Compiler Frontend")
        self.root.geometry("900x700")

        self.filename = None

        # Buttons
        tk.Button(root, text="Choose C++ File", command=self.choose_file).pack(pady=10)
        tk.Button(root, text="Tokenize", command=self.tokenize_code).pack(pady=5)
        tk.Button(root, text="Generate AST", command=self.generate_ast).pack(pady=5)

        # Text areas
        self.token_output = scrolledtext.ScrolledText(root, height=15, width=110)
        self.token_output.pack(pady=10)

        self.ast_output = scrolledtext.ScrolledText(root, height=20, width=110)
        self.ast_output.pack(pady=10)

    def choose_file(self):
        self.filename = filedialog.askopenfilename(filetypes=[("C++ Files", "*.cpp")])
        if self.filename:
            messagebox.showinfo("File Selected", f"Selected file:\n{self.filename}")
        else:
            messagebox.showwarning("No File", "No file selected.")

    def tokenize_code(self):
        if not self.filename:
            messagebox.showerror("Error", "Please select a file first.")
            return

        tokens = tokenize_file(self.filename)
        if tokens:
            self.token_output.delete(1.0, tk.END)
            self.token_output.insert(tk.END, "Tokens:\n")
            for token_type, value in tokens:
                self.token_output.insert(tk.END, f"Type: {token_type:12} Value: {value}\n")
        else:
            self.token_output.delete(1.0, tk.END)
            self.token_output.insert(tk.END, "Error tokenizing the file.")

    def generate_ast(self):
        if not self.filename:
            messagebox.showerror("Error", "Please select a file first.")
            return

        ast = tokenize_and_parse(self.filename)
        if ast:
            self.ast_output.delete(1.0, tk.END)
            self.ast_output.insert(tk.END, "Abstract Syntax Tree (Text View):\n")
            self._print_ast_to_output(ast)
            plot_ast(ast)  # This shows the AST image
        else:
            self.ast_output.delete(1.0, tk.END)
            self.ast_output.insert(tk.END, "Error generating AST.")

    def _print_ast_to_output(self, ast):
        import io
        import sys
        buffer = io.StringIO()
        sys.stdout = buffer
        print_ast_as_tree(ast)
        sys.stdout = sys.__stdout__
        self.ast_output.insert(tk.END, buffer.getvalue())
        buffer.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerUI(root)
    root.mainloop()
