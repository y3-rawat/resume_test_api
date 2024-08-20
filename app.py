import time
import threading
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations
import apis

app = Flask(__name__)
cors = CORS(app, resources={r"/submit": {"origins": "*"}})
executor = ThreadPoolExecutor(max_workers=4)

# Global variable to keep track of the server start time
start_time = time.time()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

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
            print("Result of -> ", key)
        except Exception as exc:
            results[key] = f'Error: {exc}'
            print("getting error --35")

    return results

def get_data(job_description, additional_information, extracted_text):
    final_resume = calculations.resume_final(extracted_text, additional_information)
    results = run_parallel_tasks(final_resume, job_description, extracted_text)
    time.sleep(1)
    print("-----------Mongo DB-----------")
    calculations.end()
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
                "name": "Doe",
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
                "name": "John",
                "title": "Senior Soft... ",
                "link": "https://example.com/john-doe"
            }
        ],
    }

@app.route('/submit', methods=['POST'])
def submit():
    job_description = request.args.get('job_description', '')
    additional_information = request.args.get('additional_information', '')
    extracted_text = request.args.get('ext-text', '')
    api_key = request.args.get('api', '')  # Use api_key for clarity
    apis.API_func(api_key)
    output = get_data(job_description, additional_information, extracted_text)
    return jsonify(output)

def print_elapsed_time():
    while True:
        elapsed_time = time.time() - start_time
        print(f"Server running for: {elapsed_time:.2f} seconds")
        time.sleep(1)

if __name__ == '__main__':
    # Start the elapsed time printing in a separate thread
    threading.Thread(target=print_elapsed_time, daemon=True).start()
    app.run(debug=True)
