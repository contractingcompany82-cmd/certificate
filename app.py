import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. SALARY SLIP PDF CLASS ---
class SalaryPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, st.session_state.comp_name.upper(), 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Industrial Area, Phase-II, New Delhi', 0, 1, 'C')
        self.line(10, 28, 200, 28)

    def generate(self, d):
        self.add_page()
        # Watermark
        self.set_font('Arial', 'B', 40)
        self.set_text_color(245, 245, 245)
        self.rotate(45, 100, 150)
        self.text(40, 190, st.session_state.comp_name.upper())
        self.rotate(0)
        self.set_text_color(0, 0, 0)
        
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP FOR {d['month'].upper()}", 1, 1, 'C', True)
        
        # Table Layout
        h = 8
        self.set_font('Arial', 'B', 10)
        self.cell(95, h, "EARNINGS", 1, 0, 'C', True)
        self.cell(95, h, "DEDUCTIONS", 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        self.cell(60, h, "Basic Salary", 1); self.cell(35, h, f"{d['basic']}", 1, 0, 'R')
        self.cell(60, h, "PF Deduction", 1); self.cell(35, h, f"{d['pf']}", 1, 1, 'R')
        
        self.ln(5)
        self.set_font('Arial', 'B', 12)
        self.cell(190, 10, f"NET PAYABLE: Rs. {d['net']}", 1, 1, 'C', True)
        
        # Digital Sign
        self.ln(20)
        self.set_draw_color(0, 102, 204)
        self.rect(130, 230, 60, 25)
        self.set_xy(130, 232)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.cell(60, 5, "DIGITALLY SIGNED", 0, 1, 'C')
        self.cell(60, 5, f"DATE: {datetime.now().strftime('%d-%m-%Y')}", 0, 1, 'C')
        return self.output(dest='S').encode('latin-1')

# --- 2. CERTIFICATE PDF CLASS ---
class CertificatePDF(FPDF):
    def generate(self, d):
        self.add_page()
        self.set_line_width(2); self.rect(5, 5, 200, 287) # Border
        self.ln(20)
        self.set_font('Times', 'B', 25)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        self.ln(10)
        self.set_font('Times', 'B', 35)
        self.set_text_color(150, 121, 33)
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(15)
        self.set_font('Arial', '', 18)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        self.set_font('Arial', 'B', 25)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 15)
        self.multi_cell(0, 10, f"has completed the course of {d['degree']} in {d['subject']} with CGPA {d['cgpa']}.", 0, 'C')
        return self.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
st.set_page_config(page_title="RMC Multi-ERP", layout="wide")

# Sidebar
st.sidebar.title("🏗️ RMC GROUP ERP")
menu = st.sidebar.radio("Module Chuniye", ["💰 Salary Module", "🎓 Certificate Module"])
st.session_state.comp_name = st.sidebar.text_input("Company/College Name", "Global RMC Group")

def show_pdf(bytes_data):
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- MODULE 1: SALARY ---
if menu == "💰 Salary Module":
    st.header("Professional Salary Slip Generator")
    with st.form("salary_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Employee Name")
            month = st.selectbox("Month", ["Jan 2026", "Feb 2026", "Mar 2026"])
        with c2:
            basic = st.number_input("Basic Salary", value=20000)
            pf = st.number_input("PF", value=1800)
        
        submit = st.form_submit_button("Generate Salary Slip")
        
    if submit:
        data = {'name': name, 'month': month, 'basic': basic, 'pf': pf, 'net': basic-pf}
        pdf = SalaryPDF()
        pdf_bytes = pdf.generate(data)
        st.success("Slip Ready!")
        show_pdf(pdf_bytes)
        st.download_button("📥 Download Slip", pdf_bytes, f"Salary_{name}.pdf")

# --- MODULE 2: CERTIFICATE ---
elif menu == "🎓 Certificate Module":
    st.header("Academic Certificate Generator")
    with st.form("cert_form"):
        c1, c2 = st.columns(2)
        with c1:
            s_name = st.text_input("Student Name")
            degree = st.text_input("Degree (e.g. B.Tech)")
        with col2 := st.columns(1)[0]: # Fix for simple layout
            subject = st.text_input("Subject")
            cgpa = st.text_input("CGPA")
            
        submit = st.form_submit_button("Generate Certificate")

    if submit:
        data = {'college': st.session_state.comp_name, 'name': s_name, 'degree': degree, 'subject': subject, 'cgpa': cgpa}
        pdf = CertificatePDF()
        pdf_bytes = pdf.generate(data)
        st.success("Certificate Ready!")
        show_pdf(pdf_bytes)
        st.download_button("📥 Download Certificate", pdf_bytes, f"Degree_{s_name}.pdf")
