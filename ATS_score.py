from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import _stop_words

def calculateATSscore(resume_data, job_description):
    stopwords = list(_stop_words.ENGLISH_STOP_WORDS)
    
    # Initialize TfidfVectorizer with stopwords
    vectorizer = TfidfVectorizer(stop_words=stopwords)
    
    # Fit and transform the job description and resume data
    vectors = vectorizer.fit_transform([job_description, resume_data])
    
    # Calculate cosine similarity
    similarity_value = cosine_similarity(vectors)
        
    # Return the ATS score rounded to two decimal places
    ats_score = round(similarity_value[0, 1], 2)
    return ats_score

def skill_gap_analysis(resume_text, required_skills):
    present_skills = [skill for skill in required_skills if skill.lower() in resume_text.lower()]
    missing_skills = [skill for skill in required_skills if skill.lower() not in resume_text.lower()]
    
    return {
        "present": present_skills,
        "missing": missing_skills
    }
