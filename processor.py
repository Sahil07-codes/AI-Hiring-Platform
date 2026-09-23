import json
from job_description import job_description, load_jd_text
from resume_extractor import info_extractor, section_extractor
from resumes import resume_extractor


def process_candidate_and_jd(
    resume_path: str,
    jd_path: str,
    profile_json_path: str = "Candidate_profile.json",
    jd_json_path: str = "Job_description.json",
) -> dict:

    # 1. Extract text and details from Job Description
    jd_text = load_jd_text(jd_path)
    jd_data = job_description(jd_text)

    # Save Job Description data to JSON
    with open(jd_json_path, "w", encoding="utf-8") as file:
        json.dump(jd_data, file, indent=4)

    # 2. Extract text and details from Resume
    raw_text = resume_extractor(resume_path)
    info = info_extractor(raw_text)
    sections = section_extractor(raw_text)

    # Merge contact info and sections into a single dictionary
    candidate_profile = {"contact_info": info, "sections": sections}

    # Save Candidate Profile data to JSON
    with open(profile_json_path, "w", encoding="utf-8") as file:
        json.dump(candidate_profile, file, indent=4)

    # Return both parsed dictionaries
    return {"candidate_profile": candidate_profile, "job_description": jd_data}