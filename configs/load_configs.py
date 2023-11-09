import yaml 

class ConfigLoader:
    '''Reads a YAML file and converts it to dictionary'''
    
    def __init__(self):
        pass
    
    def load_configs(self, file): # 'simulation/user_parameters.yaml'
        with open(file, "r") as stream:
            try:
                config_dict = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        return config_dict