# MedGuardian — Remaining Tasks for Submission

This document lists tasks you should complete before final submission.

---

## 1. Fill Placeholders

Replace the following placeholders in the report and presentation:

| Placeholder | Where | Example |
|-------------|-------|---------|
| `[College Name (Full)]` | Report, Presentation | Dhanraj Baid Jain College (Autonomous) |
| `[College Address, City – PIN]` | Report | Thoraipakkam, Chennai – 600097 |
| `[NAAC Accredited / Affiliated to...]` | Report | Affiliated to University of Madras |
| `[Your Full Name]` | Report, Presentation | John Doe |
| `[Your Roll No]` | Report, Presentation | 21BCS001 |
| `[Guide Name]` | Report, Presentation | Dr. Jane Smith |
| `[Guide Designation]` | Report | Assistant Professor, Department of Computer Science |
| `[Academic Year]` | Report, Presentation | 2024 – 2025 |
| `[Date]` | Certificate, Declaration | 15 March 2025 |
| `[College URL]` | References | https://www.yourcollege.ac.in |

---

## 2. Add Table of Contents (TOC)

For the report, add a Table of Contents after the Acknowledgement. In Markdown, you can use:

```markdown
# Table of Contents

1. [Abstract](#abstract)
2. [List of Abbreviations](#list-of-abbreviations)
3. [Chapter 1: Introduction](#chapter-1-introduction)
...
```

Or use Pandoc's `--toc` flag when generating DOCX (see below).

---

## 3. Add Screenshots

In **Chapter 8: Results**, add screenshots of:

- Home page
- Patient Profile (new patient form)
- Upload Report (PDF upload + parsed biomarkers)
- Risk Dashboard (gauge charts)
- History page (trend charts)

Place images in a folder (e.g. `screenshots/`) and reference them:

```markdown
![Home Page](screenshots/home.png)
```

---

## 4. Signatures

- Get the **Bonafide Certificate** signed by your guide
- Sign the **Declaration** yourself
- Add dates where indicated

---

## 5. Export Report to DOCX

Install [Pandoc](https://pandoc.org/installing.html), then run:

```bash
cd E:\OneDrive\Glor\Others-Project\MedGuardian
pandoc MedGuardian_Project_Report.md -o MedGuardian_Project_Report.docx --toc --toc-depth=3
```

Options:
- `--toc` — Add table of contents
- `--toc-depth=3` — Include headings up to level 3
- `--reference-doc=template.docx` — Use a custom Word template (optional)

---

## 6. Export Presentation to PPTX (Marp)

Install Marp CLI:

```bash
npm install -g @marp-team/marp-cli
```

Then:

```bash
cd E:\OneDrive\Glor\Others-Project\MedGuardian
marp MedGuardian_Presentation.md -o MedGuardian_Presentation.pptx
```

Or use the [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) extension and export from the editor.

---

## 7. Verify Application

- [ ] Run `streamlit run app.py` locally
- [ ] Load sample data and test all pages
- [ ] Upload a sample PDF (text-based) and verify parsing
- [ ] Compute risk scores and view History
- [ ] Test Streamlit Cloud deployment (optional)

---

## 8. Final Checklist

- [ ] All placeholders filled
- [ ] TOC added to report
- [ ] Screenshots inserted
- [ ] Bonafide certificate and Declaration signed
- [ ] Report exported to DOCX
- [ ] Presentation exported to PPTX
- [ ] Code pushed to GitHub (if deploying to Streamlit Cloud)
