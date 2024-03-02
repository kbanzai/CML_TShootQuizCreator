class ScriptOptions:
    def __init__(
        self,
        source_file_path,
        min_wrongs,
        max_wrongs,
        num_of_labs,
        lab_name_prefix,
        destination_directory
    ):
        self.source_file_path = source_file_path
        self.min_wrongs = min_wrongs
        self.max_wrongs = max_wrongs
        self.num_of_labs = num_of_labs
        self.lab_name_prefix = lab_name_prefix
        self.destination_directory = destination_directory
