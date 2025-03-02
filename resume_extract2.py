import os
from io import BytesIO
from typing import List, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from pydantic import BaseModel, Field
from pypdf import PdfReader

app = FastAPI()
load_dotenv()
llm = GoogleGenerativeAI(
    model='gemini-1.5-flash',
    temperature=0,
    GEMINI_API_KEY=os.getenv('GEMINI_API_KEY')
)

# Add CORS middleware with specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_pdf_file(file_contents: BytesIO):
    try:
        pdf_reader = PdfReader(file_contents)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading PDF: {str(e)}")

class Education(BaseModel):
    university: str = Field(description="Name of university or educational institution")
    degree: str = Field(description="Type of degree obtained")
    major: str = Field(description="Field of study or major")
    graduationYear: Optional[str] = Field(description="Year of graduation")
    gpa: Optional[str] = Field(description="GPA or academic performance")

class Experience(BaseModel):
    jobTitle: str = Field(description="Job title or position")
    company: str = Field(description="Company or organization name")
    startDate: Optional[str] = Field(description="Start date of employment")
    endDate: Optional[str] = Field(description="End date of employment, or empty if current")
    description: str = Field(description="Description of responsibilities and achievements")

class ResumeReport(BaseModel):
    firstname: str = Field(description="First name of the person")
    lastname: str = Field(description="Last name of the person")
    email: Optional[str] = Field(description="Email address of the person")
    phone: Optional[str] = Field(description="Phone number of the person")
    address: Optional[str] = Field(description="Address of the person")
    skills: List[str] = Field(description="List of skills")
    education: List[Education] = Field(description="Education details with university, degree, major, and graduation year")
    experience: List[Experience] = Field(description="Work experience details with job title, company, dates, and description")

@app.post("/summarize_resume")
async def summarize_resume(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        contents = await file.read()
        file_contents = BytesIO(contents)
        text = read_pdf_file(file_contents)

        prompt = """
        Extract detailed information from the resume delimited by triple backquotes and return it as structured JSON.
        
        For education, extract each educational entry with university name, degree type, field of study/major, and graduation year.
        
        For experience, extract each work experience with job title, company name, start date, end date (or indicate if current), 
        and a detailed description of responsibilities and achievements.
        
        Return the following fields:
        - firstname: The first name of the person
        - lastname: The last name of the person
        - email: The email address of the person
        - phone: The phone number of the person
        - address: Their current address
        - skills: A list of their technical and professional skills
        - education: A list of objects containing:
          - university: Name of the institution
          - degree: Type of degree (e.g., Bachelor's, Master's)
          - major: Field of study
          - graduationYear: Year of graduation
          - gpa: GPA if available
        - experience: A list of objects containing:
          - jobTitle: Position held
          - company: Company name
          - startDate: When they started (format as YYYY-MM-DD if possible)
          - endDate: When they ended (format as YYYY-MM-DD, or null if current)
          - description: Detailed description of responsibilities and achievements

        ```{text}```
        """

        prompt_template = PromptTemplate(template=prompt, input_variables=["text"])
        output_parser = JsonOutputParser(pydantic_object=ResumeReport)
        
        # Create the chain correctly
        chain = (
            prompt_template 
            | llm 
            | output_parser
        )
        
        # Invoke chain with the text
        response = chain.invoke({"text": text})
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")
