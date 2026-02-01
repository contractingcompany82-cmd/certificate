import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- CLASS FOR ELITE SALARY SLIP ---
class SalaryElite(FPDF):
    def header(self):
        # Company Name & Branding
        self.set_font('Arial', 'B', 18)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, st.session_state.get('comp_name', 'RMC GROUP').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'ISO 9001:2015 Certified Organization | Industrial Hub, Delhi', 0, 1, 'C')
        self.ln(5)
        self.line(10, 32, 200, 32) # Heavy Header Line

    def add_watermark(self):
        self.set_font('Arial', 'B', 55)
        self.set_text_color(240, 240, 240)
        self.rotate(45, 100, 150)
        self.text(45, 190, "OFFICIAL COPY")
        self.rotate(0)
        self.set_text_color(0, 0, 0)

    def generate(self, d):
        self.add_page()
        self.add_watermark()
        self.ln(12)
        
        # Payslip Title
        self.set_fill_color(230, 230, 230)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP FOR THE MONTH OF {d['month'].upper()}", 1, 1, 'C', True)
        
        # Employee Details Section
        self.ln(5)
        self.set_font('Arial', 'B', 10)
        self.cell(30, 8, "Employee Name:", 0); self.set_font('Arial', '', 10); self.cell(70, 8, d['name'], 0)
        self.set_font('Arial', 'B', 10); self.cell(30, 8, "Employee ID:", 0); self.set_font('Arial', '', 10); self.cell(60, 8, "EMP10293", 0, 1)
        
        self.ln(5)
        # SIDE-BY-SIDE TABLE (Professional Layout)
        self.set_font('Arial', 'B', 10)
        self.cell(65, 8, "EARNINGS", 1, 0, 'C', True)
        self.cell(30, 8, "AMOUNT", 1, 0, 'C', True)
        self.cell(65, 8, "DEDUCTIONS", 1, 0, 'C', True)
        self.cell(30, 8, "AMOUNT", 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        # Row 1
        self.cell(65, 8, "Basic Salary", 1); self.cell(30, 8, f"{d['basic']}", 1, 0, 'R')
        self.cell(65, 8, "Provident Fund (PF)", 1); self.cell(30, 8, f"{d['pf']}", 1, 1, 'R')
        # Row 2
        self.cell(65, 8, "House Rent Allowance", 1); self.cell(30, 8, "5000.00", 1, 0, 'R')
        self.cell(65, 8, "Professional Tax", 1); self.cell(30, 8, "200.00", 1, 1, 'R')
        
        # Totals
        self.set_font('Arial', 'B', 10)
        self.cell(65, 10, "Gross
