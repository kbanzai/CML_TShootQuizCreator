import yaml
import random

class TShootConfig:
    def __init__(self, config):
        self.config = config
        self.yaml_conf = yaml.safe_load(config)
        self.correct = self.yaml_conf['Correct']
        self.wrongs = self.yaml_conf['Wrong'] if type(self.yaml_conf['Wrong']) is list else [self.yaml_conf['Wrong']]

    def get_random_wrong_conf(self):
        return random.choice(self.yaml_conf['Wrong'])


class ConfigLoader:
    def __init__(self, source_file_path):
        self.source_file_path = source_file_path
        self.configs = []
        self._load()

    def get_tshoot_configs(self) -> list[TShootConfig]:
        return [tsc for tsc in self.configs if type(tsc) is TShootConfig]

    def _load(self):
        tshoot_indent = "      "
        with open(self.source_file_path, "r") as source_file:
            tshoot_mode = False
            tshoot_config = ""
            normal_configs = ""
            for line in source_file.readlines():
                trim_line = line.lstrip()
                if trim_line.startswith("#TShoot_Start"):
                    self.configs.append(normal_configs)
                    tshoot_mode = True
                    continue
                if trim_line.startswith("#TShoot_End"):
                    tshoot_mode = False
                    self.configs.append(TShootConfig(tshoot_config))
                    tshoot_config = ""
                    normal_configs = ""
                    continue

                if tshoot_mode:
                    tshoot_config += line.replace(tshoot_indent, "", 1)
                else:
                    normal_configs += line
            self.configs.append(normal_configs)
        with open(self.source_file_path, "r") as source_file:
            a = yaml.safe_load(source_file)
