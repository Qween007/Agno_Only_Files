from pydantic import BaseModel, Field
'''

Pydantic is a popular data validation and serialization library for Python. 
It uses standard Python type hints to ensure that incoming or outgoing data is 
clean, properly formatted, and conforms to the rules you define. 
If the data is invalid, Pydantic immediately throws a clear error

'''

class Education(BaseModel):

    degree: str = Field(
        default="",
        description="Degree or qualification"
    )

    institution: str = Field(
        default="",
        description="Name of educational institution"
    )

    year: str = Field(
        default="",
        description="Year of completion"
    )


class Experience(BaseModel):

    company: str = Field(
        default="",
        description="Company or organization name"
    )

    role: str = Field(
        default="",
        description="Job title or role"
    )

    duration: str = Field(
        default="",
        description="Duration of employment"
    )

    responsibilities: list[str] = Field(
        default_factory=list,
        description="Main responsibilities or work performed"
    )


class ResumeData(BaseModel):

    name: str = Field(
        default = "",
        description = "Candidate's full name"
    )

    email: str = Field(
        default="",
        description="Candidate's email address"
    )

    phone: str = Field(
        default="",
        description="Candidate's phone number"
    )

    skills: list[str] = Field(
        default_factory=list,
        description="Technical and professional skills"
    )

    education: list[Education] = Field(
        default_factory=list,
        description="Educational qualifications"
    )

    experience: list[Experience] = Field(
        default_factory=list,
        description="Professional work experience"
    )

    summary: str = Field(
        default="",
        description="Short professional summary"
    )

class JobMatch(BaseModel):

    matching_skills: list[str] = Field(
        default_factory=list,
        description="Skills the candidate has that match the job requirements"
    )

    missing_skills: list[str] = Field(
        default_factory=list,
        description="Skills required by the job but missing from the candidate's resume"
    )

    matching_percentage: float = Field(
        default=0.0,
        description="Approximate percentage of required skills matched by the candidate"
    )

    strengths: list[str] = Field(
        default_factory=list,
        description="Candidate strengths relevant to the job"
    )

    skill_gaps: list[str] = Field(
        default_factory=list,
        description="Important areas where the candidate has skill gaps"
    )

    analysis: str = Field(
        default="",
        description="Overall explanation of the candidate's alignment with the job"
    )    

class JobRequirements(BaseModel):

    job_title: str = Field(
        default="",
        description="Title of the job"
    )

    required_skills: list[str] = Field(
        default_factory=list,
        description="Skills explicitly required for the job"
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
        description="Skills preferred but not necessarily required"
    )

    experience_required: str = Field(
        default="",
        description="Required years or type of experience"
    )

    education_required: str = Field(
        default="",
        description="Required educational qualification"
    )

    responsibilities: list[str] = Field(
        default_factory=list,
        description="Main responsibilities of the job"
    )    