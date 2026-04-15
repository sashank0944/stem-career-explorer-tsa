from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'tsa_coding_2026'

# data structure declarations for questions, personas, and careers
QUESTIONS = [
    {
        "id": 1, 
        "text": "When approaching a completely new subject, what is your natural starting point?",
        "options": [
            {"text": "Deconstructing the core principles to see how they function", "type": "investigator"},
            {"text": "Searching for the practical tools needed to apply the knowledge", "type": "builder"},
            {"text": "Imagining how this subject could be reimagined for the future", "type": "innovator"},
            {"text": "Organizing the information into a logical system or framework", "type": "analyst"},
            {"text": "Considering how this knowledge can directly benefit individual lives", "type": "healer"},
            {"text": "Looking at the large scale impact this has on the world and society", "type": "changer"},
        ]
    },
    {
        "id": 2, 
        "text": "A complex system breaks down in front of you. Your first instinct is:",
        "options": [
            {"text": "Identify the specific point of failure through investigation", "type": "investigator"},
            {"text": "Gather the necessary materials and begin the physical repair", "type": "builder"},
            {"text": "Question if the system itself is obsolete and needs a new design", "type": "innovator"},
            {"text": "Analyze the data patterns to prevent the error from repeating", "type": "analyst"},
            {"text": "Ensure that everyone affected by the breakdown is supported", "type": "healer"},
            {"text": "Evaluate the environmental or social cost of the failure", "type": "changer"},
        ]
    },
    {
        "id": 3, 
        "text": "You feel most in the zone when you are:",
        "options": [
            {"text": "Deep in a rabbit hole of research and discovery", "type": "investigator"},
            {"text": "Working with your hands or code to build something tangible", "type": "builder"},
            {"text": "Generating wild ideas that challenge the status quo", "type": "innovator"},
            {"text": "Mapping out complex data to find a hidden truth", "type": "analyst"},
            {"text": "Connecting with others to provide care and guidance", "type": "healer"},
            {"text": "Leading a mission that creates meaningful global change", "type": "changer"},
        ]
    },
    {
        "id": 4, 
        "text": "If you were observing a busy machine at work, what would you focus on?",
        "options": [
            {"text": "The underlying physics and mechanics that make the motion possible", "type": "investigator"},
            {"text": "The way the individual parts are connected and assembled", "type": "builder"},
            {"text": "How the machine could be improved to do something entirely new", "type": "innovator"},
            {"text": "The efficiency and timing of the machine output", "type": "analyst"},
            {"text": "How the machine improves the lives of the people using it", "type": "healer"},
            {"text": "The energy source and the long term footprint of the machine", "type": "changer"},
        ]
    },
    {
        "id": 5, 
        "text": "You are given a blank canvas and a week of time. You choose to:",
        "options": [
            {"text": "Conduct an experiment to test a new theory", "type": "investigator"},
            {"text": "Assemble a functional prototype of a useful device", "type": "builder"},
            {"text": "Draft a concept for a brand that does things differently", "type": "innovator"},
            {"text": "Develop a program that automates a tedious task", "type": "analyst"},
            {"text": "Organize a local initiative to help those in need", "type": "healer"},
            {"text": "Restore a piece of the local ecosystem or community", "type": "changer"},
        ]
    },
    {
        "id": 6, 
        "text": "When you look at a city skyline, what do you wonder about?",
        "options": [
            {"text": "The scientific breakthroughs that made these structures possible", "type": "investigator"},
            {"text": "The engineering and machinery required to lift the steel", "type": "builder"},
            {"text": "The artistic vision behind the unique architecture", "type": "innovator"},
            {"text": "The massive network of data and power keeping it alive", "type": "analyst"},
            {"text": "The health and safety of the millions living inside", "type": "healer"},
            {"text": "The ecological footprint and sustainability of the city", "type": "changer"},
        ]
    },
    {
        "id": 7, 
        "text": "Which of these strengths do you value most in yourself?",
        "options": [
            {"text": "The ability to see details that others completely overlook", "type": "investigator"},
            {"text": "The skill to take a raw idea and turn it into something real", "type": "builder"},
            {"text": "The courage to suggest an idea that sounds impossible at first", "type": "innovator"},
            {"text": "The patience to find order and logic within total chaos", "type": "analyst"},
            {"text": "The intuition to know exactly what someone needs before they ask", "type": "healer"},
            {"text": "The drive to stand up for a cause that will outlast your lifetime", "type": "changer"},
        ]
    },
    {
        "id": 8, 
        "text": "Which of these words carries the most weight for you?",
        "options": [
            {"text": "Evidence", "type": "investigator"},
            {"text": "Function", "type": "builder"},
            {"text": "Originality", "type": "innovator"},
            {"text": "Precision", "type": "analyst"},
            {"text": "Empathy", "type": "healer"},
            {"text": "Legacy", "type": "changer"},
        ]
    },
    {
        "id": 9, 
        "text": "How do you prefer to tackle a challenge?",
        "options": [
            {"text": "By gathering every available fact before taking action", "type": "investigator"},
            {"text": "By building a trial version and refining it as I go", "type": "builder"},
            {"text": "By brainstorming unconventional solutions that others missed", "type": "innovator"},
            {"text": "By breaking the problem into a step-by-step logical sequence", "type": "analyst"},
            {"text": "By considering how the solution will affect the people involved", "type": "healer"},
            {"text": "By ensuring the solution serves the greater good of the planet", "type": "changer"},
        ]
    },
    {
        "id": 10, 
        "text": "Your ideal legacy would be:",
        "options": [
            {"text": "Discovering a law of nature that remains true forever", "type": "investigator"},
            {"text": "Constructing something that people use every single day", "type": "builder"},
            {"text": "Being the first person to ever try a specific new idea", "type": "innovator"},
            {"text": "Optimizing a system to run at its absolute peak performance", "type": "analyst"},
            {"text": "Saving lives and providing solace to those in pain", "type": "healer"},
            {"text": "Restoring balance to a world that was out of alignment", "type": "changer"},
        ]
    },
    {
        "id": 11, 
        "text": "What kind of environment allows you to thrive?",
        "options": [
            {"text": "A quiet space where I can focus on deep intellectual work", "type": "investigator"},
            {"text": "A busy workshop filled with the tools of creation", "type": "builder"},
            {"text": "A collaborative studio where ideas are constantly flowing", "type": "innovator"},
            {"text": "A sleek digital space where I can command data and code", "type": "analyst"},
            {"text": "A personal setting where I can focus on individual care", "type": "healer"},
            {"text": "A community-focused space driven by a shared mission", "type": "changer"},
        ]
    },
    {
        "id": 12, 
        "text": "In a group project, you naturally gravitate toward:",
        "options": [
            {"text": "The Research lead who ensures all the facts are correct", "type": "investigator"},
            {"text": "The Maker who handles the actual construction of the project", "type": "builder"},
            {"text": "The Creative Director who keeps the vision bold and new", "type": "innovator"},
            {"text": "The Strategist who makes sure everything runs efficiently", "type": "analyst"},
            {"text": "The Team Lead who ensures everyone is heard and supported", "type": "healer"},
            {"text": "The Advocate who ensures the project does no harm to the world", "type": "changer"},
        ]
    },
    {
        "id": 13, 
        "text": "Which of these issues interests you the most?",
        "options": [
            {"text": "The spread of misinformation and the loss of objective truth", "type": "investigator"},
            {"text": "The breakdown of physical infrastructure and slow progress", "type": "builder"},
            {"text": "The lack of creativity in solving our most boring problems", "type": "innovator"},
            {"text": "The inefficiency of global systems and wasted resources", "type": "analyst"},
            {"text": "The gaps in healthcare and the suffering of individuals", "type": "healer"},
            {"text": "The climate crisis and the threat to our future generations", "type": "changer"},
        ]
    },
    {
        "id": 14, 
        "text": "If you were to invest in a startup, you would choose:",
        "options": [
            {"text": "A biotech company uncovering the secrets of DNA", "type": "investigator"},
            {"text": "A robotics firm building the tools for deep sea exploration", "type": "builder"},
            {"text": "A design lab creating a new way for humans to interact", "type": "innovator"},
            {"text": "A cybersecurity firm protecting global logic networks", "type": "analyst"},
            {"text": "A medical tech company personalizing cancer treatments", "type": "healer"},
            {"text": "A renewable energy startup capturing carbon from the air", "type": "changer"},
        ]
    },
    {
        "id": 15, 
        "text": "Finally, which statement feels most like your internal reality?",
        "options": [
            {"text": "I am driven by the need to understand the why behind everything", "type": "investigator"},
            {"text": "I am driven by the satisfaction of making things work", "type": "builder"},
            {"text": "I am driven by the urge to create what has never existed", "type": "innovator"},
            {"text": "I am driven by the desire to bring order to chaos", "type": "analyst"},
            {"text": "I am driven by the responsibility to care for others", "type": "healer"},
            {"text": "I am driven by the necessity of leaving the world better than I found it", "type": "changer"},
        ]
    }
]
PERSONAS = {
    "investigator": {
        "name": "Science & Discovery",
        "tagline": "The power of science is limitless",
        "emoji": "🔬",
        "color": "#4f9cf9",
        "description": "You're a natural researcher: endlessly curious, methodical, and passionate about uncovering how the world works. You thrive in environments where you can dig deep, test hypotheses, and expand human knowledge.",
        "traits": ["Curious", "Analytical", "Detail-oriented", "Patient", "Methodical"],
        "careers": ["biologist", "chemist", "astronomer"]
    },
    "builder": {
        "name": "Engineering & Creation",
        "tagline": "You hold the power to create things",
        "emoji": "⚙️",
        "color": "#f97316",
        "description": "You see problems as puzzles waiting to be engineered away. Whether it's code, circuits, or construction, you love the process of designing and building systems that work.",
        "traits": ["Hands-on", "Problem-solver", "Persistent", "Logical", "Creative"],
        "careers": ["software_engineer", "mechanical_engineer", "robotics_engineer"]
    },
    "innovator": {
        "name": "Design & Creativity",
        "tagline": "Creating the future you imagine",
        "emoji": "🚀",
        "color": "#a855f7",
        "description": "You blend creativity with technical thinking to imagine things that don't exist yet. You're drawn to entrepreneurship, design thinking, and disrupting the status quo with bold ideas.",
        "traits": ["Visionary", "Bold", "Creative", "Entrepreneurial", "Adaptable"],
        "careers": ["product_designer", "biotech_entrepreneur", "ai_researcher"]
    },
    "analyst": {
        "name": "Data & Strategy",
        "tagline": "Finding patterns to solve problems",
        "emoji": "📊",
        "color": "#22c55e",
        "description": "You think in data, systems, and logic. You're the person who spots the pattern, optimizes the process, and makes sense of complexity. Technology and math feel like superpowers to you.",
        "traits": ["Logical", "Precise", "Strategic", "Focused", "Systematic"],
        "careers": ["data_scientist", "cybersecurity_analyst", "mathematician"]
    },
    "healer": {
        "name": "Health & Medicine",
        "tagline": "Science in service of people",
        "emoji": "💊",
        "color": "#ec4899",
        "description": "You combine empathy with scientific curiosity. You're driven by a deep desire to improve health, reduce suffering, and understand the human body and mind, one patient or discovery at a time.",
        "traits": ["Empathetic", "Caring", "Detail-oriented", "Resilient", "Curious"],
        "careers": ["physician", "neuroscientist", "pharmacist"]
    },
    "changer": {
        "name": "Environment & Social Impact",
        "tagline": "Preserving our world with STEM",
        "emoji": "🌱",
        "color": "#14b8a6",
        "description": "You see science and technology as tools for justice, sustainability, and equity. You're driven not just by knowledge but by purpose — making sure your work has a positive impact on the planet and its people.",
        "traits": ["Purpose-driven", "Collaborative", "Passionate", "Systems-thinker", "Resilient"],
        "careers": ["environmental_scientist", "climate_engineer", "public_health_researcher"]
    }
}

