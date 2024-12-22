# Resume Parser Project

## Overview

This project allows you to upload a PDF resume, extract information from it, and store it in a MySQL database. It uses the Gemini API for parsing resume data and takes between 1 to 7 minutes for the API to respond, depending on the network and API load.

## Features

- Upload PDF resumes.
- Extract text-based resume data using Gemini API.
- Store extracted data in a MySQL database (`resume_db`).
- A simple FastAPI backend to handle requests and communicate with the database.
- A clean HTML frontend to upload resumes and display parsed data.

## Table Structure

The database is set up with the following table to store the parsed resume data:

```sql
CREATE TABLE resumes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name TEXT,
    email TEXT,
    contact_no TEXT,
    education TEXT,
    profession TEXT,
    job_experience TEXT,
    projects TEXT,  
    certification TEXT,
    linkedin TEXT,
    core_skills TEXT,
    soft_skills TEXT,
    resume_rating TEXT,
    improvement_areas TEXT,
    upskill_suggestions TEXT,
    other TEXT
);
```
## Requirements
Make sure to create a Python virtual environment and install the dependencies. To install the required dependencies, use the following steps:

- Create Virtual Environment:

```python -m venv venv```

- Activate Virtual Environment:

```venv\Scripts\activate```

Install Dependencies: Install the necessary dependencies by running:

```pip install -r requirements.txt```

Set up the Environment Variables:
- Create a .env file or add your API key directly to the code (in the API section).
- Add your Gemini API key to the .env file 

```GEMINI_API_KEY=your_api_key```

Database Setup:

- Connect your database in the database.py file.
- Ensure that you have created a MySQL database named resume_db and the resumes table with the structure provided above.

## Running the Project

- Start the FastAPI backend: 

```uvicorn main:app --reload```

- Run the HTML Frontend: 
    Open the index.html using any browser

### API Information
The Gemini API is used to parse text from the uploaded resumes. The API takes between 1 to 7 minutes to process the PDF, depending on the response time of the API.
- Make sure the PDF contains text (not scanned images) for accurate parsing.

#### Sample Resumes
You can test the project with the sample resumes provided in the resume folder. These sample resumes are in PDF format and contain text.
You can upload your own text-based PDF resumes for testing.

