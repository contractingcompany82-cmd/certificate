import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- 1. SALARY SLIP PDF CLASS ---
class SalaryPDF(FPDF):
    def generate(self, d):
        self.add_page()
        # Header
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, st.session_state.get('comp_name', 'RMC GROUP').upper(), 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Official Payroll Document', 0, 1, 'C')
        self.line(10, 30, 200, 30)
        
        # Body
        self.ln(15)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP - {d['month']}", 1, 1, 'C')
        
        self.ln(5)
        self.set_font('Arial', '', 11)
        self.cell(95, 10, f"Employee Name: {d['name']}", 1)
        self.cell(95, 10, f"Basic: Rs. {d['basic']}", 1, 1)
        self.cell(95, 10, f"PF: Rs. {d['pf']}", 1)
        self.cell(95, 10, f"Net Salary: Rs. {d['net']}", 1, 1)
        
        # Digital Sign Box
        self.ln(20)
        self.set_font('Arial', 'B', 8)
        self.set_text_color(0, 102, 204)
        self.rect(130, 230, 60, 20)
        self.set_xy(130, 232)
        self.cell(60, 5, "DIGITALLY SIGNED", 0, 1, 'C')
        self.cell(60, 5, f"DATE: {datetime.now().strftime('%d-%m-%Y')}", 0, 1, 'C')
        return self.output(dest='S').encode('latin-1')

# --- 2. CERTIFICATE PDF CLASS ---
class CertificatePDF(FPDF):
    def generate(self, d):
        self.add_page()
        self.set_line_width(2)
        self.rect(5, 5, 200, 287) # Border
        self.ln(30)
        self.set_font('Times', 'B', 28)
        self.cell(0, 15, d['college'].upper(), 0, 1, 'C')
        self.ln(20)
        self.set_font('Times', 'B', 36)
        self.set_text_color(150, 121, 33) # Gold
        self.cell(0, 25, "PROVISIONAL DEGREE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(20)
        self.set_font('Arial', '', 18)
        self.cell(0, 10, "This is to certify that", 0, 1, 'C')
        self.set_font('Arial', 'B', 24)
        self.cell(0, 15, d['name'].upper(), 0, 1, 'C')
        self.ln(10)
        self.set_font('Arial', '', 16)
        msg = f"has successfully completed the course of {d['degree']} in {d['subject']} with CGPA {d['cgpa']}."
        self.multi_cell(0, 10, msg, 0, 'C')
        return self.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
st.set_page_config(page_title="RMC Multi-ERP", layout="wide")

st.sidebar.title("🏗️ RMC GROUP ERP")
menu = st.sidebar.radio("Module", ["💰 Salary Module", "🎓 Certificate Module"])
comp_name = st.sidebar.text_input("Org Name", "Global RMC Group")
st.session_state.comp_name = comp_name

def show_pdf(bytes_data):
    base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

if menu == "💰 Salary Module":
    st.header("Professional Salary Slip")
    with st.form("sal_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        month = c1.selectbox("Month", ["Jan 2026", "Feb 2026"])
        basic = c2.number_input("Basic", value=20000)
        pf = c2.number_input("PF", value=1800)
        sub = st.form_submit_button("Generate")
    
    if sub and name:
        pdf = SalaryPDF()
        res = pdf.generate({'name':name, 'month':month, 'basic':basic, 'pf':pf, 'net':basic-pf})
        show_pdf(res)
        st.download_button("Download", res, "Salary.pdf")

elif menu == "🎓 Certificate Module":
    st.header("Academic Certificate")
    with st.form("cert_form"):
        c1, c2 = st.columns(2)
        s_name = c1.text_input("Student Name")
        deg = c1.text_input("Degree")
        sub_j = c2.text_input("Subject")
        grade = c2.text_input("CGPA")
        btn = st.form_submit_button("Generate Certificate")
        
    if btn and s_name:
        pdf_c = CertificatePDF()
        res_c = pdf_c.generate({'college':comp_name, 'name':s_name, 'degree':deg, 'subject':sub_j, 'cgpa':grade})
        show_pdf(res_c)
        st.download_button("Download", res_c, "Degree.pdf")
