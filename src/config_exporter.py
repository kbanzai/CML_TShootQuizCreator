from config_loader import ConfigLoader, TShootConfig
from config_picker import ConfigChoicesSet
from script_options import ScriptOptions
import os
import yaml

class ConfigExporter:
    def __init__(self, config_loader : ConfigLoader, choices_set : ConfigChoicesSet, index : int, script_options : ScriptOptions):
        self.config_loader = config_loader
        self.choices_set = choices_set
        self.index = index
        self.script_options = script_options

    @property
    def lab_path(self):
        return self.script_options.destination_directory + "/excercise_%s.yaml" % self.index

    @property
    def init_lab_path(self):
        return self.script_options.destination_directory + "/init_lab_%s.yaml" % self.index

    def output_yaml(self):
        tmp_content = ""
        tshoot_indent = "      "
        for conf in self.config_loader.configs:
            if type(conf) is TShootConfig:
                config_choice = self.choices_set.get_config(conf)
                yaml_conf = config_choice.get_config()
                tmp_content += tshoot_indent + yaml_conf + "\n"
            else:
                tmp_content += conf

        lab_yaml = yaml.safe_load(tmp_content)
        lab_yaml['lab']['title'] = self.script_options.lab_name_prefix + '_' + str(self.index)
        with open(self.lab_path, 'w') as f:
            yaml.dump(lab_yaml, f)

        with open(self.init_lab_path, "w") as f:
            for node in lab_yaml['nodes']:
                f.write(node['configuration'] + '\n')

class AnswerExporter:
    def __init__(self, config_loader : ConfigLoader, script_options : ScriptOptions):
        self.config_loader = config_loader
        self.script_options = script_options

    @property
    def answer_path(self):
        return self.script_options.destination_directory + "/answer.yaml"

    def output_yaml(self):
        answer_conf = ""
        tshoot_indent = "      "
        for conf in self.config_loader.configs:
            if type(conf) is TShootConfig:
                answer_conf += tshoot_indent + conf.correct + "\n"
            else:
                answer_conf += conf

        answer_yaml = yaml.safe_load(answer_conf)
        with open(self.answer_path, 'w') as f:
            for node in answer_yaml['nodes']:
                f.write(node['configuration'] + '\n')

