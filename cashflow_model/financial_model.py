import yaml
import os 
import pandas as pd
import numpy as np 
from cashflow_model.base_model import BaseModel

class FinancialModel(BaseModel):
    '''''
    Takes total_customers_aquired and costs, to calculate some key metrics over time

    def calculate_revenues()
    def calculate_costs()
    def calculate_profits()
    '''''
    def __init__(self, total_customers_acquired, ad_revenue):
        super().__init__()
        self.total_customers_acquired = total_customers_acquired
        self.ad_revenue = ad_revenue

    def set_model_timeframe(self, model_timeframe):
        self.model_timeframe = model_timeframe

    def calculate_COGS():
        pass 
        
    def calculate_gross():
        pass

    def calculate_employee_costs():
        pass
    
    def calculate_EBITDA():
        pass

    def calculate_cooporate_tax():
        pass
    
    def calculate_profit():
        pass 
