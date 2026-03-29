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
''' 
basicConfig() - It configures how logging behaves.Without configuration, logging prints very minimal information.
level=logging.INFO - sets the minimum log level that will be displayed.
INFO has a higher priority than DEBUG, and so on
| Level    | Meaning                 |
| -------- | ----------------------- |
| DEBUG    | very detailed debugging |
| INFO     | normal script operation |
| WARNING  | something unexpected    |
| ERROR    | something failed        |
| CRITICAL | serious failure         |


format="%(asctime)s - %(levelname)s - %(message)s"
| Field           | Meaning                |
| --------------- | ---------------------- |
| `%(asctime)s`   | timestamp              |
| `%(levelname)s` | INFO / ERROR / WARNING |
| `%(message)s`   | the log message        |

'''
# writing log messages
logging.info("Script has started")
logging.debug("Script has started")

def load_data(filename):
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
    
# get the running instances
def get_running_instances(data):
    running_instances = [
        instance['InstanceId']
        for instance in data["Instances"]
        if instance["State"] == "running"
    ]
    logging.info(f"Found {len(running_instances)} running instances")
    return running_instances

# save the report
def save_report(filename,running_instances):
    with open(filename, 'w') as file:
        logging.info(f"begin writing running instances to {filename}")
        for instance_id in running_instances:
            file.write(f"Running Instance: {instance_id}\n")
        file.write(f"Total running instances: {len(running_instances)}\n")
        logging.info(f"writing to {filename} success")
            

def main():
    # Create Argument Parser, description is shown when you run --help
    parser = argparse.ArgumentParser(description="EC2 Instance Report Script")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("output_file", help="Path to output report file")

    args = parser.parse_args()
    data = load_data(args.input_file)
    if data is None:
        logging.error("Stopping script due to data loading failure")
        return
    running_instances = get_running_instances(data)
    
    save_report(args.output_file, running_instances)
    
if __name__ == "__main__":
    main()