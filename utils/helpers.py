from fpdf import FPDF

def hex_to_rgb(hex: str):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def small_break(pdf: FPDF):
    pdf.ln(2)
           
def medium_break(pdf: FPDF):
    pdf.ln(4)

def large_break(pdf: FPDF):
    pdf.ln(8)