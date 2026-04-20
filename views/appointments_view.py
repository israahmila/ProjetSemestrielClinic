import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import csv
from models.appointment import Appointment
from models.patient import Patient
from models.doctor import Doctor
import re

from theme import *

class AppointmentsView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        self.sort_reverse = False
        self.selected_appointment_id = None
        self.patients_map = {} 
        self.doctors_map = {} 
        
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
        
        lbl_title = ctk.CTkLabel(inner, text="Manage Appointment", font=ctk.CTkFont(family="Helvetica", size=22, weight="bold"), text_color=C_TEXT_PRIMARY)
        lbl_title.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        input_args = {"fg_color": C_BG_BASE, "border_color": C_BORDER, "text_color": C_TEXT_PRIMARY, "placeholder_text_color": C_TEXT_MUTED, "font": self.main_font, "height": 40}
        combo_args = {"fg_color": C_BG_BASE, "border_color": C_BORDER, "text_color": C_TEXT_PRIMARY, "dropdown_fg_color": C_BG_CARD, "dropdown_text_color": C_TEXT_PRIMARY, "button_color": C_BORDER, "button_hover_color": C_BG_BASE, "font": self.main_font, "height": 40}
        
        self.lbl_patient = ctk.CTkLabel(inner, text="Patient:", text_color=C_TEXT_PRIMARY, font=self.main_font)
        self.lbl_patient.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 0))
        self.combo_patient = ctk.CTkComboBox(inner, values=[], **combo_args)
        self.combo_patient.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        self.lbl_doctor = ctk.CTkLabel(inner, text="Doctor:", text_color=C_TEXT_PRIMARY, font=self.main_font)
        self.lbl_doctor.grid(row=3, column=0, columnspan=2, sticky="w", pady=(5, 0))
        self.combo_doctor = ctk.CTkComboBox(inner, values=[], **combo_args)
        self.combo_doctor.grid(row=4, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        
        self.entry_date = ctk.CTkEntry(inner, placeholder_text="Date (YYYY-MM-DD)", **input_args)
        self.entry_date.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.entry_time = ctk.CTkEntry(inner, placeholder_text="Time (HH:MM:SS)", **input_args)
        self.entry_time.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.combo_status = ctk.CTkComboBox(inner, values=["scheduled", "done", "cancelled"], **combo_args)
        self.combo_status.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        
        self.lbl_error = ctk.CTkLabel(inner, text="", text_color=C_ERROR, font=self.main_font)
        self.lbl_error.grid(row=8, column=0, columnspan=2, pady=5)
        
        self.btn_save = ctk.CTkButton(inner, text="✅ Save", command=self.save_appointment, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_save.grid(row=9, column=0, padx=(0, 5), pady=10, sticky="ew")
        
        self.btn_clear = ctk.CTkButton(inner, text="🔄 Clear", command=self.clear_form, fg_color=C_BORDER, hover_color=C_BG_BASE, text_color=C_TEXT_PRIMARY, font=self.bold_font, height=40)
        self.btn_clear.grid(row=9, column=1, padx=(5, 0), pady=10, sticky="ew")
        
        self.btn_delete = ctk.CTkButton(inner, text="🗑 Delete Selected", command=self.delete_appointment, fg_color=C_ERROR, hover_color="#B91C1C", text_color="white", font=self.bold_font, height=40)
        self.btn_delete.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")

    def create_table_frame(self):
        self.table_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        self.table_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="nsew")
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        top_bar = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        top_bar.grid_columnconfigure(0, weight=1)
        
        self.entry_search = ctk.CTkEntry(top_bar, placeholder_text="Search appointments...", 
                                         fg_color=C_BG_BASE, border_color=C_BORDER, text_color=C_TEXT_PRIMARY, placeholder_text_color=C_TEXT_MUTED, font=self.main_font, height=40)
        self.entry_search.grid(row=0, column=0, padx=(0, 15), sticky="ew")
        self.entry_search.bind("<KeyRelease>", self.on_search)
        
        self.btn_export = ctk.CTkButton(top_bar, text="⬇ Export CSV", command=self.export_csv, width=120, fg_color=C_PRIMARY, hover_color=C_PRIMARY_HOVER, font=self.bold_font, height=40)
        self.btn_export.grid(row=0, column=1)


        columns = ("id", "patient", "doctor", "date", "time", "status", "pid", "did")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        headings = ["ID", "Patient", "Doctor", "Date", "Time", "Status", "PID", "DID"]
        widths = [50, 150, 150, 100, 100, 100, 0, 0]
        for col, head, w in zip(columns, headings, widths):
            self.tree.heading(col, text=head, command=lambda c=col: self.sort_treeview(c))
            self.tree.column(col, width=w, stretch=(w>0), minwidth=w if w>0 else 0)
        
        self.tree.column("pid", width=0, stretch=False)
        self.tree.column("did", width=0, stretch=False)
            
        self.tree.grid(row=1, column=0, sticky="nsew", padx=(30, 0))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        vsb = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=1, sticky="ns", pady=(0, 30), padx=(0, 30))
        hsb = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, sticky="ew", padx=(30, 0), pady=(0, 30))
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    def load_dropdowns(self):
        patients = Patient.get_all()
        doctors = Doctor.get_all()
        
        self.patients_map = {f"{p['id']} - {p['first_name']} {p['last_name']}": p['id'] for p in patients}
        self.doctors_map = {f"{d['id']} - {d['first_name']} {d['last_name']}": d['id'] for d in doctors}
        
        pat_list = list(self.patients_map.keys())
        doc_list = list(self.doctors_map.keys())
        
        self.combo_patient.configure(values=pat_list)
        self.combo_doctor.configure(values=doc_list)
        
        if pat_list: self.combo_patient.set(pat_list[0])
        else: self.combo_patient.set("")
        
        if doc_list: self.combo_doctor.set(doc_list[0])
        else: self.combo_doctor.set("")

    def refresh_data(self):
        self.load_dropdowns()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for a in Appointment.get_all():
            self.tree.insert("", "end", values=(a['id'], a['patient_name'], a['doctor_name'], a['date'], a['time'], a['status'], a['patient_id'], a['doctor_id']))
            
    def on_search(self, event):
        keyword = self.entry_search.get().strip()
        if not keyword:
            self.refresh_data()
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for a in Appointment.search(keyword):
            self.tree.insert("", "end", values=(a['id'], a['patient_name'], a['doctor_name'], a['date'], a['time'], a['status'], a['patient_id'], a['doctor_id']))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected[0])['values']
        self.selected_appointment_id = values[0]
        
        pat_val = f"{values[6]} - {values[1]}"
        doc_val = f"{values[7]} - {values[2]}"
        
        if pat_val in self.patients_map: self.combo_patient.set(pat_val)
        if doc_val in self.doctors_map: self.combo_doctor.set(doc_val)
        
        self.entry_date.delete(0, 'end')
        self.entry_time.delete(0, 'end')
        
        self.entry_date.insert(0, values[3])
        self.entry_time.insert(0, values[4])
        self.combo_status.set(values[5])
        
    def clear_form(self):
        self.selected_appointment_id = None
        self.entry_date.delete(0, 'end')
        self.entry_time.delete(0, 'end')
        self.combo_status.set("scheduled")
        if self.patients_map: self.combo_patient.set(list(self.patients_map.keys())[0])
        if self.doctors_map: self.combo_doctor.set(list(self.doctors_map.keys())[0])
        self.lbl_error.configure(text="")

    def save_appointment(self):
        pat_key = self.combo_patient.get()
        doc_key = self.combo_doctor.get()
        date = self.entry_date.get().strip()
        time = self.entry_time.get().strip()
        status = self.combo_status.get()
        
        if not pat_key or not doc_key or not date or not time:
            self.lbl_error.configure(text="Required: Patient, Doctor, Date, Time")
            return
            
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
            self.lbl_error.configure(text="Date must be YYYY-MM-DD")
            return
            
        if not re.match(r"^\d{2}:\d{2}(:\d{2})?$", time):
            self.lbl_error.configure(text="Time must be HH:MM:SS or HH:MM")
            return
            
        pat_id = self.patients_map.get(pat_key)
        doc_id = self.doctors_map.get(doc_key)
        
        if self.selected_appointment_id:
            success = Appointment.update(self.selected_appointment_id, pat_id, doc_id, date, time, status)
        else:
            success = Appointment.add(pat_id, doc_id, date, time, status)
            
        if success:
            self.clear_form()
            self.refresh_data()
        else:
            self.lbl_error.configure(text="Failed to save. Check DB connection.")

    def delete_appointment(self):
        if not self.selected_appointment_id:
            messagebox.showwarning("Warning", "Please select an appointment to delete.")
            return
        if messagebox.askyesno("Confirm", "Delete this appointment?"):
            Appointment.delete(self.selected_appointment_id)
            self.clear_form()
            self.refresh_data()
            
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path: return
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Patient", "Doctor", "Date", "Time", "Status"])
                for child in self.tree.get_children():
                    vals = self.tree.item(child)["values"]
                    writer.writerow(vals[:6])
            messagebox.showinfo("Success", "Data exported.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def sort_treeview(self, col):
        if col in ("pid", "did"): return
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        try: items.sort(key=lambda x: float(x[0]), reverse=self.sort_reverse)
        except ValueError: items.sort(reverse=self.sort_reverse)
        for index, (_, k) in enumerate(items): self.tree.move(k, "", index)
        self.sort_reverse = not self.sort_reverse
        
        for c in self.tree["columns"]:
            if c in ("pid", "did"): continue
            original_text = self.tree.heading(c, "text").replace(" ▲", "").replace(" ▼", "")
            if c == col:
                original_text += " ▲" if self.sort_reverse else " ▼"
            self.tree.heading(c, text=original_text)
