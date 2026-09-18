from extractor.section import section_detector
from resumes import resume_extractor
skills_list = [
    # ---- 1. CORE PROGRAMMING & SOFTWARE (20) ----
    "Python",
    "Java",
    "C++",
    "C",
    "C Programming",
    "JavaScript",
    "Data Structures and Algorithms (DSA)",
    "Object-Oriented Programming (OOP)",
    "SQL",
    "NoSQL Databases (MongoDB)",
    "HTML5 & CSS3",
    "Git & GitHub",
    "Linux / Unix Commands",
    "Software Development Life Cycle (SDLC)",
    "RESTful APIs",
    "Docker / Containerization",
    "Cloud Computing Fundamentals (AWS/Azure)",
    "Object-Relational Mapping (ORM)",
    "Unit Testing & Debugging",
    "Agile / Scrum Methodologies",
    "System Design Fundamentals",

    # ---- 2. SPECIALIZATION & EMERGING TECH (20) ----
    "Machine Learning (ML)",
    "Deep Learning",
    "Data Analysis / Analytics",
    "Data Visualization (Tableau/PowerBI)",
    "Artificial Intelligence (AI) Prompting",
    "Android / iOS App Development",
    "Web Development (MERN/MEAN Stack)",
    "Cybersecurity Fundamentals",
    "Ethical Hacking & Network Security",
    "Internet of Things (IoT)",
    "Blockchain Technology",
    "DevOps Practices",
    "Big Data Tools (Hadoop/Spark)",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "Cloud Architecture",
    "API Testing (Postman)",
    "Computer Networking (TCP/IP)",
    "Operating Systems (OS) Concepts",
    "Compiler Design Concepts",

    # ---- 3. HARDWARE, CORE ENGINEERING & CAD (15) ----
    "MATLAB / Simulink",
    "AutoCAD",
    "SolidWorks",
    "Embedded Systems Design",
    "Microcontrollers (Arduino/Raspberry Pi)",
    "VLSI Design",
    "PLC Automation / SCADA",
    "Circuit Simulation (PSpice/Proteus)",
    "LabVIEW",
    "CNC Programming",
    "Thermodynamics & Fluid Mechanics Applications",
    "Power Systems Analysis",
    "Digital Electronics",
    "Signal Processing",
    "Robotics Kinematics",

    # ---- 4. MATHEMATICS & ANALYTICAL (10) ----
    "Linear Algebra & Calculus",
    "Probability & Statistics",
    "Discrete Mathematics",
    "Numerical Methods",
    "Optimization Techniques",
    "Quantitative Aptitude",
    "Logical Reasoning",
    "Data Interpretation",
    "Cryptographic Mathematics",
    "Statistical Modelling",

    # ---- 5. PROFESSIONAL, REASONING & MANAGERIAL (15) ----
    "Technical Documentation",
    "Project Management",
    "System Requirements Gathering",
    "Technical Research & Writing",
    "Cost Estimation & Budgeting",
    "Quality Assurance (QA)",
    "Product Management Lifecycle",
    "Systems Engineering",
    "Business Analysis",
    "Risk Management",
    "Data Privacy & Compliance",
    "IPR & Patent Filing Awareness",
    "UI/UX Wireframing (Figma)",
    "Design Thinking",
    "Technical Presentations",

    # ---- 6. SOFT SKILLS & EMPLOYABILITY (15) ----
    "Problem-Solving",
    "Critical Thinking",
    "Team Collaboration / Teamwork",
    "Cross-Functional Communication",
    "Time Management",
    "Adaptability & Continuous Learning",
    "Emotional Intelligence",
    "Active Listening",
    "Conflict Resolution",
    "Negotiation Skills",
    "Interpersonal Skills",
    "Public Speaking",
    "Professional Networking",
    "Interview Etiquette",
    "Resume / Portfolio Building"
]

raw_text= resume_extractor("resume/Deepanshu_resume.pdf")
# data = section_detector(raw_text)
# cand_skills = data["skills"]

def skill_extractor(cand_skills):
    skills = []
    for i in cand_skills:
        if i in skills_list:
            skills.append(i)
    return skills
