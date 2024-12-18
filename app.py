import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from convert import ExtractPDFText
from ATS_score import calculateATSscore, skill_gap_analysis
from model import modelFeedback
import time

# Streamlit app title
st.title("Resume Screening Assistance")

# Define required skills for the job
required_skills = ["Python", "Machine Learning", "Cloud (AWS/Azure)", "Data Analysis", "React", "Docker"]

# Job Description Input
job_description = st.text_area("Paste the job description below:", placeholder="Enter the job description here...")

# Upload Resumes
uploaded_files = st.file_uploader("Upload your resumes (PDF only):", type="pdf", accept_multiple_files=True)

# Add a submit button
if st.button("Submit"):
    if uploaded_files and job_description:
        resumes_data = []

        # Initialize progress bar
        progress_bar = st.progress(0)
        total_resumes = len(uploaded_files)

        # Placeholder to show the current processing file
        current_file_placeholder = st.empty()

        for idx, file in enumerate(uploaded_files, start=1):
            try:
                # Update the current file being processed in the placeholder
                current_file_placeholder.text(f"Currently processing: {file.name}")

                # Extract resume text
                text = ExtractPDFText(file)

                # Calculate ATS score and skill gap analysis
                ats_score = calculateATSscore(text, job_description)
                skill_analysis = skill_gap_analysis(text, required_skills)

                # Generate AI feedback
                feedback = modelFeedback(ats_score, text, job_description)

                # Append results for each resume
                resumes_data.append({
                    "name": file.name,
                    "ATS Score": ats_score,
                    "Skills Present": skill_analysis["present"],
                    "Missing Skills": skill_analysis["missing"],
                    "Feedback": feedback
                })

                # Update progress bar
                progress_bar.progress(idx / total_resumes)

            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        # Clear the current file placeholder after processing all files
        current_file_placeholder.empty()

        if resumes_data:
            # Sort resumes by ATS score
            sorted_resumes = sorted(resumes_data, key=lambda x: x["ATS Score"], reverse=True)

            # Add rankings
            for rank, resume in enumerate(sorted_resumes, start=1):
                resume["Rank"] = rank

            # Display results
            st.subheader("Top Matches:")
            for resume in sorted_resumes:
                st.write(f"#### Rank {resume['Rank']}: {resume['name']}")
                st.write(f"**ATS Score:** {resume['ATS Score']*100:.0f}%")
                st.write("**Missing Skills:**", ", ".join(resume["Missing Skills"]) if resume["Missing Skills"] else "None")
                st.write("**Feedback:**")
                st.markdown(f"> {resume['Feedback']}")
                st.write("---")

            # Skill Gap Analysis Table
            st.subheader("Skill Gap Analysis")
            for resume in sorted_resumes:
                st.write(f"**{resume['name']} (Rank {resume['Rank']})**")
                skill_data = {
                    "Required Skills": required_skills,
                    "Present in Resume": ["✅" if skill in resume["Skills Present"] else "❌" for skill in required_skills],
                    "Missing": [skill if skill in resume["Missing Skills"] else "—" for skill in required_skills]
                }
                df = pd.DataFrame(skill_data)
                st.table(df)

            # Visualize ATS Scores with Rankings
            st.subheader("ATS Score Distribution")
            names_with_ranks = [f"Rank {r['Rank']}: {r['name']}" for r in sorted_resumes]
            scores = [r["ATS Score"]*100 for r in sorted_resumes]
            plt.figure(figsize=(8, 5))
            plt.bar(names_with_ranks, scores, color='skyblue')
            plt.title("ATS Scores by Resume (Ranked)")
            plt.ylabel("ATS Score (%)")
            plt.xticks(rotation=45, ha="right")
            st.pyplot(plt)
        else:
            st.error("No resumes could be processed. Please check the uploaded files.")

    else:
        st.warning("Please upload resumes and provide a job description before submitting.")
