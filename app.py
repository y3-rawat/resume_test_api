from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations
import uuid

app = Flask(__name__)

cors = CORS(app, resources={r"/submit": {"origins": "*"}, r"/status/<task_id>": {"origins": "*"}})

executor = ThreadPoolExecutor(max_workers=4)
tasks = {}
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json() if request.is_json else request.form.to_dict()
    
    task_id = str(uuid.uuid4())
    tasks[task_id] = {'status': 'processing'}
    
    executor.submit(process_task, task_id, data)
    
    return jsonify({'task_id': task_id, 'status': 'processing'})

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(task)

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
        print(f"Error processing task {task_id}: {str(e)}")
        tasks[task_id] = {'status': 'failed', 'error': str(e)}

def run_calculations(data):
    job_description = data.get('job_description', '')
    additional_information = data.get('additional_information', '')
    extracted_text = data.get('extractedText', '')

    final_resume = resume_final(extracted_text, additional_information)
    if not final_resume:
        raise ValueError("Failed to generate final resume")

    results = run_parallel_tasks(final_resume, job_description, extracted_text)

    return {
        "score_card": results.get('score', {}).get("score_card", {}),
        "project_impact": results.get('projects', {}).get("output", {}).get("project_impact", {}),
        "skill_Score": results.get('skills', {}).get("output", {}).get("skill_Score", {}),
        "recommendations": results.get('skills', {}).get("output", {}).get("recommendations", []),
        "course_impact": results.get('courses', {}).get("output", {}).get("course_impact", {}),
        "experience_relevance": results.get('experience', {}).get("output", {}).get("experience_relevance", {}),
        "Actionable Recommendations": results.get('experience', {}).get("output", {}).get("Actionable Recommendations", []),
        "Strengths": results.get('strengths', {}).get("output", {}),
        "Weaknesses": results.get('weakness', {}).get("output", {}),
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
        'skills': lambda: skills_taken(final_resume, job_description),
        'projects': lambda: projects_done(final_resume, job_description),
        'courses': lambda: courses_done(final_resume, job_description),
        'experience': lambda: experience_done(final_resume, job_description),
        'score': lambda: Score_cards(extracted_text, job_description),
        'strengths': lambda: Strenths(extracted_text, job_description),
        'weakness': lambda: Worst_point(extracted_text, job_description),
    }
    
    results = {}
    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_task = {executor.submit(task): key for key, task in tasks.items()}
        for future in as_completed(future_to_task):
            key = future_to_task[future]
            try:
                results[key] = future.result()
            except Exception as exc:
                print(f'{key} generated an exception: {exc}')
                results[key] = f'Error: {exc}'
    
    return results

if __name__ == '__main__':
    app.run(debug=True)