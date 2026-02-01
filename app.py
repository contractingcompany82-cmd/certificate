import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- CLASS FOR ELITE SALARY SLIP ---
class SalaryElite(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, st.session_state.get('comp_name', 'RMC GROUP').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'ISO Certified Organization | Industrial Hub, Delhi', 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32)

    def add_watermark(self):
        self.set_font('Arial', 'B', 50)
        self.set_text_color(240, 240, 240)
        self.rotate(45, 100, 150)
        self.text(45, 190, "OFFICIAL RECORD")
        self.rotate(0)
        self.set_text_color(0, 0, 0)

    def generate(self, d):
        self.add_page()
        self.add_watermark()
        self.ln(12)
        self.set_fill_color(230, 230, 230)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP FOR {d['month'].upper()}", 1, 1, 'C', True)
        
        # Side-by-Side Professional Table
        self.ln(10)
        self.set_font('Arial', 'B', 10)
        self.cell(65, 8, "EARNINGS", 1, 0, 'C', True)
        self.cell(30, 8, "AMOUNT", 1, 0, 'C', True)
        self.cell(65, 8, "DEDUCTIONS", 1, 0, 'C', True)
        self.cell(30, 8, "AMOUNT", 1, 1, 'C', True)
        
        self.set_font
