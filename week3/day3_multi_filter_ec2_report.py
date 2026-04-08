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
        

# simulate fetch ec2 data, later will be replaced with boto3 API call
# This function acts as a data source abstraction layer
# Currently reads from JSON file
# Later we will replace this with real AWS API (boto3)
def fetch_ec2_data():
    return load_json("ec2_data_filtering.json") 

# [new_value for item in iterable if condition]

# get the running instances  
def get_running_instances(data,environment,state,instance_type):
    running_instances = []
    for reservation in data.get('Reservations', []):
        for instance in reservation.get('Instances',[]):
            # check if instance is running
            if state and instance.get('State',{}).get('Name') != state:
                continue
            if instance_type and instance.get('InstanceType') != instance_type:
                continue
            # check if env is development/production
            if environment:
                is_env_match = False
                for tag in instance.get('Tags', []):
                    if tag.get('Key') == "Environment" and tag.get('Value') == environment:
                        is_env_match = True
                        break
                if not is_env_match:
                    continue
            # check if instance is present
            # if instance.get('InstanceType') != instance_type:
            #     continue   
            interfaces = instance.get('NetworkInterfaces',[])
            if interfaces:
                for interface in interfaces:
                    running_instances.append(
                        {
                            "instance_id": instance.get('InstanceId'), 
                            "instance_type": instance.get('InstanceType'), 
                            "state": instance.get('State',{}).get('Name', 'N/A'), 
                            "private_ip": interface.get('PrivateIpAddress', 'N/A'), 
                            "public_ip": interface.get('Association', {}).get('PublicIp', 'N/A')
                        }            
                    )  
                    # break  
            else:
                running_instances.append(
                {
                    "instance_id": instance.get('InstanceId'), 
                    "instance_type": instance.get('InstanceType'), 
                    "state": instance.get('State',{}).get('Name', 'N/A'), 
                    "private_ip": "N/A", 
                    "public_ip": "N/A"
                }
                
                )
    return running_instances

# save report to file
def save_report(filename, running_instances, output_format):
    logging.info(f"Writing {output_format} report to {filename}")
    if output_format == "csv":
        with open(filename, 'w',newline='') as file:
            # InstanceId | Type | State | Private IP | Public IP | environment
            fieldnames =  ['instance_id', 'instance_type', 'state', 'private_ip','public_ip']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for instance in running_instances:
                writer.writerow(instance)
    else:
        with open(filename, 'w') as file:
            for instance in running_instances:
                file.write(f"Instance {instance['instance_id']} ({instance['instance_type']}) is {instance['state']} with public IP {instance['public_ip']} and private IP {instance['private_ip']}\n")
            file.write(f"Found {len(running_instances)} running network records\n")
    logging.info(f"Report successfully written to {filename}")
    
    
def main():
    # Create Argument Parser, description is shown when you run --help
    parser = argparse.ArgumentParser(description="EC2 Instance Report Script")
    parser.add_argument("output_file", help="Path to output report file")
    parser.add_argument(
        "--format",
        choices=["csv", "text"],
        default="csv",
        help="Output format (csv or text)"
    )
    parser.add_argument(
        "--env",
        choices=["Dev", "Production"],
        default = "",
        help="Specify environment (Dev or Production or leave empty if no environment specified)"
    )
    parser.add_argument(
        "--state",
        default = None,
        choices=["running","stopped"],
        help="Enter state, (running or stopped)"
    )
    parser.add_argument(
        "--instance_type",
        default = None,
        help="Enter EC2 instance instance_type"
    )
    
    args = parser.parse_args()
    data = fetch_ec2_data()
    if data is None:
        logging.error("Stopping script due to data loading failure")
        return
    running_instances = get_running_instances(data,args.env,args.state,args.instance_type)
    output_file = f'{args.output_file}_{args.env}' if args.env else args.output_file
    save_report(output_file, running_instances, args.format)
    

if __name__ == "__main__":
    main()