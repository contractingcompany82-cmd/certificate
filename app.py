import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. SALARY SLIP PDF CLASS ---
class SalaryPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, st.session_state.get('comp_name', 'RMC GROUP').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Industrial Area, Phase-II, New Delhi', 0, 1, 'C')
        self.line(10, 28, 200, 28)

    def generate(self, d):
        self.add_page()
        # Watermark
        self.set_font('Arial', 'B', 40)
        self.set_text_color(245, 245, 245)
        self.rotate(45, 100, 150)
        self.text(40, 190, st.session_state.get('comp_name', 'RMC').upper())
        self.rotate(0)
        self.set_text_color(0, 0, 0)
        
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 10, f"PAYSLIP FOR {d['month'].upper()}", 1, 1, 'C', True)
        
        h = 8
        self.set_font('Arial', '', 10)
        self.ln(5)
        self.cell(95, h, f"Employee: {d['name']}", 1)
        self.cell(95, h, f"Basic: Rs. {d['basic']}", 1, 1)
        self.cell(95, h, f"PF: Rs. {d['pf']}", 1)
        self.cell(95, h, f"Net Paid: Rs. {d['net']}", 1, 1)
        
        # Digital Sign Area
        self.ln(20)
        self.set_draw_color(0, 102, 204)
        self.rect(130, 230, 60, 25)
        self.set_xy(130, 232)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.cell(60, 5, "DIGITALLY SIGNED", 0, 1, 'C')
        # Yahan line 43 fix kar di gayi hai:
        self.set_font('Arial', '', 7) 
        self.cell(60
