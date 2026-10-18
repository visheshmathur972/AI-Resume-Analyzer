
import streamlit as st
import re
from pypdf import PdfReader

# Page settings
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Available skills
SKILLS = [
    "Python", "Java", "SQL", "HTML", "CSS",
    "JavaScript", "Machine Learning", "Data Analysis",
    "Pandas", "NumPy", "Scikit-learn", "Excel",
    "Power BI", "Tableau", "Statistics",
    "Data Visualization", "Deep Learning",
    "Git", "GitHub", "Communication"
]


def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = []

    for page in reader.pages:
        text.append(page.extract_text() or "")

    return "\n".join(text)


def find_skills(text):
    found = []
    text = text.lower()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


# Dashboard
st.title("📄 AI Resume Analyzer & Job Matcher")
st.write(
    "Upload your resume and discover how well your skills "
    "match a job description."
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("📁 Upload Resume")

    resume = st.file_uploader(
        "Choose your resume PDF",
        type=["pdf"]
    )

with right:
    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job requirements",
        placeholder=(
            "Example: We need a Data Analyst with "
            "Python, SQL, Pandas, Excel and Power BI."
        ),
        height=160
    )

analyze = st.button(
    "🔍 Analyze Resume",
    type="primary",
    use_container_width=True
)

if analyze:
    if resume is None:
        st.warning("Please upload your resume PDF.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            resume_text = extract_text(resume)

            if not resume_text.strip():
                st.error(
                    "No readable text found in this PDF. "
                    "Please use a text-based PDF."
                )

            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                matched = [
                    skill for skill in job_skills
                    if skill in resume_skills
                ]

                missing = [
                    skill for skill in job_skills
                    if skill not in resume_skills
                ]

                score = (
                    round(len(matched) / len(job_skills) * 100)
                    if job_skills else 0
                )

                st.divider()
                st.header("📊 Resume Analysis Results")
                
                st.subheader("📊 Resume Match Overview")

                c1, c2, c3 = st.columns(3)

                c1.metric("🎯 Match Score", f"{score}%")
                c2.metric("✅ Matched Skills", len(matched))
                c3.metric("📚 Missing Skills", len(missing))

                st.progress(score / 100)

                st.subheader("📈 Skills Comparison")

                chart_data = {
                    "Category": ["Matched Skills", "Missing Skills"],
                    "Count": [len(matched), len(missing)]
                }

                st.bar_chart(
                    chart_data,
                    x="Category",
                    y="Count"
                )

                

                st.subheader("✅ Skills Found in Resume")

                if resume_skills:
                    st.write(", ".join(resume_skills))
                else:
                    st.info("No recognized skills found in the resume.")

                st.subheader("🎯 Matching Skills")

                if matched:
                    st.success(", ".join(matched))
                else:
                    st.write("No matching skills found.")

                st.subheader("📚 Skills to Improve")
                
                if missing:
                    st.warning(", ".join(missing))

                    st.subheader("💡 Recommended Learning Resources")

                    resources = {
                        "Python": "Practice Python basics and functions.",
                        "SQL": "Learn SELECT, WHERE, JOIN and GROUP BY.",
                        "Pandas": "Practice DataFrames, filtering and data cleaning.",
                        "NumPy": "Learn arrays and numerical operations.",
                        "Machine Learning": "Study model training and evaluation.",
                        "Excel": "Practice formulas, PivotTables and charts.",
                        "Power BI": "Learn data modeling and dashboard creation.",
                        "Tableau": "Practice building interactive visualizations.",
                        "Statistics": "Study probability, mean, variance and correlation.",
                        "Data Analysis": "Practice EDA and finding patterns in datasets.",
                        "Data Visualization": "Learn charts using Matplotlib and Seaborn.",
                        "Scikit-learn": "Practice preprocessing, fitting and evaluating models.",
                        "Java": "Practice OOP, collections and problem-solving.",
                        "HTML": "Learn semantic elements and forms.",
                        "CSS": "Practice layouts, Flexbox and responsive design.",
                        "JavaScript": "Learn variables, functions and DOM basics.",
                        "Deep Learning": "Study neural network fundamentals.",
                        "Git": "Practice commits, branches and version control.",
                        "GitHub": "Learn repositories, README files and pull requests.",
                        "Communication": "Practice explaining technical ideas clearly."
                    }

                    for skill in missing:
                        suggestion = resources.get(
                            skill,
                            "Study the fundamentals and complete a small practice project."
                        )
                        st.write(f"**{skill}:** {suggestion}")

                else:
                    st.success("All recognized job skills are matched!")


                with st.expander("View extracted resume text"):
                    st.text(resume_text)

                st.caption(
                    "Note: This score measures matching skills only. "
                    "It does not guarantee job suitability or selection."
                )

                report = f"""
AI RESUME ANALYZER - ANALYSIS REPORT

Match Score: {score}%

Skills Found in Resume:
{", ".join(resume_skills) if resume_skills else "None"}

Matched Job Skills:
{", ".join(matched) if matched else "None"}

Skills to Improve:
{", ".join(missing) if missing else "None"}
"""

                st.download_button(
                    label="Download Analysis Report",
                    data=report,
                    file_name="resume_analysis_report.txt",
                    mime="text/plain"
                )

        except Exception as error:
            st.error(f"Could not analyze the PDF: {error}")
