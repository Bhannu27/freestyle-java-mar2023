import csv
import os

csv_file_path = os.environ['csv_path']

with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    row = next(csv_reader)

    # Extract values from the row
    branch_name = row.get('BranchName', '')
    build_number = row.get('BuildNumber', '')
    workflow_type = row.get('WorkflowType', '')
    instance_name = row.get('InstanceName', '')
    instance_count = row.get('InstanceCount', '')
    shared_module_instance_name = row.get('SharedModuleInstanceName', '')

    # Print csv_values
    csv_values = ",".join([branch_name, build_number, workflow_type, instance_name, instance_count, shared_module_instance_name])
    print("CSV Values:", csv_values)

    # Print variables for verification
    print("Branch Name:", branch_name)
    print("Build Number:", build_number)
    print("Workflow Type:", workflow_type)
    print("Instance Name:", instance_name)
    print("Instance Count:", instance_count)
    print("Shared Module:", shared_module_instance_name)
