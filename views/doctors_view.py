import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from models.doctor import Doctor

import re
from theme import *

class DoctorsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.sort_reverse = False
        self.selected_doctor_id = None
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        self.main_font = ctk.CTkFont(family="Helvetica", size=14)
        self.bold_font = ctk.CTkFont(family="Helvetica", size=15, weight="bold")
        
        self.create_form_frame()
        self.create_table_frame()
        
    def create_form_frame(self):
        self.form_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        self.form_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        inner = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        inner.pack(expand=True, fill="both", padx=30, pady=30)
        inner.grid_columnconfigure(0, weight=1)
        inner.grid_columnconfigure(1, weight=1)
        
        lbl_title = ctk.CTkLabel(inner, text="Manage Doctor", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"), text_color=C_TEXT_PRIMARY)
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        input_args = {"fg_color": C_BG_BASE, "border_color": C_BORDER, "text_color": C_TEXT_PRIMARY, "placeholder_text_color": C_TEXT_MUTED, "font": self.main_font, "height": 40}
        
        self.entry_fname = ctk.CTkEntry(inner, placeholder_text="First Name", **input_args)
        self.entry_fname.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_lname = ctk.CTkEntry(inner, placeholder_text="Last Name", **input_args)
        self.entry_lname.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_spec = ctk.CTkEntry(inner, placeholder_text="Speciality", **input_args)
        self.entry_spec.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_phone = ctk.CTkEntry(inner, placeholder_text="Phone", **input_args)
        self.entry_phone.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_email = ctk.CTkEntry(inner, placeholder_text="Email", **input_args)
        self.entry_email.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.lbl_error = ctk.CTkLabel(inner, text="", text_color=C_ERROR, font=self.main_font)
        self.lbl_error.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.btn_save = ctk.CTkButton(inner, text="✅ Save", command=self.save_doctor, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_save.grid(row=7, column=0, padx=(0, 5), pady=10, sticky="ew")
        
        self.btn_clear = ctk.CTkButton(inner, text="🔄 Clear", command=self.clear_form, fg_color=C_BORDER, hover_color=C_BG_BASE, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_clear.grid(row=7, column=1, padx=(5, 0), pady=10, sticky="ew")
        
        self.btn_delete = ctk.CTkButton(inner, text="🗑 Delete Selected", command=self.delete_doctor, fg_color=C_ERROR, hover_color="#B91C1C", text_color="white", font=self.bold_font, height=40)
        self.btn_delete.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

    def create_table_frame(self):
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        self.table_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        top_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        
        self.entry_search = ctk.CTkEntry(top_bar, placeholder_text="Search doctors...", 
                                         fg_color=C_BG_BASE, border_color=C_BORDER, text_color=C_TEXT_PRIMARY, placeholder_text_color=C_TEXT_MUTED, font=self.main_font, height=40)
        self.entry_search.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.entry_search.bind("<KeyRelease>", self.on_search)
        
        self.btn_export = ctk.CTkButton(top_bar, text="⬇ Export CSV", command=self.export_csv, width=120, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, font=self.bold_font, height=40)
        self.btn_export.grid(row=0, column=1)


        columns = ("id", "first_name", "last_name", "speciality", "phone", "email")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        headings = ["ID", "First Name", "Last Name", "Speciality", "Phone", "Email"]
        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=100)
            
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(30, 0))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns", pady=(0, 30), padx=(0, 30))
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky="ew", padx=(30, 0), pady=(0, 30))
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for d in Doctor.get_all():
            self.tree.insert("", "end", values=(d['id'], d['first_name'], d['last_name'], d['speciality'], d['phone'], d['email']))
            
    def on_search(self, event):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.refresh_data()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for d in Doctor.search(keyword):
            self.tree.insert("", "end", values=(d['id'], d['first_name'], d['last_name'], d['speciality'], d['phone'], d['email']))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0])['values']
        self.selected_doctor_id = values[0]
        
        self.entry_fname.delete(0, 'end')
        self.entry_lname.delete(0, 'end')
        self.entry_spec.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        
        self.entry_fname.insert(0, values[1])
        self.entry_lname.insert(0, values[2])
        self.entry_spec.insert(0, values[3])
        self.entry_phone.insert(0, values[4])
        self.entry_email.insert(0, values[5] if values[5] != 'None' else '')
        
    def clear_form(self):
        self.selected_doctor_id = None
        self.entry_fname.delete(0, 'end')
        self.entry_lname.delete(0, 'end')
        self.entry_spec.delete(0, 'end')
        self.entry_phone.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.lbl_error.configure(text="")

    def save_doctor(self):
        fname = self.entry_fname.get().strip()
        lname = self.entry_lname.get().strip()
        spec = self.entry_spec.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        
        if not fname or not lname or not spec:
            self.lbl_error.configure(text="Required: First Name, Last Name, Speciality")
            return
            
        if email and not re.match(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,}$", email):
            self.lbl_error.configure(text="Invalid email format.")
            return
            
        if self.selected_doctor_id:
            success = Doctor.update(self.selected_doctor_id, fname, lname, spec, phone, email)
        else:
            success = Doctor.add(fname, lname, spec, phone, email)
            
        if success:
            self.clear_form()
            self.refresh_data()
        else:
            self.lbl_error.configure(text="Failed to save. Check DB or duplicates.")

    def delete_doctor(self):
        if not self.selected_doctor_id:
            messagebox.showwarning("Warning", "Please select a doctor to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete this doctor?"):
            Doctor.delete(self.selected_doctor_id)
            self.clear_form()
            self.refresh_data()
            
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "First Name", "Last Name", "Speciality", "Phone", "Email"])
                for child in self.tree.get_children():
                    writer.writerow(self.tree.item(child)["values"])
            messagebox.showinfo("Success", "Data exported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def sort_treeview(self, col):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try: items.sort(key=lambda x: float(x[0]), reverse=self.sort_reverse)
        except ValueError: items.sort(reverse=self.sort_reverse)
        for index, (_, k) in enumerate(items): self.tree.move(k, "", index)
        self.sort_reverse = not self.sort_reverse
        
        
        for c in self.tree["columns"]:
            original_text = self.tree.heading(c, "text").replace(" ▲", "").replace(" ▼", "")
            if c == col:
                original_text += " ▲" if self.sort_reverse else " ▼"
            self.tree.heading(c, text=original_text)
