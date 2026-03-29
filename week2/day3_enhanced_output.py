# use argpase for cleaner way to accept input from the command line (CLI) on the CLI rather than hardcoding them
import argparse
import json
# use Python's in-built logging library for logging automation scripts, replacing print() statements
import logging
# configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_json(filename):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                logging.info(f"{filename} loaded succesfully!")
                return data
        except FileNotFoundError:
            logging.error(f"{filename} not found!")
            return None
    
        except json.JSONDecodeError:
            logging.error(f"{filename} not a valid JSON file!")
            return None

# [new_value for item in iterable if condition]
  
def get_running_instances(data):
    running_instances = [
        {"id": instance['InstanceId'], 
         "type": instance['InstanceType']
         }
        for instance in data['Instances']
        if instance['State'] == "running"
        
    ]
    logging.info(f"Found {len(running_instances)} running instances")
    return running_instances

def save_report(filename, running_instances):
    with open(filename, 'w') as file:
        logging.info(f"Writing report to {filename}")
        for instance in running_instances:
            file.write(f"Instance {instance['id']} ({instance['type']}) is running \n")
        file.write(f"The total running instances: {len(running_instances)}")


def main():
    # Create Argument Parser, description is shown when you run --help
    parser = argparse.ArgumentParser(description="EC2 Instance Report Script")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("output_file", help="Path to output report file")

    args = parser.parse_args()
    data = load_json(args.input_file)
    if data is None:
        logging.error("Stopping script due to data loading failure")
        return
    running_instances = get_running_instances(data)
    
    save_report(args.output_file, running_instances)


if __name__ == "__main__":
    main()