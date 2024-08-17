import time 
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations

app = Flask(__name__)
cors = CORS(app, resources={r"/submit": {"origins": "*"}})

# Create a global ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=4)

def run_parallel_tasks(final_resume, job_description, extracted_text):
    tasks = {
        'skills': lambda: calculations.skills_taken(final_resume, job_description),
        'projects': lambda: calculations.projects_done(final_resume, job_description),
        'courses': lambda: calculations.courses_done(final_resume, job_description),
        'experience': lambda: calculations.experience_done(final_resume, job_description),
        'score': lambda: calculations.Score_cards(extracted_text, job_description),
        'strengths': lambda: calculations.Strenths(extracted_text, job_description),
        'weakness': lambda: calculations.Worst_point(extracted_text, job_description),
        'twitter_peoples': lambda: calculations.twitter_search(extracted_text, job_description)
    }
    
    futures = {executor.submit(task): key for key, task in tasks.items()}
    results = {}
    calculations.end()
    for future in futures:
        key = futures[future]
        try:
            
            results[key] = future.result()
        except Exception as exc:
            results[key] = f'Error: {exc}'

    return results

def get_data(job_description, additional_information, extracted_text):
    final_resume = calculations.resume_final(extracted_text, additional_information)
    results = run_parallel_tasks(final_resume, job_description, extracted_text)
    time.sleep(1)
    return {
        "score_card": results['score']["score_card"],
        "project_impact": results['projects']["output"]["project_impact"],
        "skill_Score": results['skills']["output"]["skill_Score"],
        "recommendations": results['skills']["output"]["recommendations"],
        "course_impact": results['courses']["output"]["course_impact"],
        "experience_relevance": results['experience']["output"]["experience_relevance"],
        "Actionable Recommendations": results['experience']["output"]["Actionable Recommendations"],
        "Strengths": results['strengths']["output"],
        "Weaknesses": results['weakness']["output"],
        "recommended_People_linkdin": [
        {
        "name": " Doe",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        },
        
    ],


        "recommendedPeople_twitter": [
        {
        "name": "John Doe",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        }
        
    ],
    "recommendedPeople_instagram": [
        {
        "name": "John ",
        "title": "Senior Soft... ",
        "link": "https://example.com/john-doe"
        }       
        
    ],
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    job_description = request.args.get('job_description', '')
    additional_information = request.args.get('additional_information', '')
    extracted_text = request.args.get('ext-text', '')
    
    output = get_data(job_description, additional_information, extracted_text)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)