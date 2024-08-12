from langchain_groq import ChatGroq
import json
import apis
import prompts
import threading
import time

# Shared list to store results
results = [None, None]
results_lock = threading.Lock()  # Lock to ensure thread-safe access to results

# Maximum retry attempts
MAX_RETRIES = 2

def fetch_data_with_retry(prompt, index, retry_count):
    for attempt in range(retry_count):
        try:
            response = apis.final(prompt)
            data = response.split("```")[1]
            with results_lock:
                results[index] = data
            return True
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    return False

def resume_input1(resume_text1,additional_information, index):
    resume_content_prompt1 = f"""{prompts.resume_prompt1}
    {resume_text1}
    #Additional information of candidate
    {additional_information}"""
    
    success = fetch_data_with_retry(resume_content_prompt1, index, MAX_RETRIES)
    if success:
        print("done1")
    else:
        print("Failed to process resume_text1")

def resume_input2(resume_text,additional_information, index):
    resume_content_prompt = f"""{prompts.resume_prompt2}
    {resume_text}
    #Additional information of candidate
    {additional_information}
    ###Important Notice###
    # Only add experience which user has taken from the company not from projects"""
    
    success = fetch_data_with_retry(resume_content_prompt, index, MAX_RETRIES)
    if success:
        print("done2")
    else:
        print("Failed to process resume_text")

def resume_final(resume_text,additional_information):
    # Create threads with an index to store results
    thread1 = threading.Thread(target=resume_input1, args=(resume_text,additional_information, 0))
    thread2 = threading.Thread(target=resume_input2, args=(resume_text,additional_information, 1))

    # Start the threads
    thread1.start()
    thread2.start()

    # Wait for both threads to complete
    thread1.join()
    thread2.join()

    # Get the results from the shared list
    res1 = results[0]
    res2 = results[1]

    # Exception handling for JSON parsing
    try:
        res1 = json.loads(res1) if res1 else None
        res2 = json.loads(res2) if res2 else None
        res1["experience"] = res2["experience"]
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        res1 = None
        res2 = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        res1 = None
        res2 = None
        
    return res1




def skills_taken(resume_text,job_description):
    skill = f"""{prompts.skills_prompt}
        ###Job Description###
        {job_description}
        ###Resume###
        {resume_text["skills"]}
    """

    for attempt in range(MAX_RETRIES):
        try:
            skills_t = apis.final(skill)
            # Extract the relevant data
            skill_splited = skills_t.split("```")[1]
            d = json.loads(skill_splited)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    error_json = """{'skill_Score': {'skills_ratio': {Please Put the Complain there is some error on this function Skill function is not working correctly: 500},
  'advice': 'An error Occured At this function'},
 'recommendations': [Please Tell the author There is something wrong in this code']}"""
    # Return None or a default value if all attempts fail
    return error_json

def projects_done(resume_text,job_description):
    project = f"""{prompts.project_prompt}
        ###Job Description###
        {job_description}
        ###Resume###
        {resume_text["projects"]}
"""

    
    for attempt in range(MAX_RETRIES):
        try:
            Projects = apis.final(project)
            # Extract the relevant data
            projects_splitted = Projects.split("```")[1]
            d = json.loads(projects_splitted)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    project_error = """
            {'project_impact': {'impact': {'An Error Occured ': 404,},
            'advice': 'An Error Occured At this part.',
            'suggestion1': 'Something Went Wrong!.',
            'suggestion2': 'Something Went Wrong!.',
            'suggestion3': "Something Went Wrong!."}}"""
    return project_error

def courses_done(resume_text,job_description):
    course = f"""{prompts.course_prompt}
        ###Job Description###
        {job_description}
        ###Course_Presented_In_Resume###
        {resume_text["courses"]}
    """
    

    for attempt in range(MAX_RETRIES):
        try:
            Courses = apis.final(course)
            # Extract the relevant data
            projects_splitted = Courses.split("```")[1]
            d = json.loads(projects_splitted)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying

    course_error = """{'course_impact': {'impt': {'An Error Occured': 60},
            'course_advice': 'An Error Occured At the course part please share the information to developer.',
            'suggestion1': 'An Error Occured At the course part please share the information to developer.',
            'suggestion2': "An Error Occured At the course part please share the information to developer.",
            'suggestion3': "An Error Occured At the course part please share the information to developer."}}"""
    
    return course_error

def experience_done(resume_text,job_description):
    experience = f"""{prompts.exp_prompt}
        ###Job Description###
        {job_description}
        ###Experience_Presented_In_Resume###
        {resume_text["experience"]}"""
    for attempt in range(MAX_RETRIES):
        try:
            experience1 = apis.final(experience)
            # Extract the relevant data
            exp = experience1.split("```")[1]
            d = json.loads(exp)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying

    experience_error = """
    {'experience_relevance': {'imp': {'An Error Occured':500},
    'advice': 'An Error Occured At the course part please share the information to developer.'},

    'Actionable Recommendations': ['An Error Occured At the course part please share the information to developer.',
    'An Error Occured At the course part please share the information to developer.',
    'An Error Occured At the course part please share the information to developer.',
    'An Error Occured At the course part please share the information to developer.']}
        
    """
    
    return experience_error



