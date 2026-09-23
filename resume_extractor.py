import re
from typing import Any, Dict


def info_extractor(raw_text: str) -> Dict[str, str]:
    """Extracts candidate contact details (Name, Email, Github, Linkedin, Mobile)

    from raw text into a dictionary.
    """
    info = {
        "Name": "",
        "Email": "",
        "Github": "",
        "Linkedin": "",
        "Mobile": "",
    }

    if not raw_text or not raw_text.strip():
        return info

    # Regex patterns for contact fields
    patterns = {
        "Email": r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",
        "Github": r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+/?",
        "Linkedin": r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+/?",
        "Mobile": r"(?:\+91[\s-]?)?(?:0)?\b[6-9]\d{4}[\s-]?\d{5}\b",
    }

    # Extract field matches
    for key, pattern in patterns.items():
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            info[key] = match.group().strip()

    # Name extraction strategy
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    ignore_words = {
        "resume",
        "curriculum",
        "vitae",
        "cv",
        "profile",
        "contact",
        "about",
    }

    for line in lines[:5]:
        words = line.split()
        if 2 <= len(words) <= 3:
            first_word_clean = words[0].lower().strip(":")
            if first_word_clean not in ignore_words:
                if all(re.match(r"^[A-Z][a-zA-a-z\.-]*$", w) for w in words):
                    info["Name"] = " ".join(words)
                    break

    # Fallback for name
    if not info["Name"] and lines:
        first_line_words = lines[0].split()
        if len(first_line_words) >= 2:
            info["Name"] = f"{first_line_words[0]} {first_line_words[1]}"

    return info


def section_extractor(raw_text: str) -> Dict[str, list]:
    """Categorizes text lines into resume sections inside a dictionary."""
    sections_mapping = {
        "Summary": [
            "professional summary",
            "summary",
            "executive summary",
            "about me",
            "profile",
        ],
        "skills": [
            "skills",
            "technical skills",
            "professional skills",
            "core competencies",
            "technologies",
        ],
        "education": [
            "education",
            "academic background",
            "qualification",
            "qualifications",
        ],
        "Certificates": ["certifications", "certificates", "licenses", "courses"],
        "Projects": [
            "project",
            "projects",
            "projects experience",
            "practical experience",
            "personal projects",
        ],
        "Experience": [
            "experience",
            "work experience",
            "employment history",
            "work history",
            "professional experience",
        ],
        "Achievements": [
            "achievements",
            "achievement",
            "honors",
            "awards",
            "other achievements",
        ],
        "Strengths": ["strength", "strengths", "soft skills"],
    }

    section_data = {
        "basic_info": [],
        "Summary": [],
        "skills": [],
        "education": [],
        "Certificates": [],
        "Projects": [],
        "Experience": [],
        "Achievements": [],
        "Strengths": [],
    }

    if not raw_text or not raw_text.strip():
        return section_data

    current_section = "basic_info"
    lines = raw_text.splitlines()

    for line in lines:
        cleaned_line = line.strip()

        if not cleaned_line:
            continue

        # Normalize potential section headers
        header_candidate = re.sub(
            r"^[#*\-\d\.\s]+|[:\s]+$", "", cleaned_line
        ).lower()

        matched_section = None
        for section_key, keywords in sections_mapping.items():
            if header_candidate in keywords:
                matched_section = section_key
                break

        if matched_section:
            current_section = matched_section
        else:
            section_data[current_section].append(cleaned_line)

    return section_data