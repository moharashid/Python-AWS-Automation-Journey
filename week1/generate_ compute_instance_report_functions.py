import json
# reads JSON
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)   
    return data

# processes data
def get_running_instances(data):
    running_instances = []
    for instance in data["Instances"]:
        if instance["State"] == "running":
            running_instances.append(instance["InstanceId"])
    return running_instances

# save output
def save_report(filename, running_instances):
    with open(filename, 'w') as file:
        for instance_id in running_instances:
            file.write(f"Running Instance: {instance_id}\n")
        file.write(f"Total running instances: {len(running_instances)}\n")

def main():
    data = load_data("ec2_data.json")
    running_instances = get_running_instances(data)
    report = "report.txt"
    save_report(report, running_instances)
    
if __name__ == "__main__":
    main()