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

        print(f" {instance_name} from branch {branch_name}")
        command = ['bw.mc-new', instance_name]
        subprocess.run(command)
        result = {
            'branch_name': branch_name,
            'build_number': build_number,
            'workflow_type': workflow_type,
            'instance_count': instance_count,
            'instance_name': instance_name,
            'shared_module_instance_name': shared_module_instance_name
        }
        print("Processed data:", result)


  #  row = next(csv_reader)
 
  #  os.environ['BRANCH_NAME'] = row['BranchName']
  #  os.environ['BUILD_NUMBER'] = row['BuildNumber']
  # os.environ['WORKFLOW_TYPE'] = row['WorkflowType']
  #  os.environ['INSTANCE_COUNT'] = row['InstanceCount']
  #  os.environ['INSTANCE_NAME'] = row['InstanceName']
  #  os.environ['SHARED_MODULE_INSTANCE_NAME'] = row['SharedModuleInstanceName']
