from langchain_groq import ChatGroq
import json
import apis
import prompts
import threading
from pymongo import MongoClient
import pymongo
import json
import concurrent.futures
import time
from datetime import datetime
from dotenv import load_dotenv
import os
import uuid
from pymongo.errors import BulkWriteError
TIMEOUT_SECONDS = 8  # Timeout period in seconds
load_dotenv()
db = os.getenv('mongo')

# MongoDB setup
client = MongoClient(db)  # Replace with your MongoDB connection string
db = client['db']
collection = db['Model output Data']

# Shared list to store results
results = [None, None]
results_lock = threading.Lock()  # Lock to ensure thread-safe access to results

# Maximum retry attempts
MAX_RETRIES = 1

# List to store all outputs for batch insertion
all_outputs = []
all_outputs_lock = threading.Lock()

def log_to_mongodb_batch(outputs):
    try:
        if outputs:
            # Generate unique IDs for each document
            for output in outputs:
                output['_id'] = str(uuid.uuid4())

            # Use bulk write with ordered=False to continue processing on error
            result = collection.bulk_write([
                pymongo.UpdateOne(
                    {'_id': output['_id']},
                    {'$set': output},
                    upsert=True
                ) for output in outputs
            ], ordered=False)

            print(f"Successfully processed {result.upserted_count + result.modified_count} documents")
            if result.bulk_api_result.get('writeErrors'):
                print(f"Encountered {len(result.bulk_api_result['writeErrors'])} write errors")
    except BulkWriteError as bwe:
        print(f"Bulk write error: {bwe.details}")
    except Exception as e:
        print(f"Failed to log to MongoDB: {e}")


def add_to_outputs(name, response):
    document = {
        
        "_id": str(uuid.uuid4()),
        "name": name,
        "result": response,
        'timestamp': datetime.now()
    }
    with all_outputs_lock:
        all_outputs.append(document)

def fetch_data_with_retry(prompt, index, retry_count):
    for attempt in range(retry_count):
        try:
            response = apis.final(prompt,"resume")
            add_to_outputs("resume", response)  # Add to batch instead of immediate insertion
            data = response.split("```")[1]
            with results_lock:
                results[index] = data
            return True
        except Exception as e:
            print(f"Attempt from resume {attempt + 1} failed with error: {e}")
    return False

def resume_input1(resume_text1, additional_information, index):
    resume_content_prompt1 = f"""{prompts.resume_prompt1}
    {resume_text1}
    #Additional information of candidate
    {additional_information}"""
    
    success = fetch_data_with_retry(resume_content_prompt1, index, MAX_RETRIES)
    if success:
        print("done1")
    else:
        print("Failed to process resume_text1")

def resume_input2(resume_text, additional_information, index):
    resume_content_prompt = f"""{prompts.resume_prompt2}
    {resume_text}
    #Additional information of candidate#
    {additional_information}
    ###Important Notice###
    #Do not Ignore Any thing which is present in resume includeing skills experience etc. you know every thing
    # Only add experience which user has taken from the company not from projects"""
    
    success = fetch_data_with_retry(resume_content_prompt, index, MAX_RETRIES)
    if success:
        print("done2")
    else:
        print("Failed to process resume_text")

def resume_final(resume_text, additional_information):
    start_time = time.time()
    thread1 = threading.Thread(target=resume_input1, args=(resume_text, additional_information, 0))
    thread2 = threading.Thread(target=resume_input2, args=(resume_text, additional_information, 1))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    res1 = results[0]
    res2 = results[1]

    try:
        
        res1 = json.loads(res1) if res1 else None
        res2 = json.loads(res2) if res2 else None
        if res1 and res2:
            res1["experience"] = res2["experience"]

        res1["skills"]
        res1["projects"]
        res1["courses"]
        res1["role_user_candidate"]
        res1["education"]
    except json.JSONDecodeError as e:
        print("getting problem in resume")
        print(f"JSON decoding error: {e}")
        res1 = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        res1 = resume_text
    end_time = time.time()
    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")

    return res1



