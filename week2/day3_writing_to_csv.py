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
def get_running_instances(data):
    running_instances = [
        {"id": instance['InstanceId'], 
         "type": instance['InstanceType'],
         "state": instance['State']
         }
        for instance in data['Instances']
        if instance['State'] == "running"
        
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
                file.write(f"Instance {instance['id']} ({instance['type']}) is {instance['state']} \n")
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