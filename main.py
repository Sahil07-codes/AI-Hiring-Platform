from resumes import resume_extractor
from extractor.info_extractor import info_extract
from extractor.section import section_detector
from skills import skill_extractor
from job_description import job_description

raw_text= resume_extractor("resume/Sahil_Resume.pdf")
info = info_extract(raw_text)
sections = section_detector(raw_text)
skills = skill_extractor(sections['skills'])
JD = job_description()
candidate = {
    "info": info,
    "summary": sections["Summary"],
    "skills": skills,
    "education": sections["education"],
    "projects": sections["Projects"],
    "experience": sections["Experience"],
    "certificates": sections["Certificates"]
}

print(JD)