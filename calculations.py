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
 
    for attempt in range(MAX_RETRIES):
        try:
            skill = f"""{prompts.skills_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["skills"]}
            """

            skills_t = apis.final(skill)
            # Extract the relevant data
            skill_splited = skills_t.split("```")[1]
            d = json.loads(skill_splited)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    error_json = """{
        "output": {
            "skill_Score": {
            "skills_ratio": {"Something wrong": 5,"Error Continue":0,"Error Continue":0},
            "advice": "An error Occurred At this function"
            },
            "recommendations": [
            "Please Tell the author There is something wrong in this code"
            ]
        }
        }
        """
    # Return None or a default value if all attempts fail
    return json.loads(error_json)

def projects_done(resume_text,job_description):
   
    
    for attempt in range(MAX_RETRIES):
        try:
            project = f"""{prompts.project_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["projects"]}
            """

            Projects = apis.final(project)
            # Extract the relevant data
            projects_splitted = Projects.split("```")[1]
            d = json.loads(projects_splitted)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    project_error = """{
    "output": {
        "project_impact": {
        "impact": {
            "An Error Occurred": "5","Error Continue":0,"Error Continue":0
        },
        "advice": "An Error Occurred At this part.",
        "suggestion1": "Something Went Wrong!",
        "suggestion2": "Something Went Wrong!",
        "suggestion3": "Something Went Wrong!"
        }
    }
    }
    """
    return json.loads(project_error)

def courses_done(resume_text,job_description):
    

    for attempt in range(MAX_RETRIES):
        try:
            course = f"""{prompts.course_prompt}
                ###Job Description###
                {job_description}
                ###Course_Presented_In_Resume###
                {resume_text["courses"]}
            """
            
            Courses = apis.final(course)
            # Extract the relevant data
            projects_splitted = Courses.split("```")[1]
            d = json.loads(projects_splitted)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying

    course_error = """{
        "output": {
            "course_impact": {
            "impt": {
                "An Error Occurred": 0
            },
            "course_advice": "An Error Occurred At the course part please share the information with the developer.",
            "suggestion1": "An Error Occurred At the course part please share the information with the developer.",
            "suggestion2": "An Error Occurred At the course part please share the information with the developer.",
            "suggestion3": "An Error Occurred At the course part please share the information with the developer."
            }
        }
        }
    """
    return json.loads(course_error)

def experience_done(resume_text,job_description):
    
    for attempt in range(MAX_RETRIES):
        try:
            experience = f"""{prompts.exp_prompt}
                ###Job Description###
                {job_description}
                ###Experience_Presented_In_Resume###
                {resume_text["experience"]}"""
            experience1 = apis.final(experience)
            # Extract the relevant data
            exp = experience1.split("```")[1]
            d = json.loads(exp)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying

    experience_error ="""{
            "output": {
                "experience_relevance": {
                "imp": {
                    "An Error Occurred": 0
                },
                "advice": "An Error Occurred At the course part please share the information with the developer."
                },
                "Actionable Recommendations": [
                "An Error Occurred At the course part please share the information with the developer.",
                "An Error Occurred At the course part please share the information with the developer.",
                "An Error Occurred At the course part please share the information with the developer.",
                "An Error Occurred At the course part please share the information with the developer."
                ]
            }
            }"""

    
    return json.loads(experience_error)



def Score_cards(resume_text,job_description):
    
    for attempt in range(MAX_RETRIES):
        try:
            Score_card = f"""{prompts.score_card_prompt}
        ###Job Description###
        {job_description}
        ###Resume###
        {resume_text}"""
            score_cards_output = apis.final(Score_card)
            # Extract the relevant data
            exp = score_cards_output.split("```")[1]
            d = json.loads(exp)
            print(d)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    experience_error = """
            {
        "output": {
            "ats": {
            "score": 505,
            "description": "Error Occurred!",
            "reason": "An Error occurred",
            "improvementTip": "An Error occurred"
            },
            "jd": {
            "score": 505,
            "description": "Error Occurred!",
            "reason": "Error Occurred!",
            "improvementTip": "Error Occurred!"
            },
            "overall": {
            "score": 505,
            "description": "Error Occurred!",
            "reason": "Error Occurred!",
            "improvementTip": "Error Occurred!"
            },
            "ranking": {
            "score": 505,
            "description": "Error Occurred!",
            "reason": "Error Occurred!",
            "improvementTip": "Error Occurred!"
            },
            "keywords": {
            "score": 505,
            "description": "Error Occurred!",
            "reason": "Error Occurred!",
            "improvementTip": "Error Occurred!"
            }
        }
        }


        """
    return json.loads(experience_error)


def Strenths(resume_text,job_description):
    for attempt in range(MAX_RETRIES):
        try:
            Strent_prompts = f"""{prompts.Strengths}
        ###Job Description###
        {job_description}
        ###Resume###
        {resume_text}"""
            Strenths = apis.final(Strent_prompts)
            # Extract the relevant data
            exp = Strenths.split("```")[1]
            d = json.loads(exp)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    Strenths_error = """
          {
  "output": {
    "Error point 1": "An error occurred. Please inform the author.",
    "Error point 2": "An error occurred. Please inform the author.",
    "Error point 3": "An error occurred. Please inform the author."
    }
    }


        """
    return json.loads(Strenths_error)


def Worst_point(resume_text,job_description):
    for attempt in range(MAX_RETRIES):
        try:
            weekness_ponts = f"""{prompts.Weekness}
        ###Job Description###
        {job_description}
        ###Resume###
        {resume_text}"""
            worst_point = apis.final(weekness_ponts)
            # Extract the relevant data
            exp = worst_point.split("```")[1]
            d = json.loads(exp)
            return d  # Return the result if successful
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(1)  # Optional: delay before retrying
    worst_error = """
           {
    "output": {
        "Error point 1": "An error occurred. Please inform the author.",
        "Error point 2": "An error occurred. Please inform the author.",
        "Error point 3": "An error occurred. Please inform the author."
    }
    }


        """
    return json.loads(worst_error)



