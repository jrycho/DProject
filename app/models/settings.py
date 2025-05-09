import numpy as np
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    excess_weights: List[float]
    slack_weights: List[float]
    target_goal: List[float]
    optimized_properties: List[str]

    def get_settings(self):
        return  self.target_goal, self.excess_weights, self.slack_weights, self.optimized_properties

    def weights_normalize(target_goal,excess_weights, slack_weights):
        excess_weights = np.divide(excess_weights,target_goal)
        slack_weights = np.divide(slack_weights,target_goal)   
        return excess_weights, slack_weights

    def set_excess_weights(self, new_excess_weights:list):
        self.excess_weights = new_excess_weights

    def set_slack_weights(self, new_slack_weights:list):
        self.slack_weights = new_slack_weights

    def set_target_goal(self, new_target_goal:list):
        self.target_goal = new_target_goal

    def set_optimized_properties(self, new_optimized_properties:list):
        self.optimized_properties = new_optimized_properties

    def get_excess_weights(self):
        excess_weights_normalized= np.divide(self.excess_weights,self.target_goal)
        return excess_weights_normalized

    def get_slack_weights(self):
        slack_weights_normalized = np.divide(self.slack_weights,self.target_goal)
        return slack_weights_normalized

    def get_target_goal(self):
        return self.target_goal
    
    def get_optimized_properties(self):
        return self.optimized_properties
    
    
    def __str__(self):
        return f"Excess weights: {self.excess_weights}, Slack weights: {self.slack_weights}, Target goal: {self.target_goal}, Optimized properties: {self.optimized_properties}"


class SettingsInput(BaseModel):
    optimized_properties: List[str]
    excess_weights: List[int]
    slack_weights: List[int]
    target_goal: List[float]