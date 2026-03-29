# Python AWS Automation Journey

This repository contains my learning journey as I build Python skills specifically for cloud infrastructure and AWS automation.

Instead of learning Python in isolation, I focused on using it in a practical context. The scripts here are designed to reflect how cloud and DevOps engineers actually work: processing structured data, interacting with infrastructure-like responses, and generating useful outputs.

---

## Goal

My goal is to become a Cloud Infrastructure Engineer who can:

- Automate AWS-related tasks using Python  
- Work comfortably with AWS-style API responses  
- Write clean, structured, and maintainable scripts  
- Build practical tools that solve real infrastructure problems  

This work is part of a structured 12-week plan toward becoming job-ready.

---

## Approach

My focus has been on understanding how things work rather than just writing code that runs.

I try to:

- Understand how data moves through a script (input, processing, output)  
- Build small tools instead of isolated exercises  
- Improve code step by step instead of rewriting everything  
- Follow patterns that are actually used in cloud environments  

---

## Repository Structure
- week1/
- week2/


Each week builds on the previous one. The structure reflects progression in both technical skills and problem-solving approach.

---

## Week 1 – Foundations

Focus: Core Python for automation

Covered:

- Dictionaries and nested data  
- Loops and iteration  
- JSON parsing  
- Basic file handling  
- Filtering and extracting data  

Built:

- Scripts to read and process AWS-like JSON data  
- Basic filtering of EC2-style data  
- Simple text-based reports  

---

## Week 2 – Automation Patterns

Focus: Writing structured and reusable scripts

Covered:

- Functions and modular design  
- Logging instead of print statements  
- Command-line tools using argparse  
- CSV report generation  
- Cleaner data processing using list comprehensions  

Built:

- A CLI-based EC2 reporting tool  
- Scripts structured into reusable components  
- Logging-enabled automation scripts  

---

## Week 3 – Real-World Data Handling

Focus: Working with realistic cloud data structures

Covered:

- Deeply nested AWS-style data (Reservations → Instances → NetworkInterfaces)  
- Defensive coding using `.get()`  
- Handling missing or optional fields  
- Extracting data from multiple levels  
- Separating data source from processing logic  

Built:

- Scripts that handle complex nested data safely  
- Tools that output structured reports in CSV and text formats  
- Code designed to later integrate with real AWS APIs  

---

## Skills Demonstrated

- Parsing and transforming JSON data  
- Working with nested and complex data structures  
- Writing defensive, error-tolerant code  
- Building command-line tools  
- Using logging for visibility and debugging  
- Generating structured outputs (CSV and text)  
- Organizing code with clear separation of responsibilities  

---

## Current State

At this point, I am comfortable:

- Writing Python scripts for automation  
- Working with data structures similar to AWS API responses  
- Building small tools that reflect real infrastructure tasks  

---

## Next Steps

- Integrate Boto3 to work with real AWS data  
- Automate common infrastructure tasks  
- Build more polished, standalone projects  
- Improve CLI usability and logging structure  

---

## Final Note

This repository is a record of progress.

It shows how I approach learning, how I break down problems, and how I improve over time. The focus is not just on writing code, but on developing the skills and thinking required to work in cloud infrastructure.