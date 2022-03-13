# global import
import pandas as pd
import numpy as np
import json
import datetime
import os
import sys
import logging
import re

class Config():
    def __init__(self, config_filepath):
        assert os.path.isfile(config_filepath), 'ERROR: config filepath'
        self.config_filepath = config_filepath
        
        with open(config_filepath, 'r') as f:
            config_dict = json.load(f)
        
        # without a complex pattern checking
        # will update it when everything is solid
        self.stock_list = config_dict['stock_list']
        
        self.train_period = config_dict['train_period']
        self.test_period = config_dict['test_period']
        
        self.use_factor = config_dict['use_factor']
        self.factor_corr_thresh = config_dict['factor_corr_thresh']
        self.trade_strategy = config_dict['trade_strategy']
        self.train_model = config_dict['train_model']
        
        self.logging_home = config_dict['logging_home']
        self.logging_level = config_dict['logging_level']
        
        self.factor_home = config_dict['factor_home']
        self.model_home = config_dict['model_home']
        self.rawdata_home = config_dict['rawdata_home']
    
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
    
    def set_logging(self):
        logging.basicConfig(level=self.logging_level
                    ,filename=os.path.join(self.logging_home, 'log.' + self.get_timestamp())
                    ,filemode="w"
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" 
                    ,datefmt="%Y-%m-%d %H:%M:%S"
                    )
        logging.info(self.config_filepath)
        
    def run(self):
        self.set_logging()
