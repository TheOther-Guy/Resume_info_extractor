get_ipython().getoutput("/usr/bin/env python")
-*- coding: utf-8 -*-


#importing libraries
import pdfminer  # pdf2txt
import pandas as pd  # data manipulation
import re   # regular exression manipulation
import os   # operating system commands
import spacy  #NLP  "natural language processing"


import pdf2txt


def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath]) # pdf to text and save
    print(output_filepath + " " +"saved successfuly")
    return open(output_filepath).read()


nlp = spacy.load("en_core_web_sm")  # Load the language model


result_dict = {"name": [], "phone": [], "email": [], "skills": []}
names = []
phones = []
emails = []
skills = []


def parse_content(text):
    skillset = re.compile("python|java|sql|tableau|excel")
    phone_num = re.compile(
    "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ == 'PERSON'][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.loawer()))
    skills_list = re.findall(skillset, text.loawer())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    email.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfuly...")


#iterating the folder "resumes" for multiple files 
for file in os.listdir("resumes/"):
    if file.endswith(".pdf"):
        print("Reading..." + file)
        txt = convert_pdf(os.path.join("resumes/", file))
        parse_content(txt)



