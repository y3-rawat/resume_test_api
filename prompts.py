

resume_prompt1 = """
###Instruction###
Act as an expert in the field of ATS (Applicant Tracking Systems).
Your Task is to Saprate every thing from the resume 
you have to saprate these sections 
1. skills.
3. projects.
4. courses.
5. education.

###FORMAT###

Please return the extracted data in the correct JSON format:
```

{
"skills": "{only return the section of Skills of the Candidate}",
"projects": "{only return the section of Projects of the Candidate}",
"courses": "{only return the course of the Candidate }"# this includes His Graduation , Education, Certification, Courses.
"role_user_candidate": "{only return the Roles (which position in company) for the Candidate}"
"education": "{only return the section of Education of the Candidate}",
}

```
#remember json output should be correctly into json because it will be used in the code further
###Resume###

"""

resume_prompt2 = """
###Instruction###
Act as an expert in the field of ATS (Applicant Tracking Systems).
Your Task is to Saprate experience from the resume 
you have to saprate ONLY experience 


2. experience.

###FORMAT###

Please return the extracted data in the correct JSON format:
```
{

"experience": "{only return the section of Experience of the Candidate}",
}
```
#remember json output should be correctly into json because it will be used in the code further

###Resume###

"""

score_card_prompt = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide genuine scores based on the resume.

Conduct a deep-dive review of the existing resume and job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
```
{ "output":
{
           "ats_score": {
            "title": "Ats Score",
            "description": "What is the ATS Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
            "type": "integer"
        },
        "ats_description": {
            "title": "Ats Description",
            "description": "what is the potential of this resume for ATS ex ('Strong ATS compatibility potential') under 12 words",
            "type": "string"
        },
        "ats_reason": {
            "title": "Ats Reason",
            "description": "what is the reason for this score under 12 words",
            "type": "string"
        },
        "ats_improvementTip": {
            "title": "Ats Improvementtip",
            "description": "what is the improvement tip under 12 words",
            "type": "string"
        },
        "jd_score": {
            "title": "Jd Score",
            "description": "How much Job description is aligning with the resume (Score Number ex- 30, 40, 50)",
            "type": "integer"
        },
        "jd_description": {
            "title": "Jd Description",
            "description": "what is the potential of this ex ('High alignment with job description') under 12 words",
            "type": "string"
        },
        "jd_reason": {
            "title": "Jd Reason",
            "description": "what is the reason for this score for job description under 12 words",
            "type": "string"
        },
        "jd_improvementTip": {
            "title": "Jd Improvementtip",
            "description": "what is the improvement tip for resume which align with job description under 12 words",
            "type": "string"
        }
        }
            }
            ```
"""




project_prompt = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the project as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Ask for clarifications if anything is unclear or ambiguous.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
```
{ "output":
{
            "project_impact": {
                "impact": {
                    "project1": (Score Number ex- 34),
                    "project2": (Score Number ex- 27),
                    "project3": (Score Number ex- 71),
                    "project4": (Score Number ex- 52),
                    ....
                    "project n": (Score Number ex- 99)
                }, #only give the name of project and number nothting  and those which are less relevent to the job description give them less values and which are not giving any value give them 0 you can apply negetive too
                
                "advice": "advice on the projects which will make the resume out stnading from others.", # this should be consise and easy to understand 
                "suggestion1": "What needs to be done to get selected for this job description? Highlight the business impact of specific projects.", #suggestion should be seem like candidate get know something new and valueable
                "suggestion2": "Which project is not making any sense for this job description? Highlight the business impact of specific projects.",
                "suggestion3": "What keywords should be added in these projects to enhance their relevance? Highlight the business impact of specific projects."
            },}
            }
            ```
"""


skills_prompt = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the skills as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Ask for clarifications if anything is unclear or ambiguous.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The result should be in the following format:
```
{
 "output":{"skill_Score": {
        #list every skills which user has presented in resume 
        #do not add any skill which is not present in resume 
        #do not involve the skills which is present in Job description but not in the resume
            "skills_ratio": {
                "skill1": (Score Number ex- 71), 
                "skill2": (Score Number ex- 21),
                "skill3": (Score Number ex- 34), 
                "skill4": (Score Number ex- 36),
                ...
                "skill n": (Score Number ex- 23)
            }, 
            "advice": "advice on the Skills which skills will make the resume stand out  from others on the job at future (with the telling about market demand)." #keep it short and clear, 
        },
        "recommendations": [
            "recommendation1 on the Skills  ( with the telling about market demand",
            "recommendation2 on the Skills  ( with the telling about market demand",
            "recommendation3 on the Skills  ( with the telling about market demand",
            
        ],#keep it short and clear
}
}

        ```
        
        
        """


course_prompt = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the courses as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Ask for clarifications if anything is unclear or ambiguous.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.

you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the correct json  format which follow this format:
```
{ "output":
{
"course_impact":{ 
            "impt":{
            "course1": (Score Number ex- 11),
            "course2": (Score Number ex- 72),
            "course3": (Score Number ex- 19),
            ...
            "couse n ": (Score Number ex- 14
        }, # This course dosen't mean the languages it means courses like b.tech or any choching etc.
        "course_advice": "A very Sort Advice on skills.",
        "suggestion1": "what needs to be done to get selected for this job description ",
        "suggestion2":"which project is not making any sense for this job description",
        "suggestion3": "what keywords you should add in this projects "
        }
        }
        }
        ```
        if courses are not found then do not give any advice and courses will be None empty
        here are thge courses 
        
        """


exp_prompt = """
###Instruction###
act as an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the work Experience as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Ask for clarifications if anything is unclear or ambiguous.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.

you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
```
{ "output": {
"experience_relevance": {
            "imp":{
            "expeience1": (Score Number ex- 11),
            "expeience2":  (Score Number ex- 32),
            ...
            "expeience n":  (Score Number ex- 39)
                    }, #experience is a work done in the company 
        "advice": " advice on the Experiences which part on this will make the resume stand out from others on the job at future ( with the telling about market demand on future)."
                },#those experience which are not in resume do that add in this 

        "Actionable Recommendations": [
            "Recommendation1  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
            "Recommendation2  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
            "Recommendation3  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
            
        ],
        #keep it short and clear
}
}
        ```
        json format should be valid json
        """
