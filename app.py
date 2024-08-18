from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations
import uuid

app = Flask(__name__)
CORS(app)

executor = ThreadPoolExecutor(max_workers=4)
tasks = {}
@app.route('/submit', methods=['POST'])
def submit():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'processing'}
    
    executor.submit(process_task, task_id, data)
    
    return jsonify({'task_id': task_id, 'status': 'processing'})

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify({
        'status': task['status'],
        'result': task.get('result'),
        'error': task.get('error')
    })

def process_task(task_id, data):
    try:
        result = run_calculations(data)
        tasks[task_id] = {'status': 'completed', 'result': result}
    except Exception as e:
        tasks[task_id] = {'status': 'failed', 'error': str(e)}

def run_calculations(data):
    job_description = data.get('job_description', '')
    additional_information = data.get('additional_information', '')
    extracted_text = data.get('extractedText', '')

    final_resume = calculations.resume_final(extracted_text, additional_information)
    results = run_parallel_tasks(final_resume, job_description, extracted_text)

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
        "recommended_People_linkedin": [
            {
                "name": "John Doe",
                "title": "Senior Software Engineer",
                "link": "https://linkedin.com/in/johndoe"
            }
        ],
        "recommendedPeople_twitter": [
            {
                "name": "Jane Smith",
                "title": "Tech Recruiter",
                "link": "https://twitter.com/janesmith"
            }
        ],
        "recommendedPeople_instagram": [
            {
                "name": "Alex Johnson",
                "title": "UI/UX Designer",
                "link": "https://instagram.com/alexjohnson"
            }
        ]
    }

def run_parallel_tasks(final_resume, job_description, extracted_text):
    tasks = {
        'skills': lambda: calculations.skills_taken(final_resume, job_description),
        'projects': lambda: calculations.projects_done(final_resume, job_description),
        'courses': lambda: calculations.courses_done(final_resume, job_description),
        'experience': lambda: calculations.experience_done(final_resume, job_description),
        'score': lambda: calculations.Score_cards(extracted_text, job_description),
        'strengths': lambda: calculations.Strenths(extracted_text, job_description),
        'weakness': lambda: calculations.Worst_point(extracted_text, job_description),
        
    }
    
    futures = {executor.submit(task): key for key, task in tasks.items()}
    results = {}
    
    for future in futures:
        key = futures[future]
        try:
            results[key] = future.result()
        except Exception as exc:
            results[key] = f'Error: {exc}'

    return results

if __name__ == '__main__':
    app.run(debug=True)