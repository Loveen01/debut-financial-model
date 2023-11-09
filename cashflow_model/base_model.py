class BaseModel:
    ''''Every model has a timeframe in common, all classes inherit from this'''
    def __init__(self, model_timeframe=24):
        # represents timespan (in months) desired for the model. default = 2 yrs
        self.model_timeframe = model_timeframe 