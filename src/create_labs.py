import yaml
import sys
from script_options import ScriptOptions
from config_picker import ConfigPicker
from config_exporter import ConfigExporter, AnswerExporter
import os

if len(sys.argv) != 7:
    print("usage: {script_path} <source_yaml_file_path> <min_wrongs> <max_wrongs> <number_of_labs> <lab_name_prefix> <destination_directory>".format(script_path = sys.argv[0]))
    exit(1)

source_file_path = sys.argv[1]
min_wrongs = int(sys.argv[2])
max_wrongs = int(sys.argv[3])
num_of_labs = int(sys.argv[4])
lab_name_prefix = sys.argv[5]
destination_directory = sys.argv[6]

script_options = ScriptOptions(source_file_path, min_wrongs, max_wrongs, num_of_labs, lab_name_prefix, destination_directory)
os.makedirs(script_options.destination_directory, exist_ok=True)
config_picker = ConfigPicker(script_options)

for choice_set in config_picker.choices_set_list:
    index = 0
    for choices_set in config_picker.choices_set_list:
        config_exporter = ConfigExporter(config_picker.config_loader, config_picker.choices_set_list[index], index+1, script_options)
        config_exporter.output_yaml()
        index += 1

answer_exporter = AnswerExporter(config_picker.config_loader, script_options)
answer_exporter.output_yaml()
