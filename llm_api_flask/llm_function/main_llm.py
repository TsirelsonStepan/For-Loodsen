import json
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage
import os
from flask import abort
import requests


from dotenv import load_dotenv
load_dotenv()

from llm_function.file_transformer import GetTextFromBinary
from llm_function.models import ResumeDetails

def DeclareLLM():
	llm = ChatDeepSeek(
		model="deepseek-chat",
		temperature=0,
		max_tokens=None,
		max_retries=2,
		api_key=os.getenv("DEEPSEEK_API_KEY")
	)
	return llm.with_structured_output(ResumeDetails, method='json_mode')

def ReadConfigFile() -> dict:
	path_to_config = os.getenv("LLM_CONFIG_PATH")
	with open(path_to_config, 'r', encoding="utf-8") as config_file:
		config : dict = json.load(config_file)
	return config

def GetSchemaFromModel() -> str:
	model = ResumeDetails.model_fields
	string = ""
	for key in model.keys():
		string += key + " - " + model[key].description + ',\n'
	return string

def _Parse(file) -> dict:
	"""Transform file in format of binary string to dict in format of json via llm"""
	file_text = GetTextFromBinary(file)
	llm = DeclareLLM()
	config = ReadConfigFile()
	try:
		system_message = config.get("prompt") + "\nSchema:\n" + GetSchemaFromModel()
	except Exception as e:
		abort(500, f"There was no prompt provided in the config file. {e}")

	messages = [
		SystemMessage(content=system_message),
		HumanMessage(content=file_text)
	]
	
	responce : ResumeDetails = llm.invoke(messages)
	main_service_url = os.getenv("MAIN_SERVICE_URL")
	data = responce.ToJSON()

	main_service_response = requests.post(main_service_url, json=data)
	return main_service_response.json()