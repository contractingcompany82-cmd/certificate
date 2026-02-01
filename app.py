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
        # Stamp Color: Deep Blue (Ink Color)
        self.set_draw_color(0, 51, 153)
        self.set_text_color(0, 51, 153)
        
        # Draw Circles for Stamp
        self.set_line_width(0.8)
        self.ellipse(30, 235, 36, 36, 'D') # Outer Circle
        self.set_line_width(0.4)
        self.ellipse(33, 238, 30, 30, 'D') # Inner Circle
        
        # Stamp Text (College Name)
        self.set_font('Arial', 'B', 6)
        # Shorten name if too long for the stamp
        display_name = (college_name[:35] + '..') if len(college_name) > 35 else college_name
        
        # Positioning text inside stamp
        self.set_xy(30, 246)
        self.multi_cell(36, 3, display_name.upper(), 0, 'C')
        
        self.set_xy(30, 256)
        self.set_font('Arial', 'B', 8)
        self.cell(36, 5, "OFFICIAL", 0, 1, 'C')
        
        # Reset colors to black for other elements
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)

    def generate_degree(self, d):
        self.add_page()
        self.add_design()
        
        # 1. College/University Name
        self.ln(20)
        self.set_font('
