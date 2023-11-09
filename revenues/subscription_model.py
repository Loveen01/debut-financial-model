import pandas as pd
import numpy as np 
from cashflow_model.base_model import BaseModel

class SubscriptionModel(BaseModel):
    '''''
    SubsciptionModel to calculate revenues from total aquired customers
    :param initial_customers:
    :param new_customers_per_month:
    '''''
    def __init__(self, tier_settings, newly_acquired_customers):
        super().__init__()
        self.tier_settings = tier_settings # tuple representing (percentage_of_customers, price, churn_rate)
        self.newly_acquired_customers = newly_acquired_customers 

        self.no_tiers = len(self.tier_settings)

    def __init_empty_df(self, index_no, row_names = None):
        '''Creates an empty dataframe, filed with zeros'''
        if row_names is None:
            row_names = [f'Row_{i}' for i in range(index_no)]
        # elif len(row_names) != index_no:
        #     raise ValueError("Length of row_names should match index_no")
        df = pd.DataFrame(index = row_names, columns = range(self.model_timeframe))
        return df.fillna(0)

    def __calc_no_tiers(self):
        return len(self.tier_settings) # return length of dict
    
    def __apply_churn_to_tier_acquired_customers(self, tier_level):
        '''apply churn rate to tier-specific acquired customers'''
        
        churn_rate = self.__unwrap_tier_churn_rate(tier_level) # get tier churn rate
        monthly_customers = self.__apply_proportion_to_newly_acquired_customers(tier_level) # get customer for specific tier  

        cumulative_customers_after_churn = self.__init_empty_df(1)
        cumulative_customers_after_churn.iloc[0] = monthly_customers.iloc[0] # assign first item as first item in cumulative 

        for i in range(1,13):
            cumulative_customers_after_churn.iloc[i] = (cumulative_customers_after_churn.iloc[i-1]*churn_rate
                                                          + monthly_customers.iloc[i] )
        return cumulative_customers_after_churn

    def __unwrap_tier_price(self, tier_level): 
        return self.tier_settings[tier_level][0]
    
    def __unwrap_tier_proportion(self, tier_level): 
        return self.tier_settings[tier_level][1]
    
    def __unwrap_tier_churn_rate(self, tier_level): 
        return self.tier_settings[tier_level][2]

    def __apply_proportion_to_newly_acquired_customers(self, tier_level):
        proportion = self.__unwrap_tier_proportion(tier_level)
        return self.newly_acquired_customers * proportion

    def calc_tier_revenue(self, churned_newly_acquired_customers, tier):
        price = self.__unwrap_tier_price(tier)
        monthly_revenue = churned_newly_acquired_customers * price 
        return monthly_revenue

    def calc_total_revenue(self):
        '''Calculates total revenue from all subscription tiers'''
        total_monthly_revenue = self.__init_empty_df(1)
        for tier in range(self.no_tiers): 
            churned_newly_acquired_customers = self.__apply_churn_to_tier_acquired_customers(tier)
            total_monthly_revenue += self.__calc_tier_revenue(churned_newly_acquired_customers)
        return total_monthly_revenue