def skills_taken(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "skills" not in resume_text:
                print("Invalid resume_text or missing skills")
                return None

            skill = f"""{prompts.skills_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["skills"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, skill, "skills")
                try:
                    response = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt from skills {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    
                    return json.loads("""{
                        "output": {
                            "skill_Score": {
                                "skills_ratio": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occured": 0
                                },
                                "advice": "An error Occurred At this function"
                            },
                            "recommendations": [
                                "Please Tell the author There is something wrong in this code",
                                "There is some problem from the code",
                                "Having trouble on Finding Recommendations"
                            ]
                        }
                    }""")

            # Process the response as usual
            add_to_outputs("skills_name", response)

            skill_splited = response.split("```")[1]
            d = json.loads(skill_splited)
            d["sr"]
            d["rec"]
            merged = {
                    "output": {
                        "skill_Score": {
                            "skills_ratio": d["sr"],
                        },
                        "recommendations": d["rec"]
                    }
                }
            end_time = time.time()
            time_taken = end_time - start_time
            
            # Print the time taken
            print(f"Time taken by skills Taken: {time_taken:.2f} seconds")

            return json.loads(str(merged))

        except Exception as e:
            print(f"Attempt from skills {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


            return json.loads("""{
                "output": {
                    "skill_Score": {
                        "skills_ratio": {
                            "Please Put the Complaint there is some error on this function. Skill function is not working correctly": 5,
                            "Error Continue": 0,
                            "Error Occured": 0
                        },
                        "advice": "An error Occurred At this function"
                    },
                    "recommendations": [
                        "Please Tell the author There is something wrong in this code",
                        "There is some problem from the code",
                        "Having trouble on Finding Recommendations"
                    ]
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    skills_taken_error = """{
        "output": {
            "skill_Score": {
                "skills_ratio": {
                    "Error Occured": 5,
                    "Error Continue": 0,
                    "time out ": 0
                },
                "advice": "An error Occurred At this function"
            },
            "recommendations": [
                "Please Tell the author There is something wrong in this code",
                "There is some problem from the code",
                "Having trouble on Finding Recommendations"
            ]
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(skills_taken_error)



def projects_done(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "projects" not in resume_text:
                print("Invalid resume_text or missing projects")
                return None

            project = f"""{prompts.project_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["projects"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, project, "projects")
                try:
                    Projects = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt from projects {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "output": {
                            "project_impact": {
                                "impact": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occurred": 0
                                },
                                "advice": "An error occurred At this function",
                                "suggestion1": "Please Tell the author There is something wrong in this code",
                                "suggestion2": "There is some problem from the code",
                                "suggestion3": "Having trouble on Finding Recommendations"
                            }
                        }
                    }""")

            add_to_outputs("project_name", Projects)  # Log the output to MongoDB

            projects_splitted = Projects.split("```")[1]
            d = json.loads(projects_splitted)
            md = {
                "output": {
                    "project_impact": {
                        "impact":d["imp1"],                        
                        "suggestion1": d["s1"],
                        "suggestion2": d["s2"],
                        "suggestion3": d["s3"]
                    }
                }
            }
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Projects_done: {time_taken:.2f} seconds")
            return md

        except Exception as e:
            print(f"Attempt from projects {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                "output": {
                    "project_impact": {
                        "impact": {
                            "An Error Occurred": "5",
                            "Error Continue": 0,
                            "Error Continue1": 0
                        },
                        "advice": "An Error Occurred At this part.",
                        "suggestion1": "Something Went Wrong1!",
                        "suggestion2": "Something Went Wrong2!",
                        "suggestion3": "Something Went Wrong3!"
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    project_error = """{
        "output": {
            "project_impact": {
                "impact": {
                    "Error Occurred": "5",
                    "Error Continue": 0,
                    "Error Continue1": 0
                },
                "advice": "An Error Occurred At this part.",
                "suggestion1": "Something Went Wrong1!",
                "suggestion2": "Something Went Wrong2!",
                "suggestion3": "Something Went Wrong3!"
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(project_error)



def courses_done1(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "courses" not in resume_text:
                print("Invalid resume_text or missing courses")
                return None

            course = f"""{prompts.course_prompt1}
                ###Job Description###
                {job_description}
                ###Course_Presented_In_Resume###
                {resume_text["courses"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, course, "course1")
                try:
                    Courses = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt course {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "course_impact": {
                            "impt": {
                                "time out ": 5,
                                "time out 1": 0,
                                "Error Occurred": 0
                            }
                        }
                    }""")

            add_to_outputs("course_name1", Courses)  # Log the output to MongoDB

            course_splitted = Courses.split("```")[1]
            d = json.loads(course_splitted)
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Course Done 1: {time_taken:.2f} seconds")
            merge = {
                "course_impact": {
                    "impt": d["ci"]
                    }
                }
            return merge

        except Exception as e:
            print(f"Attempt course {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                "course_impact": {
                    "impt": {
                        "An Error Occurred": 5,
                        "An Error Occurred1": 0,
                        "An Error Occurred2": 4
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    course_error = """{
        "course_impact": {
            "impt": {
                "An Error Occurred": 5,
                "An Error Occurred1": 0,
                "An Error Occurred2": 4
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(course_error)


def courses_done2(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "courses" not in resume_text:
                print("Invalid resume_text or missing courses")
                return None

            course = f"""{prompts.course_prompt2}
                ###Job Description###
                {job_description}
                ###Course_Presented_In_Resume###
                {resume_text["courses"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, course, "course2")
                try:
                    Courses = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt course {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "sugg": {
                            "suggestion1": "Time out occurred while processing.",
                            "suggestion2": "Please try again later.",
                            "suggestion3": "The system encountered a delay."
                        }
                    }""")

            add_to_outputs("course_name2", Courses)  # Log the output to MongoDB

            course_splitted = Courses.split("```")[1]
            d = json.loads(course_splitted)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by course done2: {time_taken:.2f} seconds")
            merged = {
            "sugg":
            { "suggestion1":d["s1"],
                "suggestion2": d["s2"],
                "suggestion3": d["s3"]
                }
            }
            return merged

        except Exception as e:
            print(f"Attempt course {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                "sugg": {
                    "suggestion1": "Something Went Wrong1!",
                    "suggestion2": "Something Went Wrong2!",
                    "suggestion3": "Something Went Wrong3!"
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    course_error = """{
        "sugg": {
            "suggestion1": "Something Went Wrong1!",
            "suggestion2": "Something Went Wrong2!",
            "suggestion3": "Something Went Wrong3!"
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(course_error)


def experience_done(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "experience" not in resume_text:
                print("Invalid resume_text or missing experience")
                return None

            experience = f"""{prompts.exp_prompt}
                ###Job Description###
                {job_description}
                ###Experience_Presented_In_Resume###
                {resume_text["experience"]}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, experience, "experience")
                try:
                    experience1 = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt experience {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "experience_relevance": {
                                "imp": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occurred": 0
                                },
                                "advice": "An error occurred at the experience part. Please share the information with the developer."
                            }
                          
                        }
                    }""")

            add_to_outputs("experience_name", experience1)  # Log the output to MongoDB
            exp = experience1.split("```")[1]
            d = json.loads(exp)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by experience_done: {time_taken:.2f} seconds")
            merged =  {
                "output": {
                    "experience_relevance":d["imp"]
                }
            }
            return merged

        except Exception as e:
            print(f"Attempt experience {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "experience_relevance": {
                        "imp": {
                            "An Error Occurred": 0,
                            "An Error Occurred": 0,
                            "An Error Occurred": 0
                        },
                        "advice": "An error occurred at the experience part. Please inform the author."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        "output": {
            "experience_relevance": {
                "imp": {
                    "An Error Occurred": 0,
                    "An Error Occurred": 0,
                    "An Error Occurred": 0
                },
                "advice": "An error occurred at the experience part. Please share the information with the developer."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)




def experience_done2(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "experience" not in resume_text:
                print("Invalid resume_text or missing experience")
                return None

            experience = f"""{prompts.exp_prompt2}
                ###Job Description###
                {job_description}
                ###Experience_Presented_In_Resume###
                {resume_text["experience"]}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, experience, "experience")
                try:
                    experience1 = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt experience {attempt + 1} timed out")
                    return json.loads("""{
                       "Actionable Recommendations": [
                                "Please inform the author that an error occurred.",
                                "An error occurred at the experience part. Share the information with the developer.",
                                "An error occurred at the experience part. Please provide details to the developer."
                            ]
                        }
                    """)

            add_to_outputs("experience_name", experience1)  # Log the output to MongoDB
            exp = experience1.split("```")[1]
            d = json.loads(exp)
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by experience_done: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt experience {attempt + 1} failed with error: {e}")
            return json.loads("""{                
                    "Actionable Recommendations": [
                        "An error occurred at the experience part. Share the information with the developer.",
                        "An error occurred at the experience part. Please provide details to the developer.",
                        "An error occurred at the experience part. Please inform the author."
                    ]
                }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        
            "Actionable Recommendations": [
                "An error occurred at the experience part. Share the information with the developer.",
                "An error occurred at the experience part. Please provide details to the developer.",
                "An error occurred at the experience part. Please inform the author."
            ]
        
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)




def Score_cards1(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Score_card = f"""{prompts.score_card_prompt1}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Score_card, "scores1")
                try:
                    score_cards_output = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt score {attempt + 1} timed out")
                    return json.loads("""{
                        "score_card1": {
                            "ranking": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "keywords": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            }
                        }
                    }""")

            add_to_outputs("Score_card_name1", score_cards_output)  # Log the output to MongoDB
            exp = score_cards_output.split("```")[1]
            d = json.loads(exp)

            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Score Card: {time_taken:.2f} seconds")
            
            merge_score = {
                "score_card1": 
                {
                "ranking": d["ranking"],
                "keywords":d["keywords"]
                }
                }
            return merge_score

        except Exception as e:
            print(f"Attempt score {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "score_card1": {
                    "ranking": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "keywords": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        "score_card1": {
            "ranking": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "keywords": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)


def Score_cards2(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Score_card = f"""{prompts.score_card_prompt2}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Score_card, "scores2")
                try:
                    score_cards_output = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt score {attempt + 1} timed out")
                    return json.loads("""{
                        "score_card2": {
                            "ats": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "jd": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "overall": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            }
                        }
                    }""")

            add_to_outputs("Score_card_name2", score_cards_output)  # Log the output to MongoDB
            exp = score_cards_output.split("```")[1]
            d = json.loads(exp)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Score Card 2: {time_taken:.2f} seconds")
                            
            mg_score = {
                "score_card2": 
                {
                    "ats":d["ats"],
                    "jd": 
                       d["jd"],
                    "overall": 
                        d["overall"]
                }
                }
            return mg_score

        except Exception as e:
            print(f"Attempt score {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "score_card2": {
                    "ats": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "jd": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "overall": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        "score_card2": {
            "ats": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "jd": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "overall": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")

    return json.loads(experience_error)


def Strenths(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Strent_prompts = f"""{prompts.Strengths}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Strent_prompts, "strength")
                try:
                    Strenths = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt strengths {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "Error point 1": "Time out occurred. Please try again later.",
                            "Error point 2": "Time out occurred. Please try again later.",
                            "Error point 3": "Time out occurred. Please try again later."
                        }
                    }""")

            add_to_outputs("Strent_prompts_name", Strenths)  # Log the output to MongoDB
            exp = Strenths.split("```")[1]
            d = json.loads(exp)
            d["output"]
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Strenths: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt strengths {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "Error point 1": "An error occurred. Please inform the author.",
                    "Error point 2": "An error occurred. Please inform the author.",
                    "Error point 3": "An error occurred. Please inform the author."
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    Strenths_error = """{
        "output": {
            "Error point 1": "An error occurred. Please inform the author.",
            "Error point 2": "An error occurred. Please inform the author.",
            "Error point 3": "An error occurred. Please inform the author."
        }
    }"""
    return json.loads(Strenths_error)


def Worst_point(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            weekness_ponts = f"""{prompts.Weekness}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, weekness_ponts, "weekness")
                try:
                    worst_point = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt weaknesses {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "Error point 1": "Time out occurred. Please try again later.",
                            "Error point 2": "Time out occurred. Please try again later.",
                            "Error point 3": "Time out occurred. Please try again later."
                        }
                    }""")

            add_to_outputs("weekness_ponts_name", worst_point)  # Log the output to MongoDB
            exp = worst_point.split("```")[1]
            d = json.loads(exp)
            d["output"]
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Worst point: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt weaknesses {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "Error point 1": "An error occurred. Please inform the author.",
                    "Error point 2": "An error occurred. Please inform the author.",
                    "Error point 3": "An error occurred. Please inform the author."
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    worst_error = """{
        "output": {
            "Error point 1": "An error occurred. Please inform the author.",
            "Error point 2": "An error occurred. Please inform the author.",
            "Error point 3": "An error occurred. Please inform the author."
        }
    }"""
    end_time = time.time()
    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(worst_error)
# def end():
#     log_to_mongodb_batch(all_outputs)

