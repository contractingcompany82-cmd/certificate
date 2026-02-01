import streamlit as st
from fpdf import FPDF
import base64

# --- CERTIFICATE PDF CLASS ---
class DegreeCertificate(FPDF):
    def add_design(self):
        # Professional Border
        self.set_line_width(2)
        self.rect(5, 5, 200, 287) # Outer Border
        self.set_line_width(0.5)
        self.rect(7, 7, 196, 283) # Inner Border

    def add_digital_stamp(self, college_name):
        # Stamp Color: Deep Blue
        self.set_draw_color(0, 51, 153)
        self.set_text_color(0, 51, 153)
        
        # Draw Circles for Stamp
        self.set_line_width(0.8)
        self.ellipse(30, 235, 36, 36, 'D') 
        self.set_line_width(0.4)
        self.ellipse(33, 238, 30, 30, 'D') 
        
        # Stamp Text
        self.set_font('Arial', 'B', 6)
        display_name = (college_name[:35] + '..') if len(college_name) > 35 else college_name
        
        self.set_xy(30, 246)
        self.multi_cell(36, 3, display_name.upper(), 0, 'C')
        
        self.set_xy(30, 256)
        self.set_font('Arial', 'B', 8)
        self.cell(36, 5, "OFFICIAL", 0, 1, 'C')
        
        # Reset colors
        self.set_text_color(0, 0, 0)
        self.set_draw_color(0, 0, 0)

    def generate_degree(self, d):
        self.add_page()
        self.add_design()
        
        # 1. College Name
        self.ln(20)
        self.set_font('Times', 'B', 25)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, "Affiliated with State Technical Board", 0, 1, 'C')
        
        self.ln(10)
        # 2. Main Title
        self.set_font('Times', 'B', 35)
        self.set_text_color(150, 121, 33) # Gold color
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        
        self.ln(10)
        # 3. Content
        self.set_font('Arial', '', 15)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        
        self.set_font('Arial', 'B', 22)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        
        self.set_font('Arial', '', 15)
        self.cell(0, 10, f"Son/Daughter of Mr./Ms. {d['father']}", 0, 1, 'C')
        
        self.ln(5)
        msg = "has successfully completed the course of study and passed the examination for the degree of"
        self.multi_cell(0, 10, msg, 0, 'C')
        
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, d['degree'], 0, 1, 'C')
        
        self.set_font('Arial', 'I', 16)
        self.cell(0, 10, f"Specialization in {d['subject']}", 0, 1, 'C')
        
        self.ln(10)
        self.set_font('Arial', '', 14)
        self.cell(0, 10, f"with a Cumulative Grade Point Average (CGPA) of {d['cgpa']}", 0, 1, 'C')
        self.cell(0, 10, f"held in the month of {d['passing_year']}", 0, 1, 'C')

        # 4. Stamp and Signature
        self.ln(30)
        self.add_digital_stamp(d['college'])
        
        self.set_xy(130, 255)
        self.set_font('Arial', 'B', 12)
        self.cell(50, 0, "", 'T', 1, 'C') 
        self.set_xy(130, 257)
        self.cell(50, 10, "Registrar / Controller", 0, 1, 'C')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Academic ERP", layout="centered")

def get_pdf_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">📥 Download Certificate PDF</a>'

st.title("🎓 Academic Certificate ERP")
st.markdown("---")

with st.form("degree_form"):
    college = st.text_input("College/University Name", "Monard University Ghaziabad")
    
    col1, col2 = st.columns(2)
    with col1:
        s_name = st.text_input("Student Full Name")
        father = st.text_input("Father's Name")
        degree = st.selectbox("Degree", ["Bachelor of Technology", "Master of Business Admin", "Bachelor of Science", "Diploma"])
    
    with col2:
        subject = st.text_input("Subject/Specialization")
        cgpa = st.text_input("CGPA", "8.5")
        p_year = st.text_input("Passing Year", "May 2026")

    submitted = st.form_submit_button("Generate Official Certificate")

if submitted:
    if s_name:
        data = {
            'college': college, 'name': s_name, 'father': father,
            'degree': degree, 'subject': subject, 'cgpa': cgpa,
            'passing_year': p_year
        }
        
        pdf = DegreeCertificate()
        pdf.generate_degree(data)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        
        st.success(f"Certificate for {s_name} is ready!")
        st.download_button("📥 Download PDF", pdf_bytes, f"Degree_{s_name}.pdf", "application/pdf")
    else:
        st.error("Naam toh daalo bhai!")
