resume_prompt1 = """
###Instruction###
You are an expert in Applicant Tracking Systems (ATS). Your task is to extract specific sections from a provided resume. The extracted sections should be formatted in JSON, following the exact structure outlined below.

###Sections to Extract###
Separate and extract the following sections from the resume:

Skills: Extract all of the technical skills which you can see in the resume.
Projects: Only return the candidate's projects section.
Courses: This includes the candidate's graduation details, education, certifications, and courses.
Role_User_Candidate: Only return the roles or positions held by the candidate in various companies.
Education: Only return the candidate's education section.
Output Format
Please return the extracted data in the correct JSON format. Ensure the JSON is enclosed within triple backticks (```), like this:
```
{
"skills": "{only return the section of Skills of the Candidate}",
"projects": "{only return the section of Projects of the Candidate}",
"courses": "{only return the course of the Candidate }"# this includes His Graduation , Education, Certification, Courses.
"role_user_candidate": "{only return the Roles (which position in company) for the Candidate}"
"education": "{only return the section of Education of the Candidate}",
}
```

###Resume###

"""

resume_prompt2 = """
###Instruction###

Act as an expert in the field of ATS (Applicant Tracking Systems).
Your Task is to Saprate experience from the resume 
you have to saprate ONLY experience 
2. experience.

###FORMAT###

Please return the extracted data in the correct JSON format do not put any points add comma insted of points :
Json should be under (```)
```
{

"experience": "{only return the section of Experience of the Candidate saprated with (,) every point will be saprated by , and if exprence is not present give None in this value }",

}
```
#remember json output should be correctly into json because it will be used in the code further
#you are in a process so do not give anything else  and json should be between ``` quotes
###Resume###

"""

score_card_prompt1 = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide genuine scores based on the resume.
Conduct a deep-dive review of the existing resume and job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
so do not give the random scores 
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
  "score_card1": 
  {

  "ranking": 
        {
          "score": "What is the Resume Ranking Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
          "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
          "reason": "Reasion under 12 words",
          "improvementTip": "Small tip on Ranking under 12 words"
        },
  "keywords":
        {
          "score": "What is the Keywords Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
          "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
          "reason": "Reasion under 12 words",
          "improvementTip": "Small tip on keywords under 12 words"
        }
  }
}


```
#remember json should be closed properly
#you are in a process so do not give anything else  and json should be between ``` quotes
"""

score_card_prompt2 = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide genuine scores based on the resume.
Conduct a deep-dive review of the existing resume and job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
so do not give the random scores 
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
 

{
  "score_card2": 
  {
    "ats":
        {
          "score":" What is the ATS Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
          "description": " Example -> Moderate ATS compatibility potential (will be change according to the score)", 
          "reason": "Reasion under 12 words",
          "improvementTip": "Small tip under 12 words"
        },
    "jd": 
        {
          "score": "What is the Job Description match Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
          "description": " Example -> Moderate ATS compatibility potential (will be change according to the score)", 
          "reason": "Reasion under 12 words",
          "improvementTip": "Small tip on aligning resume with jd under 12 words"
        },
    "overall": 
        {
          "score": "What is the Overall Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
          "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
          "reason": "Reasion under 12 words",
          "improvementTip": "Small tip on aligning everything under 12 words"
        }
  }
}
```
#remember json should be closed properly
#you are in a process so do not give anything else  and json should be between ``` quotes
"""




