# list comprehension
# [new_value for item in iterable if condition]
# for index, instance in enumerate(instances):
#     print(index, instance)
import json
from json import JSONDecodeError
def load_data(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Error: file not found")
        return None
    except JSONDecodeError:
        print("Error: invalid JSON format")
        return None
    else: 
        return data

def get_running_instances(data):
    running_instances = [
                            instance['InstanceId']
                            for instance in data["Instances"]
                            if instance["State"] == "running"
                            
                        ]
    return running_instances

data = load_data('ec2_data.json')
run_inst = get_running_instances(data)
print(run_inst)

numbers = [1,2,3,4,5,6]
even = [num for num in numbers if num%2==0]
print(even)


# working with enumerate
instances = ["i-1","i-2","i-3","i-4"]
for index, instance in enumerate(instances, start=1):
    print(f"{index}. Instance ID: {instance}")
    
instanc = {
    "InstanceId": "i-123",
    "InstanceType": "t3.micro",
    "State": "running"
}

for key, value in instanc.items():
    print(f"{key} → {value}")