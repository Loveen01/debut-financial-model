class BaseModel:
    ''''All models share a common timeframe, so all classes inherit this'''
    def __init__(self, model_timeframe=24):
        # represents timespan (in months) desired for the model. default = 2 yrs
        self.model_timeframe = model_timeframe 