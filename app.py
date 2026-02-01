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
        self.set_text_color(0, 0, 0) # Back to black
        
        self.ln(10)
        # 4. Content
        self.set_font('Arial', '', 15)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        
        self.set_font('Arial', 'B', 22)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        
        self.set_font('Arial', '', 15)
        self.cell(0, 10, f"Son/Daughter of Mr./Ms. {d['father']}", 0, 1, 'C')
        
        self.ln(5)
        self.multi_cell(0, 10, f"has successfully completed the course of study and passed the examination for the degree of", 0, 'C')
        
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, d['degree'], 0, 1, 'C')
        
        self.set_font('Arial', 'I', 16)
        self.cell(0, 10, f"Specialization in {d['subject']}", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('Arial', '', 14)
        self.cell(0, 10, f"with a Cumulative Grade Point Average (CGPA) of {d['cgpa']}", 0, 1, 'C')
        self.cell(0, 10, f"held in the month of {d['passing_year']}", 0, 1, 'C')

        # 5. Bottom Seal and Signature
        self.ln(30)
        self.set_font('Arial', 'B', 12)
        
        # Seal Placeholder (Left)
        self.set_xy(30, 240)
        self.cell(40, 40, "OFFICIAL SEAL", border=1, align='C')
        
        # Signature (Right)
        self.set_xy(130, 255)
        self.cell(50, 0, "", 'T', 1, 'C') # Signature Line
        self.set_xy(130, 257)
        self.cell(50, 10, "Registrar / Controller", 0, 1, 'C')

        # Watermark (Center)
        self.set_font('Arial', 'B', 60)
        self.set_text_color(245, 245, 245)
        self.text(40, 160, "VERIFIED")

# --- STREAMLIT UI ---
st.set_page_config(page_title="Academic ERP", layout="centered")
st.title("🎓 Academic Certificate ERP")
st.markdown("---")

with st.form("degree_form"):
    college = st.text_input("College/University Name", "Indian Institute of Technology")
    
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("Student Full Name")
        father = st.text_input("Father's Name")
        degree = st.selectbox("Degree", ["Bachelor of Technology", "Master of Business Admin", "Bachelor of Science", "Diploma"])
    
    with col2:
        subject = st.text_input("Subject/Specialization (e.g. Civil Engg)")
        cgpa = st.text_input("CGPA / Percentage", "8.5")
        p_year = st.text_input("Passing Year/Month", "May 2026")
        enroll = st.text_input("Enrollment No.")

    submitted = st.form_submit_button("Generate Official Certificate")

if submitted:
    data = {
        'college': college, 'name': s_name, 'father': father,
        'degree': degree, 'subject': subject, 'cgpa': cgpa,
        'passing_year': p_year, 'enroll': enroll
    }
    
    pdf = DegreeCertificate()
    pdf.generate_degree(data)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    st.success(f"Certificate for {s_name} is ready!")
    st.download_button("📥 Download Degree PDF", pdf_bytes, f"Degree_{s_name}.pdf", "application/pdf")
