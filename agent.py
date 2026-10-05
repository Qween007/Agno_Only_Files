from dotenv import load_dotenv
from pathlib import Path

from agno.agent import Agent
from agno.models.groq import Groq

from models import ResumeData
from resume_reader import extract_resume_text

from job_parser import job_parser_agent
from matcher import matcher_agent

# Load environment variables
load_dotenv()


# Create Resume Parser Agent
agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),

    name="Resume Parser Agent",

    description=(
        "An AI agent that extracts structured information "
        "from resumes."
    ),

    instructions=[
        "You are a professional resume parser.",
        "Extract only information present in the resume.",
        "Do not invent or assume information.",
        "If information is missing, return an empty value.",
        "Identify technical and professional skills.",
        "Keep experience information concise."
    ],

    output_schema=ResumeData,

    use_json_mode=True
)


if __name__ == "__main__":

    # Let the user choose one supported resume file from the Resume folder.
    resume_folder = Path(__file__).resolve().parent / "Resume"
    supported_extensions = (".pdf", ".docx", ".txt", ".text", ".csv", ".xlsx", ".xls")
    resume_files = sorted(
        (file_path for file_path in resume_folder.iterdir()
         if file_path.is_file() and file_path.suffix.lower() in supported_extensions),
        key=lambda file_path: file_path.name.lower(),
    )
    if not resume_files:
        raise FileNotFoundError(f"No supported resume files found in {resume_folder}")

    print("Available resumes:")
    for index, file_path in enumerate(resume_files, start=1):
        print(f"{index}. {file_path.name}")

    try:
        selected_index = int(input("Enter the resume number to parse: ")) - 1
        resume_path = str(resume_files[selected_index])
    except (ValueError, IndexError):
        raise ValueError("Please enter a valid resume number.") from None

    # Extract text from the selected resume file.
    resume_text = extract_resume_text(resume_path)

    print("\nResume text extracted successfully.\n")

    # Send resume text to Agno agent
    response = agent.run(
        f"""
        Parse the following resume and extract the candidate
        information according to the required schema.

        RESUME:

        {resume_text}
        """
    )

    resume = response.content

    print("\n========== RESUME DETAILS ==========\n")

    print("Name:", resume.name)
    print("Email:", resume.email)
    print("Phone:", resume.phone)

    print("\nSkills:")
    for skill in resume.skills:
        print("-", skill)

    print("\nEducation:")

    for education in resume.education:

        print("Degree:", education.degree)
        print("Institution:", education.institution)
        print("Year:", education.year)
        print()

    print("\nExperience:")

    for experience in resume.experience:

        print("Company:", experience.company)
        print("Role:", experience.role)
        print("Duration:", experience.duration)

        print("Responsibilities:")

        for responsibility in experience.responsibilities:
            print("-", responsibility)

        print()

    print("\nSummary:")
    print(resume.summary)

    job_description = input(
        "\nPaste the job description to compare with this resume:\n"
    )

    job_response = job_parser_agent.run(
        f"""
        Parse the following job description into structured requirements.

        {job_description}
        """
    )

    job_requirements = job_response.content

    print("\n========== JOB REQUIREMENTS ==========\n")
    print("Job title:", job_requirements.job_title)
    print("\nRequired skills:")
    for skill in job_requirements.required_skills:
        print("-", skill)

    print("\nPreferred skills:")
    for skill in job_requirements.preferred_skills:
        print("-", skill)

    print("\nRequired experience:", job_requirements.experience_required)
    print("Required education:", job_requirements.education_required)

    match_response = matcher_agent.run(
        f"""
        Compare the following candidate resume with the structured job
        requirements. Treat required skills and preferred skills separately.

        CANDIDATE RESUME:
        {resume.model_dump_json()}

        JOB REQUIREMENTS:
        {job_requirements.model_dump_json()}
        """
    )

    match = match_response.content

    print("\n========== JOB MATCH ==========\n")
    print("Matching percentage:", match.matching_percentage)

    print("\nMatching skills:")
    for skill in match.matching_skills:
        print("-", skill)

    print("\nMissing skills:")
    for skill in match.missing_skills:
        print("-", skill)

    print("\nStrengths:")
    for strength in match.strengths:
        print("-", strength)

    print("\nSkill gaps:")
    for skill_gap in match.skill_gaps:
        print("-", skill_gap)

    print("\nAnalysis:")
    print(match.analysis)