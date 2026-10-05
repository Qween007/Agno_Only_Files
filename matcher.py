from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.groq import Groq

from models import JobMatch


# Load environment variables
load_dotenv()


# Create Job Matching Agent
matcher_agent = Agent(

    model=Groq(
        id="openai/gpt-oss-120b"
    ),

    name="Job Matching Agent",

    description=(
        "An AI agent that compares a candidate's resume "
        "with a job description."
    ),

    instructions=[

        "Compare the candidate resume against the job requirements.",
        "Compare the candidate's skills with required skills.",
        "Identify matching skills.",
        "Identify missing required skills.",
        "Consider preferred skills separately.",
        "Identify candidate strengths relevant to the position.",
        "Identify important skill gaps.",
        "Calculate an approximate required-skill match percentage.",
        "Do not invent skills or experience.",
        "Do not make a hiring decision.",
        "Provide factual analysis based only on the supplied data."
    ],

    output_schema=JobMatch,

    use_json_mode=True
)