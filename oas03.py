#import pyxnat
import os

# Replace these with your XNAT server details
xnat_url = 'https://central.xnat.org/'
#server_url = 'https://central.xnat.org/app/template/XDATScreen_report_xnat_projectData.vm/search_element/xnat:projectData/search_field/xnat:projectData.ID/search_value/OASIS3'
xnat_user = 'username'
xnat_pass = 'Password'

# Connect to the XNAT server
#central=pyxnat.Interface(server=server_url, user=username, password=password)

#central.get('OASIS3/OAS30001')

#print(central)

#import xnat
#session = xnat.connect(server_url, user='Sanazkv', password='Snz_0612078')
#session.subjects("")

#download(uri: str, target: str | Path


import os
import xnat

# Replace with the specific project, subject, and download path
project_id = 'OASIS3'
download_path = 'path_directory'

# Replace with the desired scan type
scan_type = 'ALL'  # Set to 'ALL' to download all scan types

# Specify the range of subject IDs you want to download
start_subject_id = 'OAS30002'
end_subject_id = 'OAS30003'



import os
import xnat

# Replace with the specific project, subject, and download path
project_id = 'OASIS3'
download_path = '/lustre06/project/6001250/sanazkv/oas/'

# Replace with the desired scan type
scan_type = 'ALL'  # Set to 'ALL' to download all scan types

# Specify the range of subject IDs you want to download
start_subject_id = 'OAS30024'
end_subject_id = 'OAS30050'

import os

# Connect to the XNAT server
with xnat.connect(xnat_url, user=xnat_user, password=xnat_pass) as session:
    project = session.projects[project_id]

    for subject_id in range(int(start_subject_id[6:]), int(end_subject_id[6:]) + 1):
        subject_id = f'OAS3{subject_id:04d}'  # Convert to the subject_id format

        subject = project.subjects[subject_id]

        # Create a folder for the subject in the download path
        subject_folder = os.path.join(download_path, subject_id)
        os.makedirs(subject_folder, exist_ok=True)

        # List all experiments for the subject
        experiments = subject.experiments.values()

        for experiment in experiments:
            experiment_id = experiment.label
            experiment_folder = os.path.join(subject_folder, experiment_id)
            os.makedirs(experiment_folder, exist_ok=True)

            try:
                # Download Resources
                for resource in experiment.resources.values():
                    resource_folder = os.path.join(experiment_folder, 'Resources', resource.label)
                    os.makedirs(resource_folder, exist_ok=True)

                    for file in resource.files.values():
                        file_filename = os.path.join(resource_folder, file.name)
                        file.download(file_filename)

                # Check if Assessors are available
                if hasattr(experiment, 'assessors'):
                    for assessor in experiment.assessors.values():
                        assessor_folder = os.path.join(experiment_folder, 'Assessors', assessor.label)
                        os.makedirs(assessor_folder, exist_ok=True)

                        for resource in assessor.resources.values():
                            resource_folder = os.path.join(assessor_folder, resource.label)
                            os.makedirs(resource_folder, exist_ok=True)

                            for file in resource.files.values():
                                file_filename = os.path.join(resource_folder, file.name)
                                file.download(file_filename)

                # Check if Scans are available
                if hasattr(experiment, 'scans'):
                    for scan in experiment.scans.values():
                        scan_folder = os.path.join(experiment_folder, 'Scans', scan.id)
                        os.makedirs(scan_folder, exist_ok=True)

                        for resource in scan.resources.values():
                            resource_folder = os.path.join(scan_folder, resource.label)
                            os.makedirs(resource_folder, exist_ok=True)

                            for file in resource.files.values():
                                file_filename = os.path.join(resource_folder, file.name)
                                file.download(file_filename)
            except Exception as e:
                print(f"Error processing experiment {experiment_id}: {str(e)}")

# Close the XNAT session
session.disconnect()













