from config_loader import TShootConfig, ConfigLoader
from script_options import ScriptOptions
import random

class ConfigChoice:
    def __init__(self, tshoot_config: TShootConfig, selected_index: int):
        self.tshoot_config = tshoot_config
        self.selected_index = selected_index

    def __eq__(self, other):
        if type(other) is ConfigChoice:
            return self.tshoot_config == other.tshoot_config and self.selected_index == other.selected_index
        else:
            return False

    def __hash__(self):
        return hash(self.selected_index) + hash(self.tshoot_config)

    def get_config(self) -> dict:
        if self.selected_index == 0:
            return self.tshoot_config.correct
        else:
            return self.tshoot_config.wrongs[self.selected_index - 1]

class ConfigChoicesSet:
    def __init__(self, config_choices: list[ConfigChoice]):
        self.config_choices = set(config_choices)

    def __eq__(self, other):
        if type(other) is ConfigChoicesSet:
            return self.config_choices == other.config_choices
        else:
            return False

    def get_config(self, tshoot_config: TShootConfig) -> ConfigChoice:
        for config_choice in list(self.config_choices):
            if config_choice.tshoot_config == tshoot_config:
                return config_choice

class ConfigPicker:
    def __init__(self, script_options: ScriptOptions):
        self.script_options = script_options
        self.config_loader = ConfigLoader(script_options.source_file_path)
        self.choices_set_list : list[ConfigChoicesSet] = self.create_choices()

    def create_choices(self) -> list[ConfigChoicesSet]:
        tshoot_configs = self.config_loader.get_tshoot_configs()
        fail_count = 0
        MAX_FAIL = 100
        choices_set_list : list[ConfigChoicesSet] = []
        while len(choices_set_list) < self.script_options.num_of_labs:
            if fail_count >= MAX_FAIL:
                raise Exception("failed to create {num_of_labs} labs".format(num_of_labs = self.script_options.num_of_labs))
            num_of_wrongs = random.randint(self.script_options.min_wrongs, self.script_options.max_wrongs)
            wrong_configs = self._pick_tshoot_configs(tshoot_configs, num_of_wrongs)
            config_choices_set = self._create_config_choices_set(tshoot_configs, wrong_configs)

            if config_choices_set in choices_set_list:
                fail_count += 1
                continue
            choices_set_list.append(config_choices_set)
        return choices_set_list


    def _pick_tshoot_configs(self, tshoot_configs: list[TShootConfig], num_of_wrongs: int) -> list[TShootConfig]:
        if len(tshoot_configs) <= num_of_wrongs:
            print(len(tshoot_configs), num_of_wrongs)
            raise Exception("cannot add {num_of_wrongs} wrongs".format(num_of_wrongs))
        random.shuffle(tshoot_configs)
        wrong_configs = tshoot_configs[:num_of_wrongs]
        return wrong_configs

    def _create_config_choice(self, tshoot_config: TShootConfig, is_correct: bool) -> ConfigChoice:
        selected_index = 0 if is_correct else random.randint(1, len(tshoot_config.wrongs))
        return ConfigChoice(tshoot_config, selected_index)

    def _create_config_choices_set(self, tshoot_configs, wrong_configs):
        config_choices : list[ConfigChoice] = []
        for tsc in tshoot_configs:
            config_choices.append(self._create_config_choice(tsc, tsc not in wrong_configs))
        return ConfigChoicesSet(config_choices)
