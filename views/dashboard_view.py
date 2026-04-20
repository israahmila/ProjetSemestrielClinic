import customtkinter as ctk
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

from theme import *

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, corner_radius=0, fg_color="transparent")
        self.controller = controller
        
        self.grid_rowconfigure((0, 1), weight=0) 
        self.grid_rowconfigure(2, weight=1) 
        self.grid_columnconfigure((0, 1), weight=1)
        
        self.create_welcome_banner()
        self.create_stats_grid()
        self.create_bottom_sections()

    def create_welcome_banner(self):
        banner = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        banner.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 24))
        
        lbl_welcome = ctk.CTkLabel(banner, text="Welcome back, Admin! ", font=ctk.CTkFont(size=28, weight="bold"), text_color=C_TEXT_PRIMARY)
        lbl_welcome.pack(anchor="w", padx=30, pady=(24, 5))
        
        lbl_sub = ctk.CTkLabel(banner, text="Here's what's happening with your clinic today.", font=ctk.CTkFont(size=14), text_color=C_TEXT_MUTED)
        lbl_sub.pack(anchor="w", padx=30, pady=(0, 24))

    def create_stats_grid(self):
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(0, 24))
        self.stats_frame.grid_columnconfigure((0,1,2), weight=1)
        
        self.stat_patients = self.create_stat_card(self.stats_frame, "Total Patients", "0", C_PRIMARY, 0)
        self.stat_doctors = self.create_stat_card(self.stats_frame, "Active Doctors", "0", '#06B6D4', 1)
        self.stat_today = self.create_stat_card(self.stats_frame, "Appointments Today", "0", '#10B981', 2)

    def create_stat_card(self, parent, title, value, color, col):
        card = ctk.CTkFrame(parent, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 16) if col < 3 else 0)
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14), text_color=C_TEXT_MUTED)
        lbl_title.pack(anchor="w", padx=20, pady=(20, 5))
        
        lbl_val = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=32, weight="bold"), text_color=color)
        lbl_val.pack(anchor="w", padx=20, pady=(0, 20))
        return lbl_val

    def create_bottom_sections(self):
        
        recent_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        recent_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 12))
        
        ctk.CTkLabel(recent_frame, text="Recent Activity", font=ctk.CTkFont(size=20, weight="bold"), text_color=C_TEXT_PRIMARY).pack(anchor="w", padx=24, pady=24)
        
        
        self.recent_container = ctk.CTkFrame(recent_frame, fg_color="transparent")
        self.recent_container.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        
        actions_frame = ctk.CTkFrame(self, corner_radius=16, fg_color=C_BG_CARD, border_width=1, border_color=C_BORDER_GLOW)
        actions_frame.grid(row=2, column=1, sticky="nsew", padx=(12, 0))
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", font=ctk.CTkFont(size=20, weight="bold"), text_color=C_TEXT_PRIMARY).pack(anchor="w", padx=24, pady=24)
        
        grid_f = ctk.CTkFrame(actions_frame, fg_color="transparent")
        grid_f.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        grid_f.grid_columnconfigure((0, 1), weight=1)
        grid_f.grid_rowconfigure((0, 1), weight=1)
        
        qa = [
            ("👤 New Patient", 0, 0, C_PRIMARY, "patients"),
            ("📅 Schedule", 0, 1, '#06B6D4', "appointments"),
            ("💊 Prescribe", 1, 0, '#10B981', "prescriptions"),
            ("👨‍⚕️ Doctors", 1, 1, '#F59E0B', "doctors")
        ]
        
        for text, r, c, color, view_name in qa:
            btn = ctk.CTkButton(grid_f, text=text, font=ctk.CTkFont(size=15, weight="bold"), 
                                fg_color="#1E293B", hover_color=C_BG_BASE, 
                                border_width=1, border_color=color, text_color=C_TEXT_PRIMARY, height=60,
                                command=lambda v=view_name: self.controller.show_view(v))
            btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

    def refresh_data(self):
        pat_count = Patient.get_count()
        doc_count = Doctor.get_count()
        app_today = Appointment.get_stats_today()
        
        self.stat_patients.configure(text=str(pat_count))
        self.stat_doctors.configure(text=str(doc_count))
        self.stat_today.configure(text=str(app_today))
        
       
        for widget in self.recent_container.winfo_children():
            widget.destroy()
            
        recent_apps = Appointment.get_all()[:4] 
        colors = [C_PRIMARY, '#10B981', '#F59E0B', '#06B6D4']
        
        for i, app in enumerate(recent_apps):
            c = colors[i % len(colors)]
            act_text = f"{app['patient_name']} scheduled with Dr. {app['doctor_name'].split(' ')[-1]}"
            act_time = f"{app['date']} {app['time']}"
            
            act_frame = ctk.CTkFrame(self.recent_container, fg_color="#1E293B", corner_radius=8)
            act_frame.pack(fill="x", pady=(0, 12))
            dot = ctk.CTkLabel(act_frame, text="⬤", text_color=c, font=ctk.CTkFont(size=10))
            dot.pack(side="left", padx=15, pady=15)
            ctk.CTkLabel(act_frame, text=act_text, font=ctk.CTkFont(size=14, weight="bold"), text_color=C_TEXT_PRIMARY).pack(side="left", pady=15)
            ctk.CTkLabel(act_frame, text=act_time, font=ctk.CTkFont(size=12), text_color=C_TEXT_MUTED).pack(side="right", padx=15, pady=15)
