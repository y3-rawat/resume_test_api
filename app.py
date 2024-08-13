from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from concurrent.futures import ProcessPoolExecutor, as_completed

import calculations


app = Flask(__name__)
# Configure CORS with specific options
cors = CORS(app, resources={
    r"/submit": {"origins": "*"}  # Allow all origins for the /submit endpoint
})





def run_parallel_tasks(final_resume, job_description):
    # Define the tasks
    tasks = {
        'skills': lambda: calculations.skills_taken(final_resume, job_description=job_description),
        'projects': lambda: calculations.projects_done(final_resume, job_description),
        'courses': lambda: calculations.courses_done(final_resume, job_description=job_description),
        'experience': lambda: calculations.experience_done(final_resume, job_description)
    }
    
    # Create a ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        # Submit tasks and get futures
        futures = {executor.submit(task): key for key, task in tasks.items()}
        
        # Collect results as they complete
        results = {}
        for future in as_completed(futures):
            key = futures[future]
            try:
                results[key] = future.result()
            except Exception as exc:
                results[key] = f'Error: {exc}'

    return results



def get_data(job_description,additional_information,experience,extreacted_text):
    
    print("resume text",extreacted_text)
    final_resume = calculations.resume_final(extreacted_text,additional_information)

    results = run_parallel_tasks(final_resume, job_description)

    
    skills = results['skills']
    projects = results['projects']
    courses = results['courses']
    experiencee = results['experience']
    
    data = {
        "score_card": {
            "ats": {
                "score": 42,
                "description": "Moderate ATS compatibility potential",
                "reason": "Lack of direct keyword matches",
                "improvementTip": "Use more job-specific keywords"
            },
            "jd": {
                "score": 51,
                "description": "Fair job description alignment",
                "reason": "Insufficient experience in data engineering",
                "improvementTip": "Highlight relevant data engineering experience"
            },
            "overall": {
                "score": 46,
                "description": "Average overall potential",
                "reason": "Limited direct experience in required skills",
                "improvementTip": "Emphasize transferable skills and education"
            },
            "ranking": {
                "score": 38,
                "description": "Below-average ranking potential",
                "reason": "Lack of strong mathematical modeling experience",
                "improvementTip": "Develop and showcase mathematical modeling skills"
            },
            "keywords": {
                "score": 55,
                "description": "Good keyword presence",
                "reason": "Some relevant technical skills mentioned",
                "improvementTip": "Use more specific and relevant keywords"
            }
        },
        "project_impact": projects["output"]["project_impact"],
        
        "skill_Score": skills["output"]["skill_Score"],
        "recommendations": skills["output"]["recommendations"],
        "course_impact": courses["output"]["course_impact"],
        "experience_relevance": experiencee["output"]["experience_relevance"],
        "Actionable Recommendations": experiencee["output"]["Actionable Recommendations"],
        
                "Strengths":{
                        "Relevant Education":" The candidate is pursuing a Bachelor's degree in AI & DS, which aligns with the job requirements.",
                        "AI/ML Experience":"The candidate has experience in AI/ML through various projects, internships, and certifications, which is a significant strength for this role.",
                        "Technical Skills":"The candidate has a good foundation in technical skills required for the job, including ML, NLP, LLM, Python, SciKit Learn, Pandas, and Matplotlib.",
                        },
                    "Weaknesses":{
                        "Lack of Direct Experience": "Although the candidate has experience in AI/ML, they lack direct experience in Gen AI development, deployment, and pipeline creation, which is a critical requirement for the job.",
                        "Limited Industry Experience" : "The candidate's experience is mostly limited to internships and personal projects, which may not be sufficient to meet the job's requirements.",
                        "No Mention of Model Development or Evaluation" : "The candidate's resume does not explicitly mention experience in model development, evaluation, or deployment, which are essential skills for the job."
                    },

        
        "recommended_People_linkdin": [
        {
        "name": " Doe",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Soft....",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Software Engineer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },

        
    ],

    
        "recommendedPeople_twitter": [
        {
        "name": "John Doe",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Soft....",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Software Engineer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        
        
    ],
    "recommendedPeople_instagram": [
        {
        "name": "John ",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Soft....",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "John Doe",
        "title": "Senior Software Engineer",
        "link": "https://example.com/john-doe"
        },
        {
        "name": "Jane Smith",
        "title": "UX Designer",
        "link": "https://example.com/john-doe"
        },
        
        
    ],

    
    }

    return jsonify(data)




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    file_name = request.args.get('fileName', '')
    file_type = request.args.get('fileType', '')
    job_description = request.args.get('job_description', '')
    additional_information = request.args.get('additional_information', '')
    experience = request.args.get('experience', '')
    extreacted_text = request.args.get('ext-text', '')
    
    output = get_data(job_description,additional_information,experience,extreacted_text)


    return output


    # # Create a response dictionary
    # response ={
    #    'fileName': file_name,
    #     'fileType': file_type,
    #     'job_description': job_description,
    #     'additional_information': additional_information,
    #     'experience': experience,
    #     'extracted_text':extreacted_text,
    # }
    
    # data = {'score_card': {'ats': {'score': 42,
    # 'description': 'Moderate ATS compatibility potential',
    # 'reason': 'Lack of direct keyword matches',
    # 'improvementTip': 'Use more job-specific keywords'},
    # 'jd': {'score': 51,
    # 'description': 'Fair job description alignment',
    # 'reason': 'Insufficient experience in data engineering',
    # 'improvementTip': 'Highlight relevant data engineering experience'},
    # 'overall': {'score': 46,
    # 'description': 'Average overall potential',
    # 'reason': 'Limited direct experience in required skills',
    # 'improvementTip': 'Emphasize transferable skills and education'},
    # 'ranking': {'score': 38,
    # 'description': 'Below-average ranking potential',
    # 'reason': 'Lack of strong mathematical modeling experience',
    # 'improvementTip': 'Develop and showcase mathematical modeling skills'},
    # 'keywords': {'score': 55,
    # 'description': 'Good keyword presence',
    # 'reason': 'Some relevant technical skills mentioned',
    # 'improvementTip': 'Use more specific and relevant keywords'}},
    # 'project_impact': {'impact': {"HEALTH-RELATED PROBLEM'S SOLUTION CHAT-BOT": 42,
    # 'VoiceFlow Microsoft Points Generator Program': 18,
    # 'Instagram Reels to YouTube Shorts Uploader': 10},
    # 'advice': 'To make the resume stand out, focus on showcasing projects that demonstrate expertise in data engineering, machine learning, and statistical analysis.',
    # 'suggestion1': "Highlight the business impact of the HEALTH-RELATED PROBLEM'S SOLUTION CHAT-BOT project by explaining how it utilizes data mining and predictive modeling skills to solve real-world problems.",
    # 'suggestion2': "Consider removing or minimizing the VoiceFlow Microsoft Points Generator Program project as it doesn't seem to be directly related to the data engineer role.",
    # 'suggestion3': "Add keywords like 'data engineering', 'machine learning', 'natural language processing' to the HEALTH-RELATED PROBLEM'S SOLUTION CHAT-BOT project to enhance its relevance to the job description."},
    # 'skill_Score': {'skills_ratio': {'Python': 85,
    # 'C++': 20,
    # 'SQL': 40,
    # 'TensorFlow': 60,
    # 'PyTorch': 50,
    # 'Scikit-Learn': 70,
    # 'LangChain': 30,
    # 'LlamaIndex': 25,
    # 'Flask': 45,
    # 'CrewAI': 20,
    # 'AWS': 55,
    # 'GCP': 40,
    # 'Machine Learning': 80,
    # 'Data Warehousing': 35,
    # 'LLM': 40,
    # 'Statistics': 60,
    # 'Data Analysis': 75,
    # 'ETL': 50,
    # 'Automation': 45,
    # 'Deeplearning': 65},
    # 'advice': 'To make the resume stand out, consider highlighting expertise in PySpark, data mining, and predictive modeling skills, as these are in high demand in the industry. Additionally, emphasizing experience in mathematical modeling, statistics, and analytics will be beneficial.'},
    # 'recommendations': ['Consider adding experience in data mining and statistical analysis to the resume, as these skills are highly valued in the industry.',
    # 'Highlighting experience in mathematical modeling and predictive modeling skills will make the resume more competitive.',
    # 'Emphasizing expertise in PySpark and other relevant programming languages will be beneficial for the Data Engineer role.'],
    # 'course_impact': {'impt': {'AI&DS Certification': 80,
    # 'Data Analysis': 70,
    # 'Career Edge - Young Professional': 40},
    # 'course_advice': "To make the resume stand out, it's recommended to pursue courses in Machine Learning, Computer Vision, and NLP, as these skills are in high demand in the industry. Additionally, having a strong foundation in statistics and algebra will be beneficial. With the growing use of big data, having experience in data mining and predictive modeling will also be valuable.",
    # 'suggestion1': "To get selected for this job description, it's essential to highlight hands-on experience in programming languages such as Python/Java and PySpark. Emphasize experience in data mining, statistical analysis, and predictive modeling skills.",
    # 'suggestion2': "The 'Career Edge - Young Professional' course may not be directly relevant to the job description. Consider replacing it with a more relevant course or certification.",
    # 'suggestion3': "Add keywords such as 'Machine Learning', 'Computer Vision', 'NLP', 'data mining', and 'predictive modeling' to the projects to increase visibility in the ATS."},
    # 'experience_relevance': {'imp': {'Query Solving System without Chatgpt API': 8,
    # 'Diffrent Chatbots with AI': 6,
    # 'Question Generation System': 9,
    # 'Resume Parsing Module': 8,
    # 'HEALTH-RELATED PROBLEM’S SOLUTION CHAT-BOT': 7,
    # 'Microsoft Points Generator Program': 5,
    # 'Instagram Reels to YouTube Shorts Uploader': 4},
    # 'advice': 'The candidate has demonstrated a strong foundation in AI and ML, with a focus on chatbots and natural language processing. To further enhance their resume, it would be beneficial to highlight more experience in data engineering, mathematical modeling, and statistical analysis, as these skills are highly valued in the data engineer role. Additionally, showcasing experience with programming languages such as Java and PySpark would be advantageous.'},
    # 'Actionable Recommendations': ['Consider taking courses or gaining experience in data engineering, mathematical modeling, and statistical analysis to enhance your skillset.',
    # 'Highlight any experience with Java and PySpark in your resume, as these skills are highly valued in the data engineer role.',
    # 'Emphasize your ability to solve problems with analytical thinking and conceptualize, design, and build models from scratch.',
    # "Quantify your achievements by including specific numbers and metrics wherever possible, such as '30% reduction in interview time' or '40% reduction in patient complaints'.",
    # 'Tailor your resume to the specific job description by highlighting relevant skills and experiences, and using keywords from the job posting.'],
    # 'Strengths': {'Relevant Education': " The candidate is pursuing a Bachelor's degree in AI & DS, which aligns with the job requirements.",
    # 'AI/ML Experience': 'The candidate has experience in AI/ML through various projects, internships, and certifications, which is a significant strength for this role.',
    # 'Technical Skills': 'The candidate has a good foundation in technical skills required for the job, including ML, NLP, LLM, Python, SciKit Learn, Pandas, and Matplotlib.'},
    # 'Weaknesses': {'Lack of Direct Experience': 'Although the candidate has experience in AI/ML, they lack direct experience in Gen AI development, deployment, and pipeline creation, which is a critical requirement for the job.',
    # 'Limited Industry Experience': "The candidate's experience is mostly limited to internships and personal projects, which may not be sufficient to meet the job's requirements.",
    # 'No Mention of Model Development or Evaluation': "The candidate's resume does not explicitly mention experience in model development, evaluation, or deployment, which are essential skills for the job."},
    # 'recommended_People_linkdin': [{'name': ' Doe',
    # 'title': 'Senior Soft... ',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Soft....',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Software Engineer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'}],
    # 'recommendedPeople_twitter': [{'name': 'John Doe',
    # 'title': 'Senior Soft... ',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Soft....',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Software Engineer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'}],
    # 'recommendedPeople_instagram': [{'name': 'John ',
    # 'title': 'Senior Soft... ',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Soft....',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'John Doe',
    # 'title': 'Senior Software Engineer',
    # 'link': 'https://example.com/john-doe'},
    # {'name': 'Jane Smith',
    # 'title': 'UX Designer',
    # 'link': 'https://example.com/john-doe'}]}
    
    # Return a JSON response
    # return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
