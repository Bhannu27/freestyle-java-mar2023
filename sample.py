import csv
import os
 
csv_file_path = os.environ['csv_path']
 
with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    row = next(csv_reader)  # Assuming only one row in the CSV, adjust if needed
 
    # Extract values from the row
    values = [row['BranchName'], row['BuildNumber'], row['WorkflowType'], row['InstanceName'], row['InstanceCount'], row['SharedModuleInstanceName']]
 
    # Assign values to variables
    branch_name, build_number, workflow_type, instance_name, instance_count, shared_module_instance_name = values
 
    # Print original csv_values
    csv_values = ",".join(values)
    #print("values:", '{csv_values}')
    print("Branch Name Variable:", branch_name)
    print("Build Number Variable:", build_number)
    print("Workflow Type Variable:", workflow_type)
    print("Instance Name Variable:", instance_name)
    print("Instance Count Variable:", instance_count)
    print("Shared Module Instance Name Variable:", shared_module_instance_name)
