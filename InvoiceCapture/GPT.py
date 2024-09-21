# -*- coding: utf-8 -*-

import tkinter as tk
import os
import openai


class GPT:
    #openai.organization = "org-BAZpYC"
    #openai.api_key = "sk-K8d0wrwKFwcjshVdPHbDA31sSw"
    
  


    def __init__(self):
        print('from init')
        
    
    def chatgpt_conversastion(self, conversastion_log):
        openai.organization = "org-kcrnQFx2uHaRouXD"
        openai.api_key = "sk-80xfwZw6nxWuwP3s99ycT3BlbdyEIYFK2" 
        gpt_model = "gpt-3.5-turbo"
    
        response = openai.ChatCompletion.create(
                model = gpt_model,
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": conversastion_log},
              ]
            )
        print(response)
        return response['choices'][0]['message']['content']

    
