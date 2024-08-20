import time 
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations
import concurrent.futures

app = Flask(__name__)
cors = CORS(app, resources={r"/submit": {"origins": "*"}})
api = None
executor = ThreadPoolExecutor(max_workers=6)

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
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_key = {executor.submit(task): key for key, task in tasks.items()}
        
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
                print(f"Completed: {key}")
            except Exception as exc:
                results[key] = None
                print(f"Error in {key}: {exc}")
    
    return results

def get_data(job_description, additional_information, extracted_text):
    final_resume = calculations.resume_final(extracted_text, additional_information)
    if final_resume is None:
        return jsonify({"error": "Failed to process resume"}), 400

    results = run_parallel_tasks(final_resume, job_description, extracted_text)
    time.sleep(1)
    print("-----------Mongo DB-----------")
    calculations.end()

    # Define default error response
    error_response = {
        "error": "An error occurred while processing the data",
        "details": {}
    }

    # Helper function to safely get nested dictionary values
    def safe_get(dict_obj, *keys):
        for key in keys:
            if dict_obj is not None and isinstance(dict_obj, dict) and key in dict_obj:
                dict_obj = dict_obj[key]
            else:
                return None
        return dict_obj

    # Populate the response, using error messages for any missing data
    response = {
        "score_card": safe_get(results, 'score', "score_card") or error_response["details"].setdefault("score_card", "Failed to calculate score"),
        "project_impact": safe_get(results, 'projects', "output", "project_impact") or error_response["details"].setdefault("project_impact", "Failed to analyze projects"),
        "skill_Score": safe_get(results, 'skills', "output", "skill_Score") or error_response["details"].setdefault("skill_Score", "Failed to analyze skills"),
        "recommendations": safe_get(results, 'skills', "output", "recommendations") or error_response["details"].setdefault("recommendations", "No recommendations available"),
        "course_impact": safe_get(results, 'courses', "output", "course_impact") or error_response["details"].setdefault("course_impact", "Failed to analyze courses"),
        "experience_relevance": safe_get(results, 'experience', "output", "experience_relevance") or error_response["details"].setdefault("experience_relevance", "Failed to analyze experience"),
        "Actionable Recommendations": safe_get(results, 'experience', "output", "Actionable Recommendations") or error_response["details"].setdefault("Actionable Recommendations", "No actionable recommendations available"),
        "Strengths": safe_get(results, 'strengths', "output") or error_response["details"].setdefault("Strengths", "Failed to identify strengths"),
        "Weaknesses": safe_get(results, 'weakness', "output") or error_response["details"].setdefault("Weaknesses", "Failed to identify weaknesses"),
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

    # If any errors occurred, include them in the response
    if error_response["details"]:
        response["errors"] = error_response["details"]

    return response

import apis

@app.route('/submit', methods=['POST'])
def submit():
    try:
        job_description = request.args.get('job_description', '')
        additional_information = request.args.get('additional_information', '')
        extracted_text = request.args.get('ext-text', '')
        api_key = request.args.get('api', '')
        apis.API_func(api_key)
        output = get_data(job_description, additional_information, extracted_text)
        return jsonify(output)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)