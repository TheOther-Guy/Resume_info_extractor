#!/usr/bin/env python
# coding: utf-8

# ### for spacy installation use this link 
# - https://spacy.io/usage

# ### Most used re "regex" package methods
# - re.match()
# - re.search()
# - re.find_all()
# - re.split()
# - re.sub()
# - re.compile()

# In[1]:


#importing libraries
import pdfminer  # pdf2txt
import pandas as pd  # data manipulation
import re   # regular exression manipulation
import os   # operating system commands
import spacy  #NLP  "natural language processing"
import time  # just for the naming of the output CSV


# In[2]:


import pdf2txt #import the file we downloaded from pdfminer repo


# ## converting pdf to text

# In[3]:


def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath]) # pdf to text and save
    print(output_filepath + " " +"saved successfuly")
    return open(output_filepath, encoding='utf8').read()


# In[4]:


nlp = spacy.load("en_core_web_sm")  # Load the language model


# In[5]:


result_dict = {"name": [], "phone": [], "email": [], "skills": []}
names = []
phones = []
emails = []
skills = []


# ### regular expressoin for phone number credit to 
# - https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script/3868861#3868861

# In[6]:


def parse_content(text):
    skillset = re.compile("python|java|sql|tableau|excel")
    phone_num = re.compile(
    "(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
    )
    #phone_num = re.compile("phone|mobile|contact")
    doc = nlp(text)
    name = [entity.text for entity in doc.ents if entity.label_ == 'PERSON'][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction completed successfuly...\n")


# In[7]:


#iterating the folder "resumes" for multiple files 
for file in os.listdir("resumes/"):
    if file.endswith(".pdf"):
        print("Reading..." + file)
        txt = convert_pdf(os.path.join("resumes/", file))
        parse_content(txt)


# # Building the dictionary

# In[8]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email'] = emails
result_dict['skills'] = skills


# # Building a DataFrame from the dictionary

# In[10]:


result_df = pd.DataFrame(result_dict)


# # Constructing the file name

# In[45]:


# Here i used hyphin instead of slash to avoid windows reading slash as path separator
now = str(time.strftime("%d-%m-%Y")+ '.csv') # This will add the date of today to the file name
# bulding the file naming arguments
csv_path = 'output/csv/'
csv_name = 'parsed_resumes '


# In[46]:


# constructing the file name from the arguments above 
arg_for_expt = csv_path+csv_name+now


# In[47]:


# converting the DataFrame to a CSV for work collaboration
result_df.to_csv(arg_for_expt)

