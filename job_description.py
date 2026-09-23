import re
from typing import Any, Dict, List, Optional
import docx
import pdfplumber


def load_jd_text(file_path: str) -> str:
    """Helper to read text locally from .pdf, .docx, .md, and .txt files."""
    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text.append(page_text)
        return "\n".join(text)

    elif file_path_lower.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    elif file_path_lower.endswith((".md", ".txt")):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    else:
        raise ValueError(
            "Unsupported format! Provide a .pdf, .docx, .md, or .txt file."
        )


class RuleBasedJDExtractor:
    """Extracts structured information from raw Job Description text into a dictionary."""

    def __init__(self, raw_text: str):
        self.raw_text = raw_text or ""
        self.lines = [
            line.strip() for line in self.raw_text.splitlines() if line.strip()
        ]

    def _extract_section_by_keywords(
        self, keywords: List[str], stop_keywords: List[str]
    ) -> List[str]:
        """Captures lines under a section header until the next recognized header."""
        capturing = False
        content = []

        pattern = re.compile(
            r"^(?:#+\s*)?(?:" + "|".join(keywords) + r")[:\s]*$",
            re.IGNORECASE,
        )
        stop_pattern = re.compile(
            r"^(?:#+\s*)?(?:" + "|".join(stop_keywords) + r")[:\s]*$",
            re.IGNORECASE,
        )

        for line in self.lines:
            if pattern.search(line):
                capturing = True
                continue
            elif capturing and stop_pattern.search(line):
                break
            elif capturing:
                cleaned_line = re.sub(r"^[\*•\-\+\d+\.\s]+", "", line)
                cleaned_line = re.sub(r"[*_~`]", "", cleaned_line).strip()
                if cleaned_line:
                    content.append(cleaned_line)

        return content

    def get_company_details(self) -> Dict[str, Optional[str]]:
        about = self._extract_section_by_keywords(
            ["about us", "about the company", "company overview", "who we are"],
            ["position", "responsibilities", "requirements", "qualifications", "role"],
        )
        return {"about": "\n".join(about) if about else None}

    def get_position_details(self) -> Dict[str, Optional[str]]:
        title, location, employment_type = None, None, None

        for line in self.lines[:15]:
            clean_line = re.sub(r"[*_~`#]", "", line).strip()
            
            if not title and re.search(r"\b(title|role|position)\b", clean_line, re.IGNORECASE):
                title = clean_line
            if not location and re.search(r"\b(remote|hybrid|on-site|location)\b", clean_line, re.IGNORECASE):
                location = clean_line
            if not employment_type and re.search(r"\b(full-time|part-time|contract|internship)\b", clean_line, re.IGNORECASE):
                employment_type = clean_line

        return {
            "title": title,
            "location": location,
            "employment_type": employment_type,
        }

    def get_responsibilities(self) -> List[str]:
        stop_headers = [
            "skills", "qualifications", "requirements", "benefits", 
            "perks", "equal opportunity", "physical", "about us"
        ]
        return self._extract_section_by_keywords(
            ["responsibilities", "key responsibilities", "duties", "what you will do", "role summary"],
            stop_headers,
        )

    def get_skills_and_qualifications(self) -> List[str]:
        stop_headers = [
            "responsibilities", "benefits", "perks", 
            "equal opportunity", "physical", "about us", "what we offer"
        ]
        return self._extract_section_by_keywords(
            [
                "skills & qualifications required", "skills & qualifications",
                "skills", "technical skills", "requirements", "qualifications", "what you bring"
            ],
            stop_headers,
        )

    def get_qualification_criteria(self) -> Dict[str, Any]:
        years_exp = None
        education = []

        for line in self.lines:
            clean_line = re.sub(r"[*_~`#]", "", line).strip()
            
            if not years_exp:
                exp_match = re.search(
                    r"\b(\d+\+?\s*(?:-\s*\d+)?\s*years?(?:\s*of)?\s*experience)\b",
                    clean_line,
                    re.IGNORECASE,
                )
                if exp_match:
                    years_exp = exp_match.group(1)

            if re.search(r"\b(bachelor|master|phd|b\.tech|m\.tech|degree|bs|ms)\b", clean_line, re.IGNORECASE):
                cleaned_edu = re.sub(r"^[\*•\-\+\d+\.\s]+", "", clean_line)
                education.append(cleaned_edu)

        return {"experience_years": years_exp, "education": education}

    def get_physical_requirements(self) -> Optional[str]:
        stop_headers = ["benefits", "perks", "equal opportunity", "about us"]
        res = self._extract_section_by_keywords(
            [
                "physical & environmental requirements", "physical requirements",
                "work environment", "working conditions"
            ],
            stop_headers,
        )
        return "\n".join(res) if res else None

    def get_benefits(self) -> List[str]:
        stop_headers = ["equal opportunity", "physical", "about us", "responsibilities", "requirements"]
        return self._extract_section_by_keywords(
            [
                "company benefits & perks", "benefits & perks", 
                "benefits", "what we offer", "perks", "compensation & benefits"
            ],
            stop_headers,
        )

    def get_equal_opportunity_statement(self) -> Optional[str]:
        eoe_lines = []
        capturing = False

        for line in self.lines:
            clean_line = re.sub(r"[*_~`#]", "", line).strip()
            if re.search(r"equal opportunity employer|eoe statement|diversity & inclusion", clean_line, re.IGNORECASE):
                capturing = True
            elif capturing and re.match(r"^(?:#+\s*)?[A-Z\s]{4,}[:\s]*$", line):
                break
            
            if capturing:
                eoe_lines.append(clean_line)

        return " ".join(eoe_lines) if eoe_lines else None

    def extract_all(self) -> Dict[str, Any]:
        """Extracts job details directly into a dictionary."""
        return {
            "company_details": self.get_company_details(),
            "position_details": self.get_position_details(),
            "responsibilities": self.get_responsibilities(),
            "skills_and_qualifications": self.get_skills_and_qualifications(),
            "qualification_criteria": self.get_qualification_criteria(),
            "physical_and_environmental_requirements": self.get_physical_requirements(),
            "company_benefits_and_perks": self.get_benefits(),
            "equal_opportunity_statement": self.get_equal_opportunity_statement(),
        }


def job_description(raw_text: str) -> Dict[str, Any]:
    """Takes raw_text and extracts details directly into a dictionary."""
    extractor = RuleBasedJDExtractor(raw_text)
    return extractor.extract_all()