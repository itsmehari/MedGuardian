"""
Generate realistic sample PDF lab reports for MedGuardian demo/testing.

Creates 15 reports from 5 different laboratories, varied age groups
(young adult, adult, middle-aged, senior), and risk profiles (low/moderate/high).
Text format matches regex patterns in services/pdf_parser.py.

Usage:
    pip install reportlab
    python scripts/generate_sample_reports.py

Output: data/sample_reports/*.pdf
"""

from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "sample_reports"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Different laboratories (name, address, phone, email, report_prefix, director)
LABS = [
    {
        "name": "CARE DIAGNOSTICS LABORATORY",
        "address": "No. 42, Anna Salai, T. Nagar, Chennai - 600 017",
        "phone": "Ph: 044-2834 5678 | NABL Accredited",
        "email": "reports@carediagnostics.in",
        "prefix": "CDL",
        "director": "Dr. R. Meenakshi, MBBS, DCP",
        "physician": "Dr. S. Krishnan, MD (Gen. Med)",
    },
    {
        "name": "APOLLO DIAGNOSTICS",
        "address": "Apollo Hospitals Campus, Greams Rd, Chennai - 600 006",
        "phone": "Ph: 044-2829 3333 | CAP Accredited",
        "email": "lab@apollohospitals.com",
        "prefix": "APL",
        "director": "Dr. K. Venkatesh, MD (Pathology)",
        "physician": "Dr. P. Lakshmi, MBBS, DNB",
    },
    {
        "name": "THYRO LAB & DIAGNOSTIC CENTRE",
        "address": "45, MG Road, Bengaluru - 560 001",
        "phone": "Ph: 080-2222 4455",
        "email": "support@thyrolab.in",
        "prefix": "TLD",
        "director": "Dr. A. Nandini, MD, DCP",
        "physician": "Dr. R. Kumar, MBBS, MD (Med)",
    },
    {
        "name": "METROPOLITAN PATHOLOGY LAB",
        "address": "Plot 12, Sector 18, Gurgaon - 122 015",
        "phone": "Ph: 0124-456 7890 | NABL",
        "email": "info@metropathlab.com",
        "prefix": "MPL",
        "director": "Dr. Vishal Sharma, MD (Pathology)",
        "physician": "Dr. Anjali Gupta, MBBS, DNB",
    },
    {
        "name": "SUNRISE CLINICAL LABORATORY",
        "address": "Block B, Kothrud, Pune - 411 038",
        "phone": "Ph: 020-2543 2121",
        "email": "lab@sunriseclinical.com",
        "prefix": "SCL",
        "director": "Dr. M. Deshpande, MBBS, DMLT",
        "physician": "Dr. S. Joshi, MD (Internal Medicine)",
    },
]

# (name, age, sex, glucose, hba1c, bmi, sbp, dbp, cholesterol, risk_level, lab_index)
# Age groups: 22-29 young, 32-42 adult, 48-58 middle, 65-72 senior
PROFILES = [
    # Low risk - varied labs & ages
    ("Anita Reddy", 26, "F", 82, 5.0, 21.2, 114, 72, 168, "low", 0),
    ("Karthik Pillai", 24, "M", 76, 4.8, 22.0, 110, 70, 162, "low", 1),
    ("Meera Iyer", 38, "F", 90, 5.3, 23.5, 118, 76, 188, "low", 2),
    ("Suresh Nair", 65, "M", 94, 5.5, 22.8, 122, 78, 192, "low", 3),
    ("Divya Menon", 32, "F", 86, 5.1, 20.5, 115, 74, 178, "low", 4),
    # Moderate risk - varied labs & ages
    ("Vijay Kumar", 52, "M", 118, 6.0, 27.5, 132, 84, 218, "moderate", 0),
    ("Lakshmi Menon", 45, "F", 108, 5.8, 26.2, 128, 82, 225, "moderate", 1),
    ("Ramesh Singh", 48, "M", 122, 6.2, 28.0, 135, 86, 232, "moderate", 2),
    ("Deepa Sharma", 58, "F", 115, 5.9, 25.8, 130, 83, 210, "moderate", 3),
    ("Prakash Rao", 41, "M", 112, 5.7, 26.5, 126, 80, 205, "moderate", 4),
    # High risk - varied labs & ages
    ("Rajesh Patel", 62, "M", 156, 7.8, 34.2, 158, 96, 278, "high", 0),
    ("Priya Venkat", 68, "F", 142, 7.2, 32.0, 148, 94, 265, "high", 1),
    ("Arun Thomas", 55, "M", 168, 8.2, 36.5, 162, 98, 292, "high", 2),
    ("Kavitha Rajan", 48, "F", 138, 6.9, 31.2, 152, 92, 258, "high", 3),
    ("Mohan Das", 70, "M", 148, 7.5, 33.0, 155, 95, 268, "high", 4),
]


