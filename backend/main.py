from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
import logging
from database import get_db_connection  
import json

# Initialize the Gemini client
client = genai.Client(api_key='AIzaSyAITFWaOXPP6FQpDvI_fo7JchQGxxj7TXg')

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from this specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Function to extract resume details using Gemini
def extract_resume_details(resume_text):
    prompt = f"""
    Extract the following details from the given resume or CV and provide them in this Json format which can be saved as json file:
    name: ...
    email: ...
    contact no: ...
    education: ...
    profession: ...
    job experience: ...
    projects: ...   #only titles
    certification: ...
    LinkedIn: ...
    core_skills: "..."
    soft_skills: "..."
    resume_rating: "..."
    improvement_areas: "..."  # keep it short and straightforward
    upskill_suggestions: "..."   # keep it short and straightforward
    other: "..."
    Ensure all the information is obtain and in the output dont give ''' json curly brackets....curly brackte ''' as the output just curly brackets then the json format would be prefered.
    make sure to fills the given details. and rate the resume out of 10 mandatory (for example: 1,2,3,4,6,7,8,9,10) based on how good the profile is and be very strict and if somthing is just comepltely absent enter Unknown)
    dont make subsets inside one set ( for example : curly brackets name : xyz , education : [abc, ths, bfg], curly brackets)
    dont make any subarrays like in education, certification , projects.
    Here is the resume:
    {resume_text}
    """
    # Send the request to the Gemini model
    response = client.models.generate_content(
        model='gemini-1.5-pro-002',
        contents=prompt
    )
    return response.text



# Function to save extracted data into the database
def save_resume_to_db(extracted_data):
    try:
        
        # Parse the extracted data 
        resume_data = json.loads(extracted_data) 
        
        # Establish the connection
        conn = get_db_connection()
        cursor = conn.cursor()  
       
        # Get a database connection
        query = """
        INSERT INTO resumes (
        name, email, contact_no, education, profession, job_experience, 
        projects, certification, linkedin, core_skills, soft_skills, 
        resume_rating, improvement_areas, upskill_suggestions, other
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            
        values=(
            resume_data.get('name', 'Uknown'),
            resume_data.get('email', 'Uknown'),
            resume_data.get('contact no', 'Uknown'),
            resume_data.get('education', 'Uknown'),
            resume_data.get('profession', 'Uknown'),
            resume_data.get('job experience', 'Uknown'),
            resume_data.get('projects', 'Uknown'),
            resume_data.get('certification', 'Uknown'),
            resume_data.get('LinkedIn', 'Uknown'),
            resume_data.get('core_skills', 'Uknown'),
            resume_data.get('soft_skills', 'Uknown'),
            resume_data.get('resume_rating', '0'),
            resume_data.get('improvement_areas', 'Uknown'),
            resume_data.get('upskill_suggestions', 'Uknown'),
            resume_data.get('other', 'Uknown')
        )
        
        # Insert data into the database
        cursor.execute(query,values)

        # Commit the transaction
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logging.error(f"Error saving resume to database: {str(e)}")
        raise HTTPException(status_code=500, detail="Error saving resume to database")
    

# Endpiont to get the extracted data and post the response back to frontend given by gemini
@app.post("/upload")
async def upload_resume(resume: dict):
    try:
        # Extracted resume text from the frontend
        resume_text = resume.get("resume_text", "")

        # Log the resume content
        logging.info(f"Received resume text: {resume_text}...")  # Log the first 100 characters

        # Extract resume details using Gemini
        extracted_data = extract_resume_details(resume_text)
        
        print(extracted_data)
        save_resume_to_db(extracted_data)
    
        return PlainTextResponse(content=extracted_data)
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return PlainTextResponse(content=f"Error: {str(e)}", status_code=500)


# Endpiont to get the history of resumes 
@app.get("/history")
async def get_uploaded_resumes():
    try:
        # Get a database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch all records from the resumes table
        query = "SELECT id, name, profession, resume_rating FROM resumes;"  # Adjust query if necessary
        cursor.execute(query)

        # Fetch column names for constructing JSON response
        column_names = [desc[0] for desc in cursor.description]

        # Fetch all rows and convert to list of dictionaries
        rows = cursor.fetchall()
        result = [dict(zip(column_names, row)) for row in rows]

        # Close the connection
        cursor.close()
        conn.close()

        return result  # Directly return the result as JSON
    
    except Exception as e:
        logging.error(f"Error fetching history: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching history")


# Endpiont to get detials of past resume 
@app.get("/details/{id}")
async def get_resume_details(id: int):
    """
    Fetch detailed resume information for a specific ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch record by ID
        query = "SELECT * FROM resumes WHERE id = %s;"
        cursor.execute(query, (id,))
        row = cursor.fetchone()

        if row:
            column_names = [desc[0] for desc in cursor.description]
            resume_details = dict(zip(column_names, row))
        else:
            raise HTTPException(status_code=404, detail="Resume not found")

        cursor.close()
        conn.close()

        return resume_details
    except Exception as e:
        logging.error(f"Error fetching resume details: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching resume details")
