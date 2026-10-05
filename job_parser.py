from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq
from models import JobRequirements

# Load environment variables
load_dotenv()


job_parser_agent = Agent(

    model=Groq(
        id="openai/gpt-oss-120b"
    ),

    name="Job Description Parser",

    description=(
        "An AI agent that extracts structured requirements "
        "from job descriptions."
    ),

    instructions=[

        "Extract information only from the provided job description.",

        "Identify the job title.",

        "Identify required skills.",

        "Identify preferred skills.",

        "Identify required experience.",

        "Identify required education.",

        "Identify the main job responsibilities.",

        "Do not invent requirements that are not present."
    ],

    output_schema=JobRequirements,

    use_json_mode=True
)

if __name__ == "__main__":

    job_description = """
    Data Scientist

    We are looking for a Data Scientist with 2+ years
    of experience.

    Required Skills:
    Python, SQL, Machine Learning, Statistics

    Preferred Skills:
    Deep Learning, Power BI, AWS, LangChain

    Education:
    Bachelor's degree in Computer Science,
    Statistics, Mathematics or related field.

    Responsibilities:
    Build machine learning models.
    Analyze large datasets.
    Create dashboards and reports.
    Work with business teams.
    """

    response = job_parser_agent.run(
        f"""
        Parse the following job description:

        {job_description}
        """
    )

    job = response.content

    print("\n========== JOB REQUIREMENTS ==========\n")

    print("Job Title:", job.job_title)

    print("\nRequired Skills:")
    for skill in job.required_skills:
        print("-", skill)

    print("\nPreferred Skills:")
    for skill in job.preferred_skills:
        print("-", skill)

    print("\nExperience:")
    print(job.experience_required)

    print("\nEducation:")
    print(job.education_required)

    print("\nResponsibilities:")
    for responsibility in job.responsibilities:
        print("-", responsibility)