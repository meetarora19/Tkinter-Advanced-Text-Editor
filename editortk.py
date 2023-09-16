import tkinter as tk
from tkinter import filedialog, messagebox
import tkinter.font as tkfont
import tkinter.colorchooser as tkcolor

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        self.textarea = tk.Text(root, undo=True)
        self.textarea.pack(expand=True, fill="both")

        self.zoom_scale = tk.Scale(root, from_=10, to=400, orient=tk.HORIZONTAL, command=self.change_zoom)
        self.zoom_scale.set(100)

        self.zoom_var = tk.StringVar()
        self.zoom_var.set("100%")

        self.dark_mode = False

        self.font_size_var = tk.StringVar()
        self.font_size_var.set("12")

        self.create_menu()

        self.textarea.bind("<Control-plus>", self.zoom_in)
        self.textarea.bind("<Control-minus>", self.zoom_out)
        self.textarea.bind("<Control-0>", self.reset_zoom)

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_editor)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.textarea.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.textarea.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Font", command=self.change_font)
        format_menu.add_command(label="Text Color", command=self.change_text_color)
        format_menu.add_command(label="Background Color", command=self.change_bg_color)
        format_menu.add_separator()
        font_size_menu = tk.Menu(format_menu, tearoff=0)
        font_size_menu.add_radiobutton(label="10", variable=self.font_size_var, value="10", command=self.change_font_size)
        font_size_menu.add_radiobutton(label="12", variable=self.font_size_var, value="12", command=self.change_font_size)
        font_size_menu.add_radiobutton(label="14", variable=self.font_size_var, value="14", command=self.change_font_size)
        font_size_menu.add_separator()
        font_size_menu.add_command(label="Custom Size", command=self.set_custom_font_size)
        format_menu.add_cascade(label="Font Size", menu=font_size_menu)
        menubar.add_cascade(label="Format", menu=format_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_separator()
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Ctrl+0")
        self.zoom_label = view_menu.add_command(label=self.zoom_var.get())
        menubar.add_cascade(label="View", menu=view_menu)

        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)
        menubar.add_cascade(label="Options", menu=options_menu)

        self.root.config(menu=menubar)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        bg_color = "#000000" if self.dark_mode else "#FFFFFF"
        text_color = "#FFFFFF" if self.dark_mode else "#000000"
        cursor_color = "white" if self.dark_mode else "black"
        self.textarea.configure(bg=bg_color, fg=text_color, insertbackground=cursor_color)

    def change_zoom(self, value):
        current_zoom = int(value)
        self.zoom_var.set(f"Zoom Scale: {current_zoom}%")
        current_font = tkfont.Font(font=self.textarea["font"])
        new_size = current_font.actual()['size'] * current_zoom // 100
        self.textarea.configure(font=(current_font.actual()['family'], new_size))

    def zoom_in(self, event=None):
        current_zoom = int(self.zoom_scale.get())
        if current_zoom < 400:
            current_zoom += 10
            self.zoom_scale.set(current_zoom)
            self.change_zoom(current_zoom)

    def zoom_out(self, event=None):
        current_zoom = int(self.zoom_scale.get())
        if current_zoom > 10:
            current_zoom -= 10
            self.zoom_scale.set(current_zoom)
            self.change_zoom(current_zoom)

    def reset_zoom(self, event=None):
        self.zoom_scale.set(100)
        self.change_zoom(100)

    def change_font_size(self):
        current_size = self.font_size_var.get()
        self.textarea.configure(font=(self.textarea["font"].split()[0], current_size))

    def set_custom_font_size(self):
        custom_size = tk.simpledialog.askinteger("Custom Font Size", "Enter the custom font size:")
        if custom_size is not None:
            self.font_size_var.set(str(custom_size))
            self.change_font_size()

    def new_file(self):
        if self.confirm_discard_changes():
            self.textarea.delete(1.0, tk.END)
            self.root.title("Text Editor")

    def open_file(self):
        if self.confirm_discard_changes():
            file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
            if file_path:
                try:
                    with open(file_path, "r") as file:
                        content = file.read()
                    self.textarea.delete(1.0, tk.END)
                    self.textarea.insert(tk.END, content)
                    self.root.title(f"Text Editor - {file_path}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def save_file(self):
        file_path = self.root.title()[len("Text Editor - "):]
        if file_path == "Text Editor" or not file_path:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
            if not file_path:
                return
        content = self.textarea.get(1.0, tk.END)
        try:
            with open(file_path, "w") as file:
                file.write(content)
            self.root.title(f"Text Editor - {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = self.textarea.get(1.0, tk.END)
            try:
                with open(file_path, "w") as file:
                    file.write(content)
                self.root.title(f"Text Editor - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def exit_editor(self):
        if self.confirm_discard_changes():
            self.root.quit()

    def confirm_discard_changes(self):
        if self.textarea.edit_modified():
            answer = messagebox.askyesnocancel("Confirm", "Do you want to save changes to the current file?")
            if answer is None:
                return False
            elif answer:
                self.save_file()
        return True

    def cut(self):
        self.textarea.event_generate("<<Cut>>")

    def copy(self):
        self.textarea.event_generate("<<Copy>>")

    def paste(self):
        self.textarea.event_generate("<<Paste>>")

    def select_all(self):
        self.textarea.tag_add(tk.SEL, 1.0, tk.END)
        self.textarea.mark_set(tk.INSERT, 1.0)
        self.textarea.see(tk.INSERT)
        return "break"
    
    def change_font_size(self, event=None):
        try:
            font_size = int(self.font_size_var.get())
            if font_size > 0:
                font = tkfont.Font(font=self.textarea["font"])
                self.textarea.configure(font=(font.actual("family"), font_size))
        except ValueError:
            messagebox.showerror("Error", "Invalid font size.")

    def change_font(self):
        current_font = tkfont.Font(font=self.textarea["font"])
        font_family = current_font.actual("family")
        font_size = current_font.actual("size")
        new_font = filedialog.askopenfilename(filetypes=[("Font Files", "*.ttf")])
        if new_font:
            try:
                new_font = tkfont.Font(family=new_font, size=font_size)
                self.textarea.configure(font=new_font)
            except tk.TclError:
                messagebox.showerror("Error", "Invalid font file.")

    def change_text_color(self):
        color = tkcolor.askcolor(parent=self.root)
        if color:
            self.textarea.config(fg=color[1])

    def change_bg_color(self):
        color = tkcolor.askcolor(parent=self.root)
        if color:
            self.textarea.config(bg=color[1])

root = tk.Tk()
text_editor = TextEditor(root)
root.mainloop()
