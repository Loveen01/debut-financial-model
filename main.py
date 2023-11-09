import yaml 
import pandas as pd 
from configs.load_configs import ConfigLoader
from configs.config_mapper import ConfigMapper

from cashflow_model.financial_model import FinancialModel
from marketing_model.ad_campaign import AdCampaign
from revenues.subscription_model import SubscriptionModel


if __name__ == "__main__":
    print("Ensure you have updated user_parameters.py")
    print("------------------------------------------")
    print("Profit & Loss Model Generator")

    # load user configs
    raw_config = ConfigLoader().load_configs('user_parameters.yaml')
    configs = ConfigMapper(raw_config)

    # access ad_campaign configs
    facebook_configs = configs.ad_campaigns['facebook']

    facebook_campaign = AdCampaign(
        ad_viewers = facebook_configs.ad_viewers,
        click_rate = facebook_configs.click_rate,
        viewership_change_rate = facebook_configs.viewership_change_rate,
        base_conv_rate = facebook_configs.base_conv_rate,
        advert_timeframe = facebook_configs.advert_timeframe,
        conv_decay = facebook_configs.conv_decay,
        word_of_mouth_coeff = facebook_configs.word_of_mouth_coeff)

    # get customers acquired from facebook ad campaign over time 
    newly_acquired_facebook_customers = facebook_campaign.calc_customers_acquired_df() 

    # obtain user parameters for premium model
    tier_one_settings = configs.freemium_model['tier_1']
    tier_two_settings = configs.freemium_model['tier_1']

    two_tier_model_configs = ((tier_one_settings.price, tier_one_settings.proportion), 
                              (tier_two_settings.price, tier_two_settings.proportion))

    # initialise subscription model with parameters
    tiered_access_model = SubscriptionModel(
        tier_settings = two_tier_model_configs,
        newly_acquired_customers = newly_acquired_facebook_customers
        )
    
    # calculate total revenue
    tiered_access_revenue = tiered_access_model.calc_total_revenue()

    # initialise financial model with previous data
    financial_model = FinancialModel(
        tiered_access_revenue)