def _draw_line(c: canvas.Canvas, y: float, text: str, x: float = 50, font: str = "Helvetica", size: int = 10) -> float:
    c.setFont(font, size)
    c.drawString(x, y, text)
    return y - 16


def _flag(value: float, low: float, high: float) -> str:
    if value < low:
        return "L"
    if value > high:
        return "H"
    return "N"


def generate_report(
    lab: dict,
    report_id: str,
    patient_name: str,
    age: int,
    sex: str,
    test_date: str,
    glucose: float,
    hba1c: float,
    bmi: float,
    systolic_bp: int,
    diastolic_bp: int,
    cholesterol: float,
    output_path: Path,
) -> None:
    """Generate a lab report PDF for the given laboratory."""
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    y = height - 40

    # ----- LAB HEADER (varies by lab) -----
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(width / 2, y, lab["name"])
    y -= 14
    c.setFont("Helvetica", 9)
    c.drawCentredString(width / 2, y, lab["address"])
    y -= 12
    c.drawCentredString(width / 2, y, lab["phone"])
    y -= 10
    c.drawCentredString(width / 2, y, lab["email"])
    y -= 20

    c.setStrokeColorRGB(0.2, 0.2, 0.2)
    c.line(50, y, width - 50, y)
    y -= 20

    # ----- REPORT & PATIENT INFO -----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "LABORATORY REPORT")
    y -= 10

    c.setFont("Helvetica", 10)
    y = _draw_line(c, y, f"Report ID: {report_id}", size=10)
    y = _draw_line(c, y, f"Patient Name: {patient_name}")
    y = _draw_line(c, y, f"Age / Sex: {age} Yrs / {sex}")
    y = _draw_line(c, y, f"Collection Date: {test_date}")
    y = _draw_line(c, y, "Specimen: Serum (Fasting 10-12 hrs)")
    y = _draw_line(c, y, f"Referring Physician: {lab['physician']}")
    y = _draw_line(c, y, "Received: " + test_date + " 08:45 | Reported: " + test_date + " 14:30")
    y -= 15

    # ----- GLYCEMIC PROFILE -----
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.rect(50, y - 2, width - 100, 18, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(55, y + 2, "GLYCEMIC PROFILE")
    c.setFillColorRGB(0, 0, 0)
    y -= 25

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Test")
    c.drawString(200, y, "Result")
    c.drawString(320, y, "Reference")
    c.drawString(480, y, "Flag")
    y -= 14
    c.setFont("Helvetica", 9)
    c.line(50, y, 540, y)
    y -= 14

    g_flag = _flag(glucose, 70, 99)
    c.drawString(55, y, f"Fasting Glucose: {glucose} mg/dL")
    c.drawString(320, y, "70 - 99")
    c.drawString(485, y, g_flag)
    y -= 14

    h_flag = _flag(hba1c, 4.0, 5.6)
    c.drawString(55, y, f"HbA1c: {hba1c} %")
    c.drawString(320, y, "4.0 - 5.6")
    c.drawString(485, y, h_flag)
    y -= 14

    c.drawString(55, y, "Insulin (Fasting)")
    c.drawString(200, y, "8.2")
    c.drawString(320, y, "2.6 - 24.9")
    c.drawString(485, y, "N")
    y -= 20

    # ----- LIPID PROFILE -----
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.rect(50, y - 2, width - 100, 18, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(55, y + 2, "LIPID PROFILE")
    c.setFillColorRGB(0, 0, 0)
    y -= 25

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Test")
    c.drawString(200, y, "Result")
    c.drawString(320, y, "Reference")
    c.drawString(480, y, "Flag")
    y -= 14
    c.setFont("Helvetica", 9)
    c.line(50, y, 540, y)
    y -= 14

    c_flag = _flag(cholesterol, 0, 200)
    c.drawString(55, y, f"Total Cholesterol: {cholesterol} mg/dL")
    c.drawString(320, y, "< 200")
    c.drawString(485, y, c_flag)
    y -= 14

    ldl = round(cholesterol * 0.7)
    hdl = 45 if cholesterol < 200 else 38
    tg = round(cholesterol * 0.6)
    c.drawString(55, y, "LDL Cholesterol")
    c.drawString(200, y, str(ldl))
    c.drawString(320, y, "< 100")
    c.drawString(485, y, "H" if ldl > 100 else "N")
    y -= 14
    c.drawString(55, y, "HDL Cholesterol")
    c.drawString(200, y, str(hdl))
    c.drawString(320, y, "> 40 (M), > 50 (F)")
    c.drawString(485, y, "N")
    y -= 14
    c.drawString(55, y, "Triglycerides")
    c.drawString(200, y, str(tg))
    c.drawString(320, y, "< 150")
    c.drawString(485, y, "H" if tg > 150 else "N")
    y -= 20

    # ----- VITAL SIGNS & ANTHROPOMETRY -----
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.rect(50, y - 2, width - 100, 18, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(55, y + 2, "VITAL SIGNS & ANTHROPOMETRY")
    c.setFillColorRGB(0, 0, 0)
    y -= 25

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Test")
    c.drawString(200, y, "Result")
    c.drawString(320, y, "Reference")
    c.drawString(480, y, "Flag")
    y -= 14
    c.setFont("Helvetica", 9)
    c.line(50, y, 540, y)
    y -= 14

    bp_s_flag = _flag(systolic_bp, 90, 120)
    bp_d_flag = _flag(diastolic_bp, 60, 80)
    c.drawString(55, y, f"Blood Pressure: {systolic_bp}/{diastolic_bp} mmHg")
    c.drawString(320, y, "< 120 / < 80")
    c.drawString(485, y, "H" if bp_s_flag == "H" or bp_d_flag == "H" else "N")
    y -= 14

    bmi_flag = _flag(bmi, 18.5, 24.9)
    c.drawString(55, y, f"BMI: {bmi}")
    c.drawString(260, y, "kg/m2")
    c.drawString(320, y, "18.5 - 24.9")
    c.drawString(485, y, bmi_flag)
    y -= 14
    c.drawString(55, y, "Weight")
    c.drawString(200, y, f"{round(bmi * 1.7, 1)}")
    c.drawString(320, y, "As per height")
    c.drawString(485, y, "-")
    y -= 20

    # ----- ROUTINE BIOCHEMISTRY -----
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(0.2, 0.4, 0.6)
    c.rect(50, y - 2, width - 100, 18, fill=1)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(55, y + 2, "ROUTINE BIOCHEMISTRY")
    c.setFillColorRGB(0, 0, 0)
    y -= 25

    c.setFont("Helvetica-Bold", 9)
    c.drawString(50, y, "Test")
    c.drawString(200, y, "Result")
    c.drawString(320, y, "Reference")
    c.drawString(480, y, "Flag")
    y -= 14
    c.setFont("Helvetica", 9)
    c.line(50, y, 540, y)
    y -= 14

    c.drawString(55, y, "Creatinine")
    c.drawString(200, y, "0.9")
    c.drawString(320, y, "0.7 - 1.3")
    c.drawString(485, y, "N")
    y -= 14
    c.drawString(55, y, "Urea")
    c.drawString(200, y, "32")
    c.drawString(320, y, "15 - 40")
    c.drawString(485, y, "N")
    y -= 14
    c.drawString(55, y, "SGOT (AST)")
    c.drawString(200, y, "28")
    c.drawString(320, y, "0 - 40")
    c.drawString(485, y, "N")
    y -= 14
    c.drawString(55, y, "SGPT (ALT)")
    c.drawString(200, y, "35")
    c.drawString(320, y, "0 - 41")
    c.drawString(485, y, "N")
    y -= 25

    # ----- FOOTER (lab-specific director) -----
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(50, y, "N - Normal | L - Low | H - High | * Critical value")
    y -= 12
    c.drawString(50, y, "This report is valid for clinical correlation. For any query contact Lab.")
    y -= 12
    c.drawString(50, y, f"Report verified by: {lab['director']} | Lab Director")
    y -= 20
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, y, "--- End of Report ---")
    c.save()


def main() -> None:
    from datetime import date, timedelta

    base_date = date.today()
    for i, (name, age, sex, glucose, hba1c, bmi, sbp, dbp, chol, level, lab_idx) in enumerate(PROFILES):
        lab = LABS[lab_idx]
        test_date = (base_date - timedelta(days=25 * (14 - i))).strftime("%d-%b-%Y")
        report_id = f"{lab['prefix']}/{base_date.strftime('%Y%m')}/{2000 + i}"
        safe_name = "".join(c if c.isalnum() else "_" for c in name.split()[0])
        lab_short = lab["prefix"].lower()
        filename = f"lab_{lab_short}_{safe_name}_{age}y_{level}_{i + 1:02d}.pdf"
        path = OUTPUT_DIR / filename
        generate_report(
            lab=lab,
            report_id=report_id,
            patient_name=name,
            age=age,
            sex=sex,
            test_date=test_date,
            glucose=glucose,
            hba1c=hba1c,
            bmi=bmi,
            systolic_bp=sbp,
            diastolic_bp=dbp,
            cholesterol=chol,
            output_path=path,
        )
        print(f"Created: {path.name} ({lab['name'][:20]}..., {age}y, {level})")

    print(f"\nDone. {len(PROFILES)} reports from {len(LABS)} laboratories saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
