import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

# --- CLASS FOR SALARY SLIP ---
class SalaryElite(FPDF):
    def generate_slip(self, d):
        self.add_page()
        # Watermark
        self.set_font('Arial', 'B', 50)
        self.set_text_color(240, 240, 240)
        self.text(45, 150, "OFFICIAL RECORD")
        
        # Header
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, st.session_state.get('org_name', 'GLOBAL RMC').upper(), 0, 1, 'C')
        self.line(10, 25, 200, 25)
        
        # Table
        self.ln(20)
        self.set_fill_color(230, 230, 230)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"PAYSLIP - {d['month']}", 1, 1, 'C', True)
        
        self.set_font('Arial', '', 10)
        self.cell(95, 10, f"Employee: {d['name']}", 1)
        self.cell(95, 10, f"Net Salary: Rs. {d['net']}", 1, 1)
        
        # Digital Sign Box
        self.ln(30)
        self.rect(140, 240, 50, 20)
        self.set_xy(140, 242)
        self.set_font('Arial', 'B', 8)
        self.cell(50, 5, "VERIFIED DIGITAL", 0, 1, 'C')
        return self.output(dest='S').encode('latin-1')

# --- CLASS FOR CERTIFICATE ---
class CertElite(FPDF):
    def generate_cert(self, d):
        self.add_page()
        self.set_line_width(2)
        self.rect(5, 5, 200, 287)
        self.ln(30)
        self.set_font('Times', 'B', 30)
        self.cell(0, 15, d['org'].upper(), 0, 1, 'C')
        self.ln(20)
        self.set_font('Times', 'B', 40)
        self.set_text_color(184, 134, 11) # Gold
        self.cell(0, 20, "DEGREE CERTIFICATE", 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(20)
        self.set_font('Arial', '', 18)
        self.cell(0, 10, f"This is to certify that {d['name']}", 0, 1, 'C')
        self.multi_cell(0, 10, f"has passed {d['degree']} in {d['subject']}.", 0, 'C')
        return self.output(dest='S').encode('latin-1')

# --- STREAMLIT UI ---
st.set_page_config(page_title="Professional ERP", layout="wide")

st.sidebar.title("💎 MULTI-ERP SYSTEM")
module = st.sidebar.radio("Select Module", ["Salary Slip", "Certificate"])
org_name = st.sidebar.text_input("Organization Name", "Global RMC Group")
st.session_state.org_name = org_name

def preview(pdf_bytes):
    b64 = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_html = f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="600px"></iframe>'
    st.markdown(pdf_html, unsafe_allow_html=True)

if module == "Salary Slip":
    st.title("💰 Professional Payroll")
    with st.form("s_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        month = c1.selectbox("Month", ["Jan 2026", "Feb 2026"])
        basic = c2.number_input("Salary", value=30000)
        pf = c2.number_input("PF", value=1800)
        go = st.form_submit_button("Generate Official Slip")
    if go and name:
        pdf_s = SalaryElite()
        out = pdf_s.generate_slip({'name':name, 'month':month, 'net':basic-pf})
        preview(out)
        st.download_button("Download", out, "Salary.pdf")

else:
    st.title("🎓 Certificate Module")
    with st.form("c_form"):
        c1, c2 = st.columns(2)
        s_name = c1.text_input("Student Name")
        deg = c1.text_input("Degree")
        subj = c2.text_input("Subject")
        btn = st.form_submit_button("Generate Certificate")
    if btn and s_name:
        pdf_c = CertElite()
        out_c = pdf_c.generate_cert({'org':org_name, 'name':s_name, 'degree':deg, 'subject':subj})
        preview(out_c)
        st.download_button("Download", out_c, "Degree.pdf")
