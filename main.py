from report.pdf import PDF
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    pdf = PDF(title="Pelagi Daily Report")
    
    pdf.output("pelagi-report.pdf")

if __name__ == "__main__":
    main()