CAREERS = {
    "biologist": {
        "title": "Biologist",
        "emoji": "🧬",
        "description": "Biologists work to study all living organisms in order to understand the fundamental processes of life. They work to drive breakthroughs in a variety of fields, such as medicine, agriculture, and environmental conservation. By becoming a biologist, you always are asking questions about the world around us.",
        "salary": "$65,000 – $130,000",
        "growth": "5%",
        "hs_courses": ["AP Biology", "AP Chemistry", "AP Environmental Science", "Statistics", "AP Physics"],
        "extracurriculars": ["Science Olympiad", "Biology or Ecology club", "Nature center volunteering", "Local science fair competitor", "iNaturalist species logging"],
        "skills": ["Lab techniques & microscopy", "Data collection & analysis", "Scientific writing", "Critical thinking", "Attention to detail"],
        "roadmap": ["Take AP Biology & Chemistry in high school", "Volunteer at a biology lab or nature center", "Earn a BS in Biology or Life Sciences", "Gain lab research experience or field internship", "Pursue MS/PhD for research, or enter biotech industry"],
        "entry_jobs": ["Lab Technician", "Research Assistant", "Wildlife Technician", "Biological Science Technician"],
        "links": [
            ("Khan Academy – Biology", "https://www.khanacademy.org/science/biology"),
            ("Coursera – Introductory Biology Courses", "https://www.coursera.org/courses?query=biology+MIT"),
            ("HHMI BioInteractive (free lessons)", "https://www.biointeractive.org"),
            ("American Institute of Biological Sciences", "https://www.aibs.org/careers/"),
        ]
    },
    "chemist": {
        "title": "Chemist",
        "emoji": "⚗️",
        "description": "Chemists investigate the composition, structure, and properties of substances. They develop and test materials, medicines, and industrial processes. Chemists work in laboratories, pharmaceutical companies, materials science, and food or chemical industries, performing experiments, analyzing results, and ensuring quality and safety.",
        "salary": "$60,000 – $120,000",
        "growth": "5%",
        "hs_courses": ["AP Chemistry", "AP Biology", "AP Physics", "Pre-Calculus / Calculus", "Statistics"],
        "extracurriculars": ["Chemistry Olympiad (USNCO)", "Science fair projects", "STEM club", "Local university lab shadow", "Maker/DIY chemistry hobby"],
        "skills": ["Laboratory safety & techniques", "Quantitative analysis", "Problem solving", "Technical writing", "Attention to accuracy"],
        "roadmap": ["Excel in AP Chemistry and math", "Compete in Chemistry Olympiad", "Earn a BS in Chemistry", "Intern at a pharma, materials, or food science company", "Specialize (organic, analytical, physical, or biochemistry)"],
        "entry_jobs": ["Lab Analyst", "QA/QC Chemist", "Research Technician", "Process Development Associate"],
        "links": [
            ("American Chemical Society – Education", "https://www.acs.org/education.html"),
            ("MIT OpenCourseWare – Chemistry", "https://ocw.mit.edu/courses/chemistry/"),
            ("Khan Academy – Chemistry", "https://www.khanacademy.org/science/chemistry"),
            ("Coursera – Chemistry for Engineers", "https://www.coursera.org/courses?query=chemistry"),
        ]
    },
    "astronomer": {
        "title": "Astronomer",
        "emoji": "🔭",
        "description": "Astronomers work to study celestial objects and phenomena, including those relating to stars, planets, galaxies, and black holes. In this career, you would combine subjects like physics and mathematics with observational data to understand the origin and evolution of not our world, but our universe in its entirety.",
        "salary": "$70,000 – $150,000",
        "growth": "5%",
        "hs_courses": ["AP Physics C", "AP Calculus BC", "AP Computer Science", "Statistics", "AP Chemistry"],
        "extracurriculars": ["Astronomy club", "NASA Citizen Science projects", "Local observatory volunteering", "Science Olympiad – Astronomy event", "Astrophotography hobby"],
        "skills": ["Advanced mathematics", "Programming (Python)", "Data analysis", "Physics fundamentals", "Scientific communication"],
        "roadmap": ["Join an astronomy club and get a telescope", "Take AP Physics and Calculus seriously", "Earn a BS in Physics or Astronomy", "Internship at NASA, ESA, or an observatory", "Complete a PhD and postdoctoral research"],
        "entry_jobs": ["Observatory Research Assistant", "Data Analyst (Space Science)", "Science Communicator", "Planetarium Educator"],
        "links": [
            ("NASA Learning Resources", "https://www.nasa.gov/learning-resources/"),
            ("Crash Course Astronomy (YouTube)", "https://www.youtube.com/playlist?list=PL8dPuuaLjXtPAJr1ysd5yGIyiSFuh0mIL"),
            ("Coursera – Astronomy: Exploring Time & Space (U of Arizona)", "https://www.coursera.org/learn/astro"),
            ("AAS Careers in Astronomy", "https://aas.org/careers/career-astronomer"),
        ]
    },
    "software_engineer": {
        "title": "Software Engineer",
        "emoji": "💻",
        "description": "Software engineers work to design, build, test, and maintain computer programs and applications that power a variety of things. They work on web development, app creation, system infrastructure, and other projects. This career combines logical thinking with creativity in regards to problem solving, providing an enticing environment.",
        "salary": "$90,000 – $180,000",
        "growth": "25%",
        "hs_courses": ["AP Computer Science A", "AP Computer Science Principles", "AP Calculus", "Statistics", "AP Physics"],
        "extracurriculars": ["Hackathons", "Coding clubs or FIRST Robotics", "Personal app or website projects", "Contributing to open source on GitHub", "Math competitions (AMC, MATHCOUNTS)"],
        "skills": ["Programming (Python, Java, JavaScript)", "Debugging & problem solving", "Version control (Git)", "Algorithmic thinking", "Collaboration & communication"],
        "roadmap": ["Learn Python or JavaScript with free online courses", "Build small personal projects (games, apps, websites)", "Earn a BS in Computer Science or Software Engineering", "Complete internships at tech companies", "Join a startup or land a full-time engineering role"],
        "entry_jobs": ["Junior Software Developer", "QA / Test Engineer", "Frontend Developer", "Backend Developer Intern"],
        "links": [
            ("freeCodeCamp – Free Full-Stack Curriculum", "https://www.freecodecamp.org"),
            ("CS50 by Harvard (free, beginner-friendly)", "https://cs50.harvard.edu"),
            ("MIT OpenCourseWare – Computer Science", "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/"),
            ("Codecademy – Learn to Code", "https://www.codecademy.com"),
        ]
    },
    "mechanical_engineer": {
        "title": "Mechanical Engineer",
        "emoji": "🔧",
        "description": "Mechanical engineers design and analyze physical systems such as engines, machines, and devices. Their work uses principles from physics, mathematics, and materials science to solve practical problems. They are very versatile, being involved in industries like manufacturing, aerospace, energy, and robotics.",
        "salary": "$75,000 – $140,000",
        "growth": "7%",
        "hs_courses": ["AP Physics C: Mechanics", "AP Calculus BC", "AP Chemistry", "Pre-Engineering / CAD", "Statistics"],
        "extracurriculars": ["FIRST Robotics or VEX Robotics", "Engineering competitions (SkillsUSA, TSA)", "Build-it-yourself projects (electronics, woodworking)", "Science Olympiad – engineering events", "CAD software self-study (Fusion 360, SolidWorks)"],
        "skills": ["CAD modeling (SolidWorks, AutoCAD)", "Physics & thermodynamics", "Materials science", "Problem analysis", "Project management"],
        "roadmap": ["Take AP Physics and Calculus", "Join robotics or engineering competitions", "Earn a BS in Mechanical Engineering (ABET-accredited)", "Intern at a manufacturing, aerospace, or automotive firm", "Pursue Professional Engineer (PE) licensure"],
        "entry_jobs": ["Engineering Technician", "CAD Designer", "Test Engineer", "Manufacturing Engineer I"],
        "links": [
            ("MIT OpenCourseWare – Mechanical Engineering", "https://ocw.mit.edu/courses/mechanical-engineering/"),
            ("ASME Student Resources", "https://www.asme.org/topics-resources/content/resources-for-students"),
            ("Autodesk Fusion 360 (free for students)", "https://www.autodesk.com/education/edu-software/overview"),
            ("Coursera – Mechanics of Materials (Georgia Tech)", "https://www.coursera.org/learn/mechanics-of-materials-i-fundamentals"),
        ]
    },
    "robotics_engineer": {
        "title": "Robotics Engineer",
        "emoji": "🤖",
        "description": "Robotics engineers focus on designing, building, and programming autonomous machines that can govern themselves, sensing, thinking, and acting on their own. This field is great if you are interested in mechanical engineering, electrical engineering, and computer science, being a cross-section of all three.",
        "salary": "$85,000 – $160,000",
        "growth": "13%",
        "hs_courses": ["AP Computer Science A", "AP Physics C", "AP Calculus", "Electronics", "Statistics"],
        "extracurriculars": ["FIRST Robotics Competition (FRC)", "VEX Robotics", "Drone or RC vehicle building", "Arduino / Raspberry Pi projects", "Science Olympiad – Robot Tour event"],
        "skills": ["Programming (Python, C++, ROS)", "Electronics & circuitry", "Mechanical design", "Systems thinking", "Troubleshooting & iteration", "Linear Algebra"],
        "roadmap": ["Join a FIRST Robotics team in high school", "Learn Python and basic electronics", "Earn a BS in Robotics, Mechatronics, or EE/CS", "Build a portfolio of robotics projects", "Work at aerospace, automotive, or consumer robotics companies"],
        "entry_jobs": ["Robotics Technician", "Automation Engineer I", "Controls Engineer", "Embedded Systems Developer"],
        "links": [
            ("FIRST Robotics – Get Involved", "https://www.firstinspires.org"),
            ("ROS (Robot Operating System) Tutorials", "https://www.ros.org/blog/getting-started/"),
            ("Coursera – Robotics Specialization (UPenn)", "https://www.coursera.org/specializations/robotics"),
            ("edX – Robotics MicroMasters (Columbia)", "https://www.edx.org/micromasters/columbiax-robotics"),
        ]
    },
    "product_designer": {
        "title": "Product / UX Designer",
        "emoji": "🎨",
        "description": "Product and UX designers shape the look, feel, and usability of digital and physical products. They study user behavior, design interfaces, build prototypes, and test their ideas with real users to make sure products are intuitive and easy to use. This role combines psychology, visual design, and technology to create experiences that work well for people.",
        "salary": "$75,000 – $150,000",
        "growth": "16%",
        "hs_courses": ["AP Computer Science Principles", "Art & Design", "Psychology", "Statistics", "Digital Media / Graphic Design"],
        "extracurriculars": ["Design club or art portfolio building", "Build your own app or website mock-up", "Participate in design competitions (Adobe Creative Jam)", "Study popular apps and critique their UX", "Photography or visual arts"],
        "skills": ["Visual design & typography", "Wireframing & prototyping (Figma)", "User research & empathy", "Communication & storytelling", "Iterative thinking"],
        "roadmap": ["Learn Figma and study design fundamentals", "Build a portfolio of 3–5 design case studies", "Earn a BS in Design, HCI, or CS", "Freelance or intern at a startup or agency", "Join a product team at a tech or consumer company"],
        "entry_jobs": ["Junior UX Designer", "UI Designer", "UX Research Assistant", "Product Design Intern"],
        "links": [
            ("Google UX Design Certificate (Coursera)", "https://grow.google/certificates/ux-design/"),
            ("Figma Education – Free for Students", "https://www.figma.com/education/"),
            ("Nielsen Norman Group – UX Articles & Training", "https://www.nngroup.com/articles/"),
            ("Interaction Design Foundation (free + paid)", "https://www.interaction-design.org"),
        ]
    },
    "biotech_entrepreneur": {
        "title": "Biotechnology Entrepreneur",
        "emoji": "🧪",
        "description": "Biotech entrepreneurs start or lead companies that apply biological and medical science to solve problems in healthcare, agriculture, food, and the environment. This role demands both deep scientific knowledge and sharp business instincts. You'll need to understand biology well enough to spot real opportunities, and business well enough to build teams, raise funding, and bring products to market.",
        "salary": "$80,000 – $250,000+",
        "growth": "Highly variable",
        "hs_courses": ["AP Biology", "AP Chemistry", "AP Economics", "Statistics", "AP Computer Science Principles"],
        "extracurriculars": ["Science fair (regional and national levels)", "DECA or entrepreneurship club", "iGEM (International Genetically Engineered Machine)", "Shadow a biotech professional or startup founder", "Read biotech news (STAT News, BioPharma Dive)"],
        "skills": ["Scientific research literacy", "Business strategy & pitching", "Networking & communication", "Project management", "Risk tolerance & resilience"],
        "roadmap": ["Study biology AND business fundamentals", "Enter science and entrepreneurship competitions", "Earn a BS in Bioengineering, Biochemistry, or Biology", "Network with biotech investors, founders, and incubators", "Start a company, join a startup early, or pursue an MBA"],
        "entry_jobs": ["Patent Agent Intern", "Business Development Analyst", "Clinical Operations Coordinator", "Lab Manager"],
        "links": [
            ("Y Combinator Startup School (free)", "https://www.startupschool.org"),
            ("iGEM – Student Biotech Competition", "https://igem.org"),
            ("Coursera – Bioinformatics Specialization (UCSD)", "https://www.coursera.org/specializations/bioinformatics"),
            ("BIO.org – Careers in Biotech", "https://www.bio.org/careers"),
        ]
    },
    "ai_researcher": {
        "title": "AI / ML Researcher",
        "emoji": "🧠",
        "description": "AI and machine learning researchers develop algorithms and models that allow computers to learn, analyze data, and make decisions. They work on areas such as natural language processing, computer vision, and generative AI. This field changes quickly and requires strong skills in math, programming, and problem solving, while offering opportunities to work on impactful and cutting-edge technology.",
        "salary": "$110,000 – $300,000+",
        "growth": "40%+",
        "hs_courses": ["AP Computer Science A", "AP Calculus BC", "AP Statistics", "AP Physics", "Linear Algebra (if available)"],
        "extracurriculars": ["Math Olympiad (AMC, AIME)", "Kaggle machine learning competitions", "Personal ML projects on GitHub", "Research paper reading clubs", "Science fair with a data or AI focus"],
        "skills": ["Python & ML libraries (TensorFlow, PyTorch)", "Linear algebra & calculus", "Statistics & probability", "Research & paper writing", "Critical thinking & experimentation"],
        "roadmap": ["Learn Python and linear algebra thoroughly", "Complete ML courses (fast.ai, DeepLearning.AI)", "Earn a BS in Computer Science or Mathematics", "Publish research or build open-source ML projects", "Pursue an MS/PhD at a top university or join a research lab"],
        "entry_jobs": ["ML Engineer", "Data Scientist", "AI Research Intern", "NLP / CV Engineer"],
        "links": [
            ("fast.ai – Practical Deep Learning (free)", "https://www.fast.ai"),
            ("DeepLearning.AI – Andrew Ng Courses", "https://www.deeplearning.ai"),
            ("MIT OpenCourseWare – Introduction to Machine Learning", "https://ocw.mit.edu/courses/6-867-machine-learning-fall-2006/"),
            ("Kaggle – Learn & Compete", "https://www.kaggle.com/learn"),
        ]
    },
    "data_scientist": {
        "title": "Data Scientist",
        "emoji": "📈",
        "description": "Data scientists collect, clean, analyze, and visualize complex datasets to uncover insights that guide decisions in business, science, and government. They use a combination of statistics, programming, and domain knowledge to answer meaningful questions, such as predicting customer behavior, tracking disease trends, or improving operations. This field is growing quickly and is in demand across many industries.",
        "salary": "$85,000 – $165,000",
        "growth": "36%",
        "hs_courses": ["AP Statistics", "AP Computer Science A", "AP Calculus", "AP Economics", "AP Psychology"],
        "extracurriculars": ["Kaggle competitions", "Statistics or math club", "Personal data analysis projects (sports stats, social media)", "DECA or business analytics competitions", "Data journalism projects for school newspaper"],
        "skills": ["Python & R programming", "Statistics & probability", "Data visualization (Tableau, Matplotlib)", "SQL & databases", "Machine learning basics"],
        "roadmap": ["Learn Python and statistics fundamentals", "Work through Kaggle Learn modules", "Earn a BS in Statistics, Math, or Computer Science", "Build a portfolio of data analysis projects", "Start as a Data Analyst and grow into Data Scientist roles"],
        "entry_jobs": ["Data Analyst", "Business Intelligence Analyst", "Junior Data Scientist", "Analytics Engineer"],
        "links": [
            ("Kaggle Learn – Free Data Science Courses", "https://www.kaggle.com/learn"),
            ("Coursera – IBM Data Science Professional Certificate", "https://www.coursera.org/professional-certificates/ibm-data-science"),
            ("DataCamp – Interactive Data Science Courses", "https://www.datacamp.com"),
            ("Towards Data Science (Medium publication)", "https://towardsdatascience.com"),
        ]
    },
    "cybersecurity_analyst": {
        "title": "Cybersecurity Analyst",
        "emoji": "🛡️",
        "description": "Cybersecurity analysts protect computer systems, networks, and data from digital attacks, unauthorized access, and security weaknesses. As technology connects more of the world, the responsibility increases, including securing hospitals, power grids, and personal financial information. This career requires both technical accuracy and creative problem-solving, because understanding how hackers operate is essential to stopping them.",
        "salary": "$80,000 – $150,000",
        "growth": "32%",
        "hs_courses": ["AP Computer Science A", "AP Computer Science Principles", "Intro to Cybersecurity (if offered)", "Statistics", "AP Physics"],
        "extracurriculars": ["CyberPatriot competition", "TryHackMe or HackTheBox (ethical hacking platforms)", "CTF (Capture the Flag) competitions", "Coding club or cybersecurity club", "Certify early: CompTIA IT Fundamentals+"],
        "skills": ["Network security fundamentals", "Linux & command line", "Threat analysis & incident response", "Scripting (Python, Bash)", "Analytical & investigative thinking"],
        "roadmap": ["Learn basic networking and Linux command line", "Practice on TryHackMe or HackTheBox", "Earn a BS in Cybersecurity, CS, or IT", "Get CompTIA Security+ certification", "Start as a SOC Analyst and specialize from there"],
        "entry_jobs": ["SOC Analyst (Tier 1)", "IT Security Analyst", "Junior Penetration Tester", "Information Security Associate"],
        "links": [
            ("TryHackMe – Beginner Cybersecurity Learning", "https://tryhackme.com"),
            ("CompTIA Security+ Certification", "https://www.comptia.org/certifications/security"),
            ("Cybrary – Free Cybersecurity Courses", "https://www.cybrary.it"),
            ("SANS Cyber Aces (free intro training)", "https://www.cyberaces.org"),
        ]
    },
    "mathematician": {
        "title": "Mathematician / Statistician",
        "emoji": "∑",
        "description": "Mathematicians and statisticians create new mathematical theories or use existing ones to solve practical problems in finance, engineering, physics, medicine, and public policy. Statisticians are especially in high demand, interpreting clinical trial data, forecasting economic trends, and analyzing large datasets that influence many fields. If you enjoy abstract reasoning, this career allows you to put that skill to powerful use.",
        "salary": "$75,000 – $140,000",
        "growth": "30%",
        "hs_courses": ["AP Calculus BC", "AP Statistics", "AP Computer Science", "AP Physics C", "Linear Algebra/Calculus III (if available)"],
        "extracurriculars": ["AMC / AIME / MATHCOUNTS competitions", "Math team or club", "Statistics projects (data collection & analysis)", "Chess club (logical reasoning)", "Science fair with a mathematical modeling focus"],
        "skills": ["Advanced calculus & linear algebra", "Statistical modeling", "Programming (R, Python, MATLAB)", "Logical & abstract reasoning", "Written & verbal communication of complex ideas"],
        "roadmap": ["Compete in AMC and math olympiads", "Take AP Calculus BC and Statistics", "Earn a BS in Mathematics or Statistics", "Pursue internship in finance, actuarial science, or research", "Consider graduate study or actuarial certification (ASA/FSA)"],
        "entry_jobs": ["Actuarial Analyst", "Statistical Analyst", "Operations Research Analyst", "Quantitative Analyst (Junior)"],
        "links": [
            ("Art of Problem Solving – Math Competitions", "https://artofproblemsolving.com"),
            ("MIT OpenCourseWare – Mathematics", "https://ocw.mit.edu/courses/mathematics/"),
            ("Coursera – Statistics with Python (U of Michigan)", "https://www.coursera.org/specializations/statistics-with-python"),
            ("Society of Actuaries – Student Resources", "https://www.soa.org/programs/actuarial-careers/"),
        ]
    },
    "physician": {
        "title": "Physician",
        "emoji": "🩺",
        "description": "Physicians diagnose and treat injuries, illnesses, and chronic conditions while building long-term relationships with their patients. Medicine is a highly demanding career that requires many years of education and residency, but it is also one of the most respected and rewarding professions. With a vast amount of fields, any one of them will lead to a career where you make a meaningful difference in people's lives.",
        "salary": "$200,000 – $400,000+",
        "growth": "3%",
        "hs_courses": ["AP Biology", "AP Chemistry", "AP Physics", "AP Psychology", "Statistics"],
        "extracurriculars": ["Hospital or clinic volunteering", "EMT or CNA certification (optional)", "Health professions club", "Research internship at a university lab", "Community health outreach programs"],
        "skills": ["Scientific reasoning & clinical judgment", "Empathy & bedside manner", "Communication (patient & team)", "Resilience under pressure", "Attention to detail & memory"],
        "roadmap": ["Excel in AP sciences and take pre-med courses", "Volunteer in hospitals, clinics, or research labs", "Earn a BS on a pre-med track (Biology, Chemistry, or related)", "Prepare for and take the MCAT; apply to medical school (MD or DO)", "Complete residency (3–7 years) and board certification"],
        "entry_jobs": ["Medical Intern (PGY-1)", "Resident Physician", "Clinical Research Coordinator", "Medical Scribe (pre-med)"],
        "links": [
            ("AAMC – Pre-Med and Medical School Resources", "https://www.aamc.org/students/applying"),
            ("Khan Academy – MCAT Prep (free)", "https://www.khanacademy.org/test-prep/mcat"),
            ("Coursera – Anatomy Specialization (U of Michigan)", "https://www.coursera.org/specializations/anatomy"),
            ("Shadow Health – Virtual Patient Simulations", "https://www.shadowhealth.com"),
        ]
    },
    "neuroscientist": {
        "title": "Neuroscientist",
        "emoji": "🧠",
        "description": "Neuroscientists study the brain and nervous system to understand perception, memory, emotion, behavior, and consciousness while working to find treatments for disorders such as Alzheimer's, depression, and Parkinson's. This field is constantly growing because, despite decades of research, the human brain remains deeply mysterious. Neuroscience appeals to people who want to combine biology, psychology, chemistry, and computer science to explore one of the most complex objects we know of.",
        "salary": "$70,000 – $140,000",
        "growth": "10%",
        "hs_courses": ["AP Biology", "AP Psychology", "AP Chemistry", "AP Statistics", "AP Computer Science Principles"],
        "extracurriculars": ["Shadow a neurologist or psychiatrist", "Psychology club or mental health awareness group", "Neuroscience research assistant (university programs)", "Science fair with a neuroscience or cognitive focus", "Read journals like Neuron or Nature Neuroscience"],
        "skills": ["Experimental design & lab techniques", "Data analysis (MATLAB, Python)", "Scientific writing & literature review", "Critical thinking", "Empathy & ethics in research"],
        "roadmap": ["Take AP Biology and Psychology seriously", "Shadow a neurologist or psychiatric professional", "Earn a BS in Neuroscience, Biology, or Psychology", "Work in a university neuroscience lab as an undergrad", "Pursue a PhD in Neuroscience for research careers"],
        "entry_jobs": ["Research Assistant", "Lab Technician (Neuroscience)", "Clinical Research Coordinator", "Behavior Technician"],
        "links": [
            ("Society for Neuroscience – Education Resources", "https://www.sfn.org/education"),
            ("Neuroscience News – Free Articles & Research", "https://neurosciencenews.com"),
            ("Coursera – Medical Neuroscience (Duke University)", "https://www.coursera.org/learn/medical-neuroscience"),
            ("edX – The Brain and Space (Duke University)", "https://www.edx.org/learn/neuroscience"),
        ]
    },
    "pharmacist": {
        "title": "Pharmacist",
        "emoji": "💊",
        "description": "Pharmacists are experts in medications who make sure patients receive safe and effective treatments while advising them on proper use, side effects, and interactions. They work not only in retail pharmacies but also in hospitals, research labs, pharmaceutical companies, and public health agencies. This career combines in-depth scientific knowledge with direct, meaningful patient care every day.",
        "salary": "$120,000 – $160,000",
        "growth": "3%",
        "hs_courses": ["AP Chemistry", "AP Biology", "AP Statistics", "AP Calculus", "AP Psychology"],
        "extracurriculars": ["Pharmacy technician volunteer or part-time work", "Health professions club", "Hospital or clinic shadowing", "Science fair with a pharmacology or health focus", "APhA-ASP student chapter (college preview programs)"],
        "skills": ["Pharmacology & drug interactions", "Patient counseling & communication", "Attention to detail & accuracy", "Mathematics & dosage calculations", "Ethics & confidentiality"],
        "roadmap": ["Excel in chemistry and biology", "Volunteer or work part-time at a pharmacy", "Complete pre-pharmacy undergraduate coursework", "Earn a Doctor of Pharmacy — 4-year professional degree", "Pass NAPLEX and MPJE licensing exams"],
        "entry_jobs": ["Pharmacy Technician", "PharmD Intern", "Clinical Pharmacist (Resident)", "Drug Information Specialist"],
        "links": [
            ("AACP – Find a Pharmacy School", "https://www.aacp.org"),
            ("NAPLEX Prep – NABP Resources", "https://nabp.pharmacy"),
            ("Khan Academy – Pharmacology Basics", "https://www.khanacademy.org/science/health-and-medicine/pharmacology"),
            ("Coursera – Drug Discovery (UC San Diego)", "https://www.coursera.org/learn/drug-discovery"),
        ]
    },
    "environmental_scientist": {
        "title": "Environmental Scientist",
        "emoji": "🌿",
        "description": "Environmental scientists study the natural world and how human activity affects ecosystems, air, water, and soil. They collaborate with governments, NGOs, corporations, and communities to create solutions that protect natural resources and maintain a livable planet. Environmental science draws from biology, chemistry, geology, policy, and economics to tackle some of the most urgent challenges of our time.",
        "salary": "$60,000 – $120,000",
        "growth": "7%",
        "hs_courses": ["AP Environmental Science", "AP Biology", "AP Chemistry", "AP Statistics", "AP Government / Politics"],
        "extracurriculars": ["Environmental club or Green Team", "Local conservation volunteering (parks, rivers, wildlife)", "iNaturalist or eBird citizen science", "Model UN (environmental committees)", "Science fair with an environmental focus"],
        "skills": ["Field data collection & sampling", "GIS & spatial analysis", "Environmental regulations knowledge", "Report writing & policy communication", "Collaboration with diverse stakeholders"],
        "roadmap": ["Join environmental clubs and volunteer for conservation", "Take AP Environmental Science and Biology", "Earn a BS in Environmental Science or related field", "Intern with the EPA, a state agency, or an NGO", "Pursue field research or government/consulting roles"],
        "entry_jobs": ["Environmental Technician", "Contact Tracer", "Conservation Aide", "Environmental Compliance Analyst"],
        "links": [
            ("EPA – Student Environmental Resources", "https://www.epa.gov/students"),
            ("NRDC – Environmental Career Resources", "https://www.nrdc.org/about/careers"),
            ("Coursera – Our Earth: Its Climate, History and Processes", "https://www.coursera.org/learn/our-earth"),
            ("National Geographic Education – Environmental Science", "https://education.nationalgeographic.org"),
        ]
    },
    "climate_engineer": {
        "title": "Clean Energy Engineer",
        "emoji": "☀️",
        "description": "Clean energy engineers design and construct systems that support a sustainable future, including solar panels, wind turbines, energy storage, smart grids, carbon capture, and green hydrogen. This career is one of the most urgent and fast-growing fields as governments and companies work to decarbonize the global economy. If you want to develop solutions to climate change, this is a field where your skills can have a major impact.",
        "salary": "$75,000 – $150,000",
        "growth": "11%",
        "hs_courses": ["AP Physics C", "AP Chemistry", "AP Environmental Science", "AP Calculus", "Pre-Engineering / CAD"],
        "extracurriculars": ["Solar car or wind turbine competitions", "Engineers Without Borders student chapter", "Science fair with a renewable energy focus", "FIRST Robotics or TSA engineering events", "Follow clean energy news (Canary Media, CleanTechnica)"],
        "skills": ["Electrical & mechanical engineering principles", "Energy systems modeling", "CAD & simulation software", "Project management", "Sustainability analysis & lifecycle thinking"],
        "roadmap": ["Take AP Physics and environmental sciences", "Follow clean energy news and research trends", "Earn a BS in Environmental, Chemical, or Electrical Engineering", "Intern at a renewable energy company or national lab", "Specialize in solar, wind, storage, or grid systems"],
        "entry_jobs": ["Solar Installation Engineer", "Energy Analyst", "Sustainability Consultant", "Renewable Energy Technician"],
        "links": [
            ("U.S. Department of Energy – Student Programs", "https://www.energy.gov/careers"),
            ("IRENA – Youth & Clean Energy Resources", "https://www.irena.org/youth"),
            ("edX – Sustainable Energy (TU Delft)", "https://www.edx.org/learn/sustainable-energy"),
            ("Coursera – Solar Energy Engineering (DTU)", "https://www.coursera.org/learn/solar-energy-engineering"),
        ]
    },
    "public_health_researcher": {
        "title": "Public Health Researcher",
        "emoji": "🏥",
        "description": "Public health researchers examine patterns of health and disease across populations to prevent illness and reduce health disparities. They address issues such as pandemic preparedness, childhood nutrition, and gun violence while shaping policies that can save thousands or even millions of lives. This career combines rigorous scientific work with a strong social conscience.",
        "salary": "$60,000 – $120,000",
        "growth": "13%",
        "hs_courses": ["AP Biology", "AP Statistics", "AP Psychology", "AP Government", "AP Environmental Science"],
        "extracurriculars": ["Community health volunteering", "Red Cross or public health campaigns", "Model UN – Health or humanitarian committees", "Research internship (university or hospital)", "Science fair with a health disparities or epidemiology focus"],
        "skills": ["Epidemiology & biostatistics", "Survey design & data collection", "Policy writing & advocacy", "Community outreach & communication", "Critical analysis of health literature"],
        "roadmap": ["Volunteer with community health organizations", "Take statistics and social science courses seriously", "Earn a BS in Public Health, Biology, or a related field", "Pursue a Master of Public Health (MPH) degree", "Work with CDC, WHO, local health departments, or NGOs"],
        "entry_jobs": ["Community Health Worker", "Epidemiologist Assistant", "Health Educator", "Research Coordinator (Public Health)"],
        "links": [
            ("APHA – Student Resources & Careers", "https://www.apha.org/Professional-Development/Students"),
            ("CDC – Public Health Career Pathways", "https://jobs.cdc.gov"),
            ("Coursera – Global Health (Duke University)", "https://www.coursera.org/learn/global-health"),
            ("edX – Public Health Essentials (Harvard)", "https://www.edx.org/learn/public-health"),
        ]
    },
}

