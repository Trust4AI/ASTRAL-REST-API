# -*- coding: utf-8 -*-

from TestExecutor.testExecutor import TestExecutor

from openai import OpenAI 
import openai

class TestExecutorO3(TestExecutor):
    
    def __init__(self, model, token, role = "user"):
        
        super().__init__(model, role)
        
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'GPT_token' must be a string")       
        
    def updateToken(self, token):
        if isinstance(token, str):
            self.client = OpenAI(
               api_key = token
               )
            self.token = token
        else: 
            raise TypeError("Attribute 'GPT_token' must be a string")

        
    def executeTestcase(self, testcase):
        try:
            response = self.client.responses.create(model = self.model, input = testcase)
        
        except openai.BadRequestError as e:
            error_message = str(e)
            print("LLM couldn't provide an answer due to a policy violation in the prompt")
            return "policy violation"
        
        except ValueError:
            print("Problem when executing GPT LLM")
            return "value error"
        
        except:
            return "error"
        
        return response.output_text
    
