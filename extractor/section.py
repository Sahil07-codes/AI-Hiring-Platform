sections_list = {
    'Summary': ['professional summary', 'summary', 'executive summary'],
    'skills': ['skills', 'technical skills', 'professional skills'],
    'education': ['education'],
    'Certificates': ['certifications','certificates', 'achievements'],
    'Projects' : ['project','projects','projects experience','practical experience'],
    'Experience' : ['experience'],
    'Achievements' : ['achievements', 'achievement', 'other achievements'],
    'Strengths' : ['strength','strengths']
}

def section_detector(raw_text):
    section_data = {
    'basic_info' : [],
    'Summary' : [],
    "skills" : [],
    "education" : [],
    "Certificates" : [],
    "Projects" : [],
    "Experience" : [],
    "Achievements" : [],
    "Strengths" : []
    }
    current_section = 'basic_info'
    lines = raw_text.splitlines()
    for line in lines:
        line = line.strip()
        for key, value in sections_list.items():
            if line.lower() in value:
                current_section = key
                break
        else:
            section_data[current_section].append(line)
        
    return section_data

# data = section_detector(raw_text)
# print(data())