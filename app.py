import streamlit as st
from fpdf import FPDF
from datetime import datetime

# --- CERTIFICATE PDF CLASS ---
class DegreeCertificate(FPDF):
    def add_design(self):
        # Professional Border
        self.set_line_width(2)
        self.rect(5, 5, 200, 287) # Outer Border
        self.set_line_width(0.5)
        self.rect(7, 7, 196, 283) # Inner Border

    def add_digital_stamp(self, college_name):
        # Stamp Color: Deep Blue (Official Ink Color)
        self.set_draw_color(0, 51, 153)
        self.set_text_color(0, 51, 153)
        
        # Draw Circles for Stamp
        self.set_line_width(0.8)
        self.ellipse(30, 235, 36, 36, 'D') # Outer Circle
        self.set_line_width(0.4)
        self.ellipse(33, 238, 30, 30, 'D') # Inner Circle
        
        # Stamp Text (College Name)
        self.set_font('Arial', 'B', 6)
        display_name = (college_name[:35] + '..') if len(college_name) > 35 else college_name
        
        # Positioning text inside stamp
        self.set_xy(30, 246)
        self.multi_cell(36, 3, display_name.upper(), 0, 'C')
        
        self.set_xy(30, 256)
        self.set_font('Arial', 'B', 8)
        self.cell(36, 5, "OFFICIAL", 0, 1, 'C')
        
        # Reset colors for other elements
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)

    def generate_degree(self, d):
        self.add_page()
        self.add_design()
        
        # 1. College/University Name
        self.ln(20)
        self.set_font('Times', 'B', 25)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        
        # 2. Sub-header
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, "Affiliated with State Technical Board", 0, 1, 'C')
        
        self.ln(10)
        # 3. Main Title
        self.set_font('Times', 'B', 35)
        self.set_text_color(150, 121, 33) # Gold color
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        
        self.ln(10)
        # 4. Content
        self.set_font('Arial', '', 15)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        
        self.set_font('Arial', 'B', 22)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        
        self.set_font('Arial', '', 15)
        self.cell(0, 10, f"Son/Daughter of Mr./Ms. {d['father']}", 0, 1, 'C')
        
        self.ln(5)
        self.set_font('Arial', '', 15)
        msg = "has successfully completed the course of study and passed the examination for the degree of"
        self.multi_cell(0, 10, msg, 0, 'C')
        
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, d['degree'], 0, 1, 'C')
        
        self.set_font('Arial', 'I', 16)
        self.cell(0, 10, f"Specialization in {d['subject']}", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('Arial', '', 14)
        self.cell(0, 10, f"with a Cumulative Grade Point Average (CGPA
