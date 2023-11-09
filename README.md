# debut-financial-model
Financial P&amp;L Model using Pandas

To use, update the user_parameters.yaml file to set the desired parameters. 
They are described here below: 

Revenues: 
Revenue obtained from pricing model (subscription based)

Costs: 
Cost of creating, maintaining the platform, and hosting it 
Salaries for small team of developers

model_timeframe: 36

ad_campaigns:
  facebook: 
    ad_viewers: 600
    viewership_change_rate: 0.1  # rate of decay of ad-viewers monthly
    click_rate: 0.2          # rate of viewers clicking ad
    base_conv_rate: 0.3          # month 1 conversion rate (this may be constant for all rates, if conv_decay = 1)
    conv_decay: 0.2           # rate at which conversion rate will decrease monthly. base_conv_rate * conv_rate^month 
    advert_timeframe: 21        # period of time to keep advert for
    word_of_mouth_coeff: 0.9     # 1 means we have the same wom customers as last months newcomers (very optimistic)
   
  add any other add campaign here, e.g. 
  instagram:
    viewership_change_rate: etc ...

freemium_model:
  tier_1 : 
    price: 0
    proportion: 0.8  # proportions of the 3 tiers should sum to 1 
    churn_rate: 0.2
  tier_2 : 
    price: 5
    proportion: 0.2
    churn_rate: 0.2