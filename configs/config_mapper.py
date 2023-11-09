from typing import Dict 

class ConfigMapper:
    '''Takes in raw config dict & maps it to domain specific objects, 
        structured, type-safe way to access parameters'''
    
    def __init__(self, user_parameters_dict):
        self.model_timeframe = user_parameters_dict.get('model_timeframe')

        self.ad_campaigns = {key: AdCampaigns(**value) 
                             for key, value in user_parameters_dict['ad_campaigns'].items()}

        self.freemium_model = {key: FreemiumModel(**value)
                                   for key, value in user_parameters_dict['freemium_model'].items()}
                            
class FreemiumModel:
    def __init__(self, price, proportion, churn_rate): 
        self.price = price
        self.proportion = proportion
        self.churn_rate = churn_rate

class AdCampaigns:
    def __init__(self, **entries):
        self.__dict__.update(entries)
