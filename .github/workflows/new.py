import csv
import os

csv_file_path = os.environ['csv_path']
 
with open(csv_file_path, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        branch_name = row['BranchName']
        build_number = row['BuildNumber']
        workflow_type = row['WorkflowType']
        instance_count = row['InstanceCount']
        instance_name = row['InstanceName']
        shared_module_instance_name = row['SharedModuleInstanceName']

        print(f"procesing {instance_name} from branch {branch_name}")
  #  row = next(csv_reader)
 
  #  os.environ['BRANCH_NAME'] = row['BranchName']
  #  os.environ['BUILD_NUMBER'] = row['BuildNumber']
  # os.environ['WORKFLOW_TYPE'] = row['WorkflowType']
  #  os.environ['INSTANCE_COUNT'] = row['InstanceCount']
  #  os.environ['INSTANCE_NAME'] = row['InstanceName']
  #  os.environ['SHARED_MODULE_INSTANCE_NAME'] = row['SharedModuleInstanceName']
