import json
import re
from typing import Any, Dict, List, Optional
import docx  # python-docx library
import pdfplumber


# 1. File Loader Helper (PDF, DOCX, MD, TXT support)


def load_jd_text(file_path: str) -> str:
  """Reads text completely locally from .pdf, .docx, .md, and .txt files."""
  file_path_lower = file_path.lower()

  # Handle PDF files
  if file_path_lower.endswith(".pdf"):
    text = ""
    with pdfplumber.open(file_path) as pdf:
      for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
          text += page_text + "\n"
    return text

  # Handle DOCX files
  elif file_path_lower.endswith(".docx"):
    doc = docx.Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

  # Handle Markdown (.md) and Plain Text (.txt) files
  elif file_path_lower.endswith(".md") or file_path_lower.endswith(".txt"):
    with open(file_path, "r", encoding="utf-8") as f:
      return f.read()

  else:
    raise ValueError(
        "Unsupported file format! Please provide a .pdf, .docx, .md, or .txt"
        " file."
    )


# 2. Rule-Based Extractor Class


class RuleBasedJDExtractor:

  def __init__(self, raw_text: str):
    self.raw_text = raw_text
    self.lines = [
        line.strip() for line in raw_text.splitlines() if line.strip()
    ]

  def _extract_section_by_keywords(
      self, keywords: List[str], stop_keywords: List[str]
  ) -> List[str]:
    """Captures lines under a section header until the next recognized section header."""
    capturing = False
    content = []

    # Strip common Markdown headers (#, ##, ###) and clean up
    pattern = re.compile(
        r"^(?:#+\s*)?(?:" + "|".join(keywords) + r")[:\s]*$", re.IGNORECASE
    )
    stop_pattern = re.compile(
        r"^(?:#+\s*)?(?:" + "|".join(stop_keywords) + r")[:\s]*$", re.IGNORECASE
    )

    for line in self.lines:
      if pattern.search(line):
        capturing = True
        continue
      elif capturing and stop_pattern.search(line):
        break
      elif capturing:
        # Clean bullet points, markdown list symbols (*, -, +)
        cleaned_line = re.sub(r"^[\bullet\-\*•\+\d+\.]\s*", "", line)
        cleaned_line = re.sub(
            r"[*_~`]", "", cleaned_line
        )  # Strip markdown formatting symbols
        if cleaned_line:
          content.append(cleaned_line)

    return content

  def get_company_details(self) -> Dict[str, Optional[str]]:
    about = self._extract_section_by_keywords(
        ["about us", "about the company", "company overview"],
        ["position", "responsibilities", "requirements", "qualifications"],
    )
    return {"about": "\n".join(about) if about else None}

  def get_position_details(self) -> Dict[str, Optional[str]]:
    title = None
    location = None
    employment_type = None

    for line in self.lines[:12]:
      clean_line = re.sub(r"[*_~`#]", "", line)
      if (
          re.search(r"title|role|position", clean_line, re.IGNORECASE)
          and not title
      ):
        title = clean_line
      if (
          re.search(
              r"remote|hybrid|on-site|location", clean_line, re.IGNORECASE
          )
          and not location
      ):
        location = clean_line
      if (
          re.search(
              r"full-time|part-time|contract|internship",
              clean_line,
              re.IGNORECASE,
          )
          and not employment_type
      ):
        employment_type = clean_line

    return {
        "title": title,
        "location": location,
        "employment_type": employment_type,
    }

  def get_responsibilities(self) -> List[str]:
    all_headers = [
        "skills",
        "qualifications",
        "requirements",
        "benefits",
        "perks",
        "equal opportunity",
        "physical",
    ]
    return self._extract_section_by_keywords(
        ["responsibilities", "key responsibilities", "duties", "what you will do"],
        all_headers,
    )

  def get_skills_and_qualifications(self) -> List[str]:
    all_headers = [
        "responsibilities",
        "benefits",
        "perks",
        "equal opportunity",
        "physical",
        "about us",
    ]
    return self._extract_section_by_keywords(
        [
            "skills & qualifications required",
            "skills",
            "technical skills",
            "requirements",
            "qualifications",
        ],
        all_headers,
    )

  def get_qualification_criteria(self) -> Dict[str, Any]:
    years_exp = None
    education = []

    for line in self.lines:
      clean_line = re.sub(r"[*_~`#]", "", line)
      # Match years of experience pattern
      if not years_exp:
        exp_match = re.search(
            r"\b(\d+\+?\s*(?:-\s*\d+)?\s*years?(?:\s*of)?\s*experience)\b",
            clean_line,
            re.IGNORECASE,
        )
        if exp_match:
          years_exp = exp_match.group(1)

      # Match degree/education patterns
      if re.search(
          r"\b(bachelor|master|phd|b\.tech|m\.tech|degree|bs|ms)\b",
          clean_line,
          re.IGNORECASE,
      ):
        education.append(re.sub(r"^[\bullet\-\*•\+\d+\.]\s*", "", clean_line))

    return {"experience_years": years_exp, "education": education}

  def get_physical_requirements(self) -> Optional[str]:
    all_headers = ["benefits", "perks", "equal opportunity", "about us"]
    res = self._extract_section_by_keywords(
        [
            "physical & environmental requirements",
            "physical requirements",
            "work environment",
            "working conditions",
        ],
        all_headers,
    )
    return "\n".join(res) if res else None

  def get_benefits(self) -> List[str]:
    all_headers = [
        "equal opportunity",
        "physical",
        "about us",
        "responsibilities",
    ]
    return self._extract_section_by_keywords(
        [
            "company benefits & perks",
            "benefits & perks",
            "benefits",
            "what we offer",
            "perks",
        ],
        all_headers,
    )

  def get_equal_opportunity_statement(self) -> Optional[str]:
    eoe_lines = []
    capturing = False

    for line in self.lines:
      clean_line = re.sub(r"[*_~`#]", "", line)
      if re.search(
          r"equal opportunity employer|eoe statement|diversity & inclusion",
          clean_line,
          re.IGNORECASE,
      ):
        capturing = True
      if capturing:
        eoe_lines.append(clean_line)

    return " ".join(eoe_lines) if eoe_lines else None

  def extract_all(self) -> Dict[str, Any]:
    return {
        "company_details": self.get_company_details(),
        "position_details": self.get_position_details(),
        "responsibilities": self.get_responsibilities(),
        "skills_and_qualifications": self.get_skills_and_qualifications(),
        "qualification_criteria": self.get_qualification_criteria(),
        "physical_and_environmental_requirements": (
            self.get_physical_requirements()
        ),
        "company_benefits_and_perks": self.get_benefits(),
        "equal_opportunity_statement": (
            self.get_equal_opportunity_statement()
        ),
    }


# 3. Execution Example
def job_description():
    # if __name__ == "__main__":
    # Pass any file format: .pdf, .docx, .md, or .txt
    file_path = "Job descriptions/sample_ml_engineer_jd.docx"

    try:
        # 1. Read file text
        jd_text = load_jd_text(file_path)
        print(jd_text)
        # 2. Parse details locally
        extractor = RuleBasedJDExtractor(jd_text)
        extracted_data = extractor.extract_all()

        # 3. JSON Output
        return json.dumps(extracted_data, indent=2)

    except FileNotFoundError:
        return f"File '{file_path}' not found"
    except ValueError as e:
        return e