project_prompt = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the project as outlined in the job description.
Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
#if project is not present in the resume you have to say "Project Not preset":0 and at the section of suggestion = No Suggestions for project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "project_impact": {
            "impact": {
                "project1": (Score Number ex- 34),
                "project2": (Score Number ex- 27),
                "project3": (Score Number ex- 71),
                "project4": (Score Number ex- 52),
                ....
                "project n": (Score Number ex- 99)
            },
            "suggestion1": "What needs to be done to get selected for this job description? Highlight the business impact of specific projects.",
            "suggestion2": "Which project is not making any sense for this job description? Highlight the business impact of specific projects.",
            "suggestion3": "What keywords should be added in these projects to enhance their relevance? Highlight the business impact of specific projects."
        }
    }
}            
            ```
            points to be remember 
            #suggestions should be very short and clear try to put that into 15-20 words do not repeat things this part should be strongly focus on projects
            #suggestion should be seem like candidate get know something new and valueable
             #only give the name of project and number nothting  and those which are less relevent to the job description give them less values and which are not giving any value give them 0 you can apply negetive too
            #remember json should be closed properly
"""


skills_prompt = """
###Instruction###
You are an expert in ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description.

Goals:
Evaluate the Resume: Conduct a detailed review of the user's resume against the provided job description.
Provide Feedback: Offer actionable advice to enhance the resume and address skills discrepancies.
Focus on Skills: Ensure feedback and scoring reflect the skills outlined in the job description.

Requirements:

Skill Scoring: Score each skill listed in the job description based on its presence and relevance in the resume. Provide these scores in a JSON format.
Recommendations: Offer concise, actionable recommendations focused on skill improvement, and include market demand insights.

Instructions for JSON Output:
Skills Included: List only those skills present in the resume.
Skills Excluded: Do not include skills from the job description that are not found in the resume.
No Skill Found Case: If no skills from the job description are present in the resume just tell in json that "No skill found":0 
Recommendations: Keep them brief (15-20 words), focusing on skill improvement and market demand.

Note:
 Provide no additional information or analysis beyond the required JSON output.


###FORMAT###
The result should be in the following format:
Json should be under (```)
```
{
    "output": {
        "skill_Score": {
            "skills_ratio": {
                "skill1": (Score Number ex- 71),
                "skill2": (Score Number ex- 21),
                "skill3": (Score Number ex- 34),
                "skill4": (Score Number ex- 36),
                ...
                "skill n": (Score Number ex- 23)
            }
        },
        "recommendations": [
            "recommendation1 on the Skills  ( with the telling about market demand)",
            "recommendation2 on the Skills  ( with the telling about market demand)",
            "recommendation3 on the Skills  ( with the telling about market demand)"
        ]
    }
}
```
        """


course_prompt1 = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
 Your task is to evaluate a user's resume courses against a provided job description.
   You will provide excellent advice and genuine scores based on the resume course, focusing on the impacts on the courses as outlined in the job description.

Conduct a deep-dive review of the existing courses of resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.


###FORMAT###
The output should be in the correct json  format which follow this format:
Json should be under (```)
```
{

  "course_impact": {
      "impt": {
          "course1": (Score Number ex- 11),
          "course2": (Score Number ex- 72),
          "course3": (Score Number ex- 19),
          ...
          "couse n ": (Score Number ex- 14)
      }
          
    }
}
```
you are the part of process so do not give any thing else it do not give any value and it will increase the output time
#if you didn't find any courses on resume just give in json "No courses found" : 0 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
        """

course_prompt2 = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
 Your task is to evaluate a user's resume courses against a provided job description.
   You will provide excellent advice and genuine scores based on the resume course, focusing on the impacts on the courses as outlined in the job description.

Conduct a deep-dive review of the existing courses of resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.


###FORMAT###
The output should be in the correct json  format which follow this format:
Json should be under (```)
```
{
"sugg":
   { "suggestion1": "what needs to be done to get selected for this job description ",
      "suggestion2": "which project is not making any sense for this job description",
      "suggestion3": "what keywords you should add in this projects "
    }
}
```
you are the part of process so do not give any thing else it do not give any value and it will increase the output time
#if you didn't find any courses on resume just give in json "No courses found" : 0 
#do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
#it suggestions should be short clear and understandable it should be only within 12-20 words 
        """


exp_prompt = """
###Instruction###
act as an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the work Experience as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.

you are the part of process so do not give any thing else it do not give any value to that project 
if you didn't find any experience on resume just give in json "No expereince found":0
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "experience_relevance": {
            "imp": {
                "expeience name 1": (Score Number ex- 11),
                "expeience name 2":  (Score Number ex- 32),
                ...
                "expeience name  n":  (Score Number ex- 39)
            }
        },
        "Actionable Recommendations": [
            "Recommendation1  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
            "Recommendation2  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
            "Recommendation3  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future)."
        ]
    }
}
        ```
        #json format should be valid json
         #experience is a work done in the company 
         #suggestions should be very short and clear try to put that into 15-20 words and it should be focused on what can be achive in short period nothing should sound ideal
        """

Strengths = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
Your task is to evaluate a user's resume against a provided job description. 
You will provide excellent advice based on the resume, 
focusing on the impacts on the Strengths of resume as outlined in the job description.

Conduct a deep-dive review of the resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to give the best part of resume for the job desciption.
you are the part of process so do not give any thing else it do not give any value to that project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "Strenght point 1": "Brief on Strenght point 1 (it should be very clear, Sort ,Valid).",
        "Strenght point 2": "Brief on Strenght point 2 (it should be very clear, Sort ,Valid).",
        "Strenght point 3": "Brief on Strenght point 3 (it should be very clear, Sort ,Valid)."
    }
}


```
#it should be very short and clear try to put every point into 12-15 words
#remember json should be closed properly
#i want only 3-4 points
"""



Weekness = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
Your task is to evaluate a user's resume against a provided job description. 
You will provide excellent advice based on the resume, 
focusing on the impacts on the Strengths of resume as outlined in the job description.

Conduct a deep-dive review of the resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to give the Worst part of resume for the job desciption.
you are the part of process so do not give any thing else it do not give any value to that project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "Worst point name": "Brief on Worst point 1 (it should be very clear, Sort ,Valid).",
        "Worst point name": "Brief on Worst point 2 (it should be very clear, Sort ,Valid).",
        "Worst point name": "Brief on Worst point 3 (it should be very clear, Sort ,Valid)."
    }
}
```
#it should be very short and clear try to put every point into 12-15 words
#remember json should be closed properly
i want only 3-4 points
"""
