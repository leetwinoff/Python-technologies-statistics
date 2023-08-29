from urllib.parse import urljoin

ALL_TECHNOLOGIES = [
    "Python", "OOP", "NLTK", "Spacy", "Gensim", "TextBlob", "nltk", "spaCy", "Gensim", "Pattern", "Scrapy", "BeautifulSoup",
    "Requests", "Pillow", "feedparser", "lxml", "Flask", "Django", "FastAPI", "Pyramid", "Flask-RESTful",
    "Sanic", "Dash", "Streamlit", "Plotly", "Bokeh", "Matplotlib", "Seaborn", "SciPy", "NumPy", "Pandas",
    "Scikit-learn", "Statsmodels", "XGBoost", "LightGBM", "CatBoost", "TensorFlow", "PyTorch", "Keras",
    "Theano", "Selenium", "Celery",
    "HTML/CSS", "JavaScript", "React", "Angular", "Vue.js", "Django REST framework",
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis",
    "Git", "GitHub", "GitLab", "Bitbucket",
    "AWS", "GCP",  "Azure",
    "Docker", "Kubernetes",
    "Jenkins", "Travis CI", "CircleCI",
    "REST", "GraphQL",
    "OAuth", "JWT",
    "HTTP", "HTTPS", "APIs",
    "Unit Testing", "Selenium",
    "Ansible", "Puppet", "Chef", "Terraform"
]

ALL_TECHNOLOGIES_LOWER = [tech.lower() for tech in ALL_TECHNOLOGIES]

BASE_URL = "https://djinni.co/jobs/"
PYTHON_VACANCIES = urljoin(BASE_URL, "?all-keywords=&any-of-keywords=&exclude-keywords=&primary_keyword=Python")

VACANCY_OUTPUT_CSV_PATH = "vacancies.csv"