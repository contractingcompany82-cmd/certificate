import streamlit as st
from fpdf import FPDF
import base64

# --- CERTIFICATE CLASS ---
class DegreeCertificate(FPDF):
    def add_design(self):
        self.set_line_width(2)
        self.rect(5, 5, 200, 287)
        self.set_line_width(0.5)
        self.rect(7, 7, 196, 283)

    def generate_degree(self, d):
        self.add_page()
        self.add_design()
        self.ln(20)
        self.set_font('Times', 'B', 25)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        self.ln(10)
        self.set_font('Times', 'B', 35)
        self.set_text_color(150, 121, 33) # Gold color
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.set_font('Arial', '', 18)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        self.set_font('Arial', 'B', 25)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        self.set_font('Arial', '', 15)
        self.cell(0, 10, f"Degree: {d['degree']}", 0, 1, 'C')
        self.cell(0, 10, f"Subject: {d['subject']}", 0, 1, 'C')
        self.ln(20)
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, f"Date of Issue: {d['date']}", 0, 1, 'C')
        return self.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
st.title("🎓 Certificate Generator")

with st.form("cert_form"):
    college = st.text_input("University/College Name", "RMC Institute of Technology")
    name = st.text_input("Student Name")
    degree = st.selectbox("Degree", ["B.Tech", "
