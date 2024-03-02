You can create network troubleshooting labs on CML (Cisco Modeling Lab) with this tool.

# Requirements
- Cisco Modeling Lab >= 2.6.1
- Python >= 3.9.13

# Installation
After downloading this repository, run the following command:
```bash
# check the version of python
python --version

# create a virtual environment
python -m venv venv

# activate the virutal environment
## For Windows
./venv/Scripts/activate
## For Mac or Linux
./venv/bin/activate

# install python packages
pip install -r requirements.txt
```

# Usage
1. Create a lab on CML
<br>
First, create a lab on CML and export the lab.

2. Export the lab
<br>
You need to extract configs before exporting the lab.

3. Add wrong configurations
<br>
Add wrong configurations to the lab yaml file.
<br>
Here is an example.
Assume you want to add wrong IP address configurations for GigabitEthernet 0/0, you can write YAML file as follows:
```
interface GigabitEthernet 0/0
#TShoot_Start
Correct:
    conf: ip address 192.168.0.1 255.255.255.0
    description: The address of Gig 0/0 should be "192.168.0.1/24"
Wrong:
    - conf: ip address 192.168.0.2 255.255.255.0
      description: The IP address of Gig0/0 is incorrect
    - conf: ip address 192.168.0.1 255.255.255.128
      description: The subnet mask of Gig0/0 is incorrect
#TShoot_End
```

4. Run the program
<br>
With this yaml file, this tool chooses correct configurations or wrong configurations randomly, then creates troubleshooting lab yaml files.
You can create lab files with the following command:
```bash
# activate the virtual environment
## For Windows
./venv/Scripts/activate
## For Mac or Linux
./venv/bin/activate
# create lab files
python ./src/create_lab.py <source_yaml_file_path> <min_wrongs> <max_wrongs> <number_of_labs> <lab_name_prefix> <destination_directory>
```
- source_yaml_file_path: the path of the file you created in the previous step.
- min_wrongs: the minimum number of wrong configurations you want to include in the output file.
- max_wrongs: the maximum number of wrong configurations you want to include in the output file.
- number_of_labs: the number of lab files you want to create.
- lab_name_prefix: the prefix of the lab file name.
- destination_directory: the destination directory where you want to output the lab files.

After running the program, it outputs files to destination_directory.
```
destination_directory:
| - excercise_1.yaml
| - excercise_2.yaml
    ...
| - excercise_N.yaml
| - init_lab_1.yaml
| - init_lab_2.yaml
    ...
| - init_lab_N.yaml
| - answer.yaml
```
excercise_X.yaml is a CML file; You can create a lab by importing this file on CML.
init_lab_X.yaml is a configuration file; You can view answer by comparing answer.yaml.

5. Import the lab into CML
<br>
Pick up a lab file and import it into CML.

6. Do Excercise!
<br>
Hope you enjoy.

7. View the answer
<br>
You can view answer with the following command.
```bash
# view the answer of lab1
diff -u init_lab_1.yaml answer.yaml
```
