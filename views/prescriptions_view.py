import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from models.prescription import Prescription
from models.appointment import Appointment
from models.patient import Patient

from theme import *

class PrescriptionsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.sort_reverse = False
        self.selected_prescription_id = None
        self.appointments_map = {}
        
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
        
        lbl_title = ctk.CTkLabel(inner, text="Manage Prescription", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"), text_color=C_TEXT_PRIMARY)
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        input_args = {"fg_color": C_BG_BASE, "border_color": C_BORDER, "text_color": C_TEXT_PRIMARY, "placeholder_text_color": C_TEXT_MUTED, "font": self.main_font, "height": 40}
        combo_args = {"fg_color": C_BG_BASE, "border_color": C_BORDER, "text_color": C_TEXT_PRIMARY, "dropdown_fg_color": C_BG_CARD, "dropdown_text_color": C_TEXT_PRIMARY, "button_color": C_BORDER, "button_hover_color": C_BG_BASE, "font": self.main_font, "height": 40}
        
        self.lbl_appointment = ctk.CTkLabel(inner, text="Appointment:", text_color=C_TEXT_PRIMARY, font=self.main_font)
        self.lbl_appointment.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
        self.combo_appointment = ctk.CTkComboBox(inner, values=[], **combo_args)
        self.combo_appointment.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        self.entry_diagnosis = ctk.CTkEntry(inner, placeholder_text="Diagnosis", **input_args)
        self.entry_diagnosis.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_medication = ctk.CTkEntry(inner, placeholder_text="Medication", **input_args)
        self.entry_medication.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.lbl_notes = ctk.CTkLabel(inner, text="Notes:", text_color=C_TEXT_PRIMARY, font=self.main_font)
        self.lbl_notes.grid(row=5, column=0, columnspan=2, sticky="w", pady=(5, 0))
        self.text_notes = ctk.CTkTextbox(inner, height=100, fg_color=C_BG_BASE, border_color=C_BORDER, border_width=1, text_color=C_TEXT_PRIMARY, font=self.main_font)
        self.text_notes.grid(row=6, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        self.lbl_error = ctk.CTkLabel(inner, text="", text_color=C_ERROR, font=self.main_font)
        self.lbl_error.grid(row=7, column=0, columnspan=2, pady=5)
        
        self.btn_save = ctk.CTkButton(inner, text="✅ Save", command=self.save_prescription, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_save.grid(row=8, column=0, padx=(0, 5), pady=10, sticky="ew")
        
        self.btn_clear = ctk.CTkButton(inner, text="🔄 Clear", command=self.clear_form, fg_color=C_BORDER, hover_color=C_BG_BASE, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_clear.grid(row=8, column=1, padx=(5, 0), pady=10, sticky="ew")
        
        self.btn_delete = ctk.CTkButton(inner, text="🗑 Delete Selected", command=self.delete_prescription, fg_color=C_ERROR, hover_color="#B91C1C", text_color="white", font=self.bold_font, height=40)
        self.btn_delete.grid(row=9, column=0, columnspan=2, pady=10, sticky="ew")

    def create_table_frame(self):
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        self.table_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        top_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        
        self.entry_search = ctk.CTkEntry(top_bar, placeholder_text="Search prescriptions...", 
                                         fg_color=C_BG_BASE, border_color=C_BORDER, text_color=C_TEXT_PRIMARY, placeholder_text_color=C_TEXT_MUTED, font=self.main_font, height=40)
        self.entry_search.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.entry_search.bind("<KeyRelease>", self.on_search)
        
        self.btn_export = ctk.CTkButton(top_bar, text="⬇ Export CSV", command=self.export_csv, width=120, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, font=self.bold_font, height=40)
        self.btn_export.grid(row=0, column=1)


        columns = ("id", "patient", "date", "diagnosis", "medication", "notes", "appid")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        headings = ["ID", "Patient", "Date", "Diagnosis", "Medication", "Notes", "AppID"]
        widths = [50, 150, 100, 150, 100, 200, 0]
        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=w, stretch=(w>0), minwidth=w if w>0 else 0)
            
        self.tree.column("appid", width=0, stretch=False)
            
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(30, 0))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns", pady=(0, 30), padx=(0, 30))
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky="ew", padx=(30, 0), pady=(0, 30))
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def load_dropdowns(self):
        appointments = Appointment.get_all()
        self.appointments_map = {f"{a['id']} - {a['patient_name']} ({a['date']})": a['id'] for a in appointments}
        app_list = list(self.appointments_map.keys())
        self.combo_appointment.configure(values=app_list)
        if app_list: self.combo_appointment.set(app_list[0])
        else: self.combo_appointment.set("")

    def refresh_data(self):
        self.load_dropdowns()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in Prescription.get_all():
            self.tree.insert("", "end", values=(p['id'], p['patient_name'], p['appointment_date'], p['diagnosis'], p['medication'], p['notes'], p['appointment_id']))
            
    def on_search(self, event):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.refresh_data()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in Prescription.search(keyword):
            self.tree.insert("", "end", values=(p['id'], p['patient_name'], p['appointment_date'], p['diagnosis'], p['medication'], p['notes'], p['appointment_id']))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0])['values']
        self.selected_prescription_id = values[0]
        
        app_val = f"{values[6]} - {values[1]} ({values[2]})"
        if app_val in self.appointments_map:
            self.combo_appointment.set(app_val)
            
        self.entry_diagnosis.delete(0, 'end')
        self.entry_medication.delete(0, 'end')
        self.text_notes.delete('1.0', 'end')
        
        self.entry_diagnosis.insert(0, values[3])
        self.entry_medication.insert(0, values[4])
        self.text_notes.insert('1.0', values[5] if values[5] != 'None' else '')
        
    def clear_form(self):
        self.selected_prescription_id = None
        self.entry_diagnosis.delete(0, 'end')
        self.entry_medication.delete(0, 'end')
        self.text_notes.delete('1.0', 'end')
        if self.appointments_map: self.combo_appointment.set(list(self.appointments_map.keys())[0])
        self.lbl_error.configure(text="")

    def save_prescription(self):
        app_key = self.combo_appointment.get()
        diagnosis = self.entry_diagnosis.get().strip()
        medication = self.entry_medication.get().strip()
        notes = self.text_notes.get('1.0', 'end-1c').strip()
        
        if not app_key or not diagnosis or not medication:
            self.lbl_error.configure(text="Required: Appointment, Diagnosis, Medication")
            return
            
        app_id = self.appointments_map.get(app_key)
        
        if self.selected_prescription_id:
            success = Prescription.update(self.selected_prescription_id, app_id, diagnosis, medication, notes)
        else:
            success = Prescription.add(app_id, diagnosis, medication, notes)
            
        if success:
            self.clear_form()
            self.refresh_data()
        else:
            self.lbl_error.configure(text="Failed to save. Check DB connection.")

    def delete_prescription(self):
        if not self.selected_prescription_id:
            messagebox.showwarning("Warning", "Please select a prescription to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete this prescription?"):
            Prescription.delete(self.selected_prescription_id)
            self.clear_form()
            self.refresh_data()
            
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Patient", "Date", "Diagnosis", "Medication", "Notes"])
                for child in self.tree.get_children():
                    vals = self.tree.item(child)["values"]
                    writer.writerow(vals[:6])
            messagebox.showinfo("Success", "Data exported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def sort_treeview(self, col):
        if col == "appid": return
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try: items.sort(key=lambda x: float(x[0]), reverse=self.sort_reverse)
        except ValueError: items.sort(reverse=self.sort_reverse)
        for index, (_, k) in enumerate(items): self.tree.move(k, "", index)
        self.sort_reverse = not self.sort_reverse
        
        for c in self.tree["columns"]:
            if c == "appid": continue
            original_text = self.tree.heading(c, "text").replace(" ▲", "").replace(" ▼", "")
            if c == col:
                original_text += " ▲" if self.sort_reverse else " ▼"
            self.tree.heading(c, text=original_text)
