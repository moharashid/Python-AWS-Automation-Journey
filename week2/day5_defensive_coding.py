# use argpase for cleaner way to accept input from the command line (CLI) on the CLI rather than hardcoding them
import argparse
import csv
import json
# use Python's in-built logging library for logging automation scripts, replacing print() statements
import logging
# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
# load JSON file
def load_json(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                logging.info(f"{filename} loaded successfully!")
                return data
        except FileNotFoundError:
            logging.error(f"{filename} not found!")
            return None
    
        except json.JSONDecodeError:
            logging.error(f"{filename} not a valid JSON file!")
            return None

# [new_value for item in iterable if condition]

# get the running instances 
"""
===============================
PYTHON .get() — SAFE DATA ACCESS
===============================

The .get() method is used to safely access values from dictionaries
without causing errors if a key is missing.

--------------------------------
BASIC USAGE
--------------------------------

dictionary.get(key, default_value)

- If the key exists → returns its value
- If the key does NOT exist → returns the default value (or None if not provided)

Example:

data = {"name": "John"}

data.get("name")        → "John"
data.get("age")         → None
data.get("age", 0)      → 0

--------------------------------
WHY NOT USE dictionary[key]?
--------------------------------

Using direct access:

data["age"]

→ Raises KeyError if "age" does not exist

Using .get():

data.get("age")

→ Returns None (safe, no crash)

--------------------------------
NESTED .get() (VERY IMPORTANT)
--------------------------------

When working with nested dictionaries (common in AWS/Boto3 responses):

instance.get("State", {}).get("Name")

Step-by-step:
1. instance.get("State", {})
   - If "State" exists → returns dictionary
   - If missing → returns empty dictionary {}

2. {}.get("Name") → returns None (safe)

This prevents crashes like:

KeyError: 'State'

--------------------------------
WHY USE {} AS DEFAULT?
--------------------------------

We use {} (empty dictionary) when we expect to call .get() again.

Example:

instance.get("State", {}).get("Name")

If we used [] instead:

instance.get("State", []).get("Name")

→ ERROR: list has no .get()

--------------------------------
WHY USE [] IN OTHER CASES?
--------------------------------

We use [] (empty list) when looping:

for reservation in data.get("Reservations", []):
    ...

Reason:
- for-loops expect an iterable (like a list)
- [] means "loop zero times" → safe

--------------------------------
RULE OF THUMB
--------------------------------

Use {} → when accessing dictionary keys (.get())
Use [] → when looping (for-loops)

--------------------------------
REAL AWS EXAMPLE
--------------------------------

data.get("Reservations", [])
    → list of reservations

reservation.get("Instances", [])
    → list of instances

instance.get("State", {}).get("Name")
    → safely access nested state

--------------------------------
WHY THIS MATTERS
--------------------------------

In real cloud environments (AWS, APIs):

- Data is often incomplete
- Some fields are optional
- Scripts MUST NOT crash

Using .get() makes scripts:
✔ robust
✔ production-ready
✔ safe against missing data

--------------------------------
SUMMARY
--------------------------------

.get() helps:
✔ avoid KeyError
✔ safely access nested data
✔ write defensive code
✔ handle real-world API responses

This is a critical skill for:
- Cloud Engineers
- DevOps Engineers
- Automation Scripts
"""

 
def get_running_instances(data):
    running_instances = [
    {
        "id": instance.get('InstanceId'),
        "type": instance.get('InstanceType'),
        "state": instance.get('State', {}).get('Name')
    }
    for reservation in data.get('Reservations', [])
    for instance in reservation.get('Instances',[])
    if instance.get('State',{}).get('Name') == "running"
    ]
    logging.info(f"Found {len(running_instances)} running instances")
    return running_instances

# save report to file
def save_report(filename, running_instances, output_format):
    logging.info(f"Writing {output_format} report to {filename}")
    if output_format == "csv":
        with open(filename, 'w',newline='') as file:
            fieldnames =  ['id', 'type', 'state']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for instance in running_instances:
                writer.writerow(instance)
    else:
        with open(filename, 'w') as file:
            for instance in running_instances:
                file.write(f"Instance {instance['id']} ({instance['type']}) is {instance['state']}\n")
            file.write(f"Total running instances: {len(running_instances)}")
    logging.info(f"Report successfully written to {filename}")
    
    
def main():
    # Create Argument Parser, description is shown when you run --help
    parser = argparse.ArgumentParser(description="EC2 Instance Report Script")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("output_file", help="Path to output report file")
    parser.add_argument(
        "--format",
        choices=["csv", "text"],
        default="csv",
        help="Output format (csv or text)"
)
    
    args = parser.parse_args()
    data = load_json(args.input_file)
    if data is None:
        logging.error("Stopping script due to data loading failure")
        return
    running_instances = get_running_instances(data)
    
    save_report(args.output_file, running_instances, args.format)
    

if __name__ == "__main__":
    main()