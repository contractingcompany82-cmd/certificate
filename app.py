import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- CLASS FOR ELITE DOCUMENTS ---
class EliteERP(FPDF):
    def add_digital_stamp(self, org_name):
        """Ye function ek professional round stamp banata hai"""
        self.set_draw_color(0, 51, 153) # Deep Blue Stamp Color
        self.set_line_width(0.8)
        # Outer Circle of Stamp
        self.ellipse(25, 235, 35, 35, 'D')
        # Inner Circle
        self.ellipse(28, 238, 29, 29, 'D')
        
        # Stamp Text (College Name in Circle)
        self.set_font('Arial', 'B', 6)
        self.set_text_color(0, 51, 153)
        self.set_xy(25, 245)
        self.multi_cell(35, 3, org_name.upper()[:40], 0, 'C')
        
        self.set_xy(25, 255)
        self.set_font('Arial', 'B', 7)
        self.cell(35, 5, "VERIFIED", 0, 1, 'C')
        self.set_text_color(0, 0, 0) # Reset color

    def generate_certificate(self, d):
        self.add_page()
        # Double Border
        self.set_line_width(1.5); self.rect(5, 5, 200, 287)
        self.set_line_width(0.5); self.rect(7, 7, 196, 283)
        
        # Header
        self.ln(20)
        self.set_font('Times', 'B', 28)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        
        # Title
        self.ln(10)
        self.set_font('Times', 'B', 38)
        self.set_text_color(184, 134, 11) # Gold
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        
        # Body
        self.ln(15)
        self.set_font('Arial', '', 16)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        self.set_font('Arial', 'B', 24)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        
        self.ln(10)
        self.set_font('Arial', '', 15)
        content = f"has successfully completed the degree of {d['degree']} in {d['subject']} with an aggregate score of {d['cgpa']} CGPA in {d['passing_year']}."
        self.multi_cell(0, 10, content, 0, 'C')
        
        # Footer: Digital Stamp & Sign
        self.add_digital_stamp(d['college'])
        
        self.set_xy(130, 250)
        self.set_font('Arial', 'B', 12)
        self.cell(50, 0, "", 'T', 1, 'C') # Sign Line
        self.set_xy(130, 252)
        self.cell(50, 10, "Registrar / Controller", 0, 1, 'C')
        
        return self.output(dest='S').encode('latin-1')

    def generate_salary(self, d):
        self.add_page()
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, d['comp'].upper(), 0, 1, 'C')
        self.line(10, 25, 200, 25)
        
        self.ln(15)
        self.set_fill_color(240, 240, 240)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP - {d['month']}", 1, 1, 'C', True)
        
        self.ln(5)
        self.set_font('Arial', '', 11)
        self.cell(95, 10, f"Employee: {d['name']}", 1)
        self.cell(95, 10, f"Net Payable: Rs. {d['net']}", 1, 1)
        
        # Digital Stamp for Salary
        self.add_digital_stamp(d['comp'])
        return self.output(dest='S').encode('latin-1')

# --- STREAMLIT INTERFACE ---
st.set_page_config(page_title="RMC Premium ERP", layout="wide")

st.sidebar.title("💎 ELITE ERP SYSTEM")
menu = st.sidebar.radio("Navigation", ["🎓 Degree Module", "💰 Salary Module"])
org_name = st.sidebar.text_input("Organization Name", "Monard University Ghaziabad")

def preview_pdf(pdf_bytes):
    b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    display = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="700" type="application/pdf"></iframe>'
    st.markdown(display, unsafe_allow_html=True)

# --- MODULE 1: DEGREE ---
if menu == "🎓 Degree Module":
    st.title("Academic Certificate Generator")
    with st.form("cert_form"):
        c1, c2 = st.columns(2)
        s_name = c1.text_input("Student Name")
        father = c1.text_input("Father's Name")
        deg = c1.selectbox("Degree", ["B.Tech", "MBA", "B.Sc", "Diploma"])
        
        subj = c2.text_input("Subject")
        cgpa = c2.text_input("CGPA", "8.5")
        p_year = c2.text_input("Passing Year", "2026")
        btn = st.form_submit_button("Generate Official Certificate")
    
    if btn and s_name:
        data = {'college': org_name, 'name': s_name, 'degree': deg, 'subject': subj, 'cgpa': cgpa, 'passing_year': p_year}
        pdf = EliteERP()
        res = pdf.generate_certificate(data)
        st.success("Certificate Generated with Digital Stamp!")
        preview_pdf(res)
        st.download_button("📥 Download PDF", res, f"Degree_{s_name}.pdf")

# --- MODULE 2: SALARY ---
else:
    st.title("Payroll Management")
    with st.form("sal_form"):
        c1, c2 = st.columns(2)
        e_name = c1.text_input("Employee Name")
        month = c1.selectbox("Month", ["Jan 2026", "Feb 2026"])
        basic = c2.number_input("Salary", value=25000)
        pf = c2.number_input("PF", value=1800)
        btn_s = st.form_submit_button("Generate Official Payslip")
        
    if btn_s and e_name:
        data_s = {'comp': org_name, 'name': e_name, 'month': month, 'net': basic-pf}
        pdf_s = EliteERP()
        res_s = pdf_s.generate_salary(data_s)
        st.success("Salary Slip Generated with Digital Stamp!")
        preview_pdf(res_s)
        st.download_button("📥 Download PDF", res_s, f"Salary_{e_name}.pdf")