# scoring logic
def score_quiz(answers):
    scores = {"investigator": 0, "builder": 0, "innovator": 0, "analyst": 0, "healer": 0, "changer": 0}
    for answer in answers:
        if answer in scores:
            scores[answer] += 1
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top_persona = sorted_scores[0][0]
    second_persona = sorted_scores[1][0] if sorted_scores[1][1] > 0 else None
    return top_persona, second_persona, scores


# routing logic, redirect user to correct pages
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/quiz")
def quiz():
    session.clear()
    return render_template("quiz.html", questions=QUESTIONS, total=len(QUESTIONS))

@app.route("/submit", methods=["POST"])
def submit():
    answers = []
    for i in range(1, len(QUESTIONS) + 1):
        answer = request.form.get(f"q{i}")
        if answer:
            answers.append(answer)
    top_persona, second_persona, scores = score_quiz(answers)
    persona_data = PERSONAS[top_persona]
    second_data = PERSONAS.get(second_persona) if second_persona else None
    careers_data = [CAREERS[c] for c in persona_data["careers"] if c in CAREERS]
    return render_template(
        "results.html",
        persona=persona_data,
        persona_key=top_persona,
        second=second_data,
        careers=careers_data,
        scores=scores,
        all_personas=PERSONAS,
        all_careers=CAREERS
    )

@app.route("/explore")
def explore():
    return render_template("explore.html", careers=CAREERS, personas=PERSONAS)


if __name__ == "__main__":
    app.run(debug=True)
