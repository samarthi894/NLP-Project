import json
import requests
import csv
import argparse
import os
import pdb

def open_file(file_name):
  file = open(file_name, "r")
  data = json.load(file)
  file.close()

  return data

def get_answers_GPT3(url, headers, data):
  responses = []
  for i in data:
    payload = {
      "prompt": "Given some context, answer the question.\nContext: "+ i["context"] + "Question: " + i["question"] + "Answer:",
      "max_tokens": 10,
      "temperature": 1
    }


    file = open("payload.json", "w")
    json.dump(payload, file)
    file.close()
    payload = open("payload.json")
    r = requests.post(url, data=payload, headers=headers)
    responses.append(r.json()['choices'][0]['text'])
  return responses

def get_answers_T0pp(url, headers, data):
  responses = []
  for i in data:
    prompt = "Question: " + i["question"] + "Answer based on following passage.\n\n" + i["context"]
    payload = {"inputs": prompt, "options": {"use-gpu":True}}
   ## pdb.set_trace()
    response = requests.post(url, headers=headers, data=payload)
   ## print(response.text)
   ## pdb.set_trace()
    responses.append(response.json()[0]['generated_text'])
    
  return responses
  
def compare_answers(decomp_file, decomp_answers, undecomp_file, undecomp_answers, output_file_name):
  data = open_file(undecomp_file)
  data_decomp = open_file(decomp_file)
  file = open(output_file_name, "w")
  for i in range(len(data)):
    string = ""
    string += "Context: " + data[i]["context"] + "\nQuestion: " + data[i]["question"] + "True Answer: " + data[i]["answer"] + "\nGenerated Answer: " + undecomp_answers[i] + "\n\n"
    for j in range(len(data_decomp)):
      if data_decomp[j]["id"] == data[i]["id"]:
        string += "Decomposed Question: " + data_decomp[j]["question"] + "True Answer: " + data_decomp[j]["answer"] + "\nGenerated Answer: " + decomp_answers[j] + "\n\n"
    file.write(string)
  file.close()

def generate_answers(dataset_name, model_name, API_TOKEN):
    decomp_file = dataset_name + "_" +  "decomp.json"
    undecomp_file = dataset_name + "_" + "undecomp.json"
    
    data_decomp = open_file(decomp_file)
    data_undecomp = open_file(undecomp_file)
    
    if model_name == "GPT3":
        
        url_GPT3 = "https://api.openai.com/v1/engines/davinci-instruct-beta/completions"
        headers_GPT3 = {'content-type': 'application/json', 'authorization': 'Bearer {0}'.format(API_TOKEN)}
        
        responses_undecomp_GPT3 = get_answers_GPT3(url_GPT3, headers_GPT3, data_undecomp)
        responses_decomp_GPT3 = get_answers_GPT3(url_GPT3, headers_GPT3, data_decomp)
        
        compare_answers(decomp_file, responses_decomp_GPT3, undecomp_file, responses_undecomp_GPT3, dataset_name + "_GPT3_trial.txt")
    
    if model_name == "T0pp":
        
        url_T0pp = "https://api-inference.huggingface.co/models/bigscience/T0pp"
        headers_T0pp = {'Content-type': 'application/json; charset=utf-8', 'Authorization': 'Bearer {0}'.format(API_TOKEN)}

        responses_decomp_T0pp = get_answers_T0pp(url_T0pp, headers_T0pp, data_decomp)
        responses_undecomp_T0pp = get_answers_T0pp(url_T0pp, headers_T0pp, data_undecomp)
        
        compare_answers(decomp_file, responses_decomp_T0pp, undecomp_file, responses_undecomp_T0pp, dataset_name + "_T0pp_trial.txt")

def gold_and_predictions(dataset_name, model_name):
    
    file_name = dataset_name + "_" + model_name + "_trial.txt"
    file = open(file_name, "r")
    
    true_answers_decomp = ""
    generated_answers_decomp = []
    
    true_answers_undecomp = ""
    generated_answers_undecomp = []
    
    lines = file.readlines()
    for i in range(len(lines)):
        if lines[i][:10] =="Decomposed":
            s = str(lines[i+1][13:-1]).strip()
            true_answers_decomp += s + "\n"

            s = str(lines[i+2][18:-1]).strip()
            generated_answers_decomp.append(s)
            
        if lines[i][:8] == "Question":
            s = str(lines[i+1][13:-1]).strip()
            true_answers_undecomp += s + "\n"

            s = str(lines[i+2][18:-1]).strip()
            generated_answers_undecomp.append(s)
    
    decomp_true_file = open(dataset_name + "_" + model_name +"_decomp_true_answers.txt", "w")        
    decomp_true_file.write(true_answers_decomp[:-2])
    decomp_true_file.close()
    
    undecomp_true_file = open(dataset_name + "_" + model_name +"_undecomp_true_answers.txt", "w")        
    undecomp_true_file.write(true_answers_undecomp[:-2])
    undecomp_true_file.close()
    
    predictions = {"predictions": generated_answers_decomp}
    predictions_file = open(dataset_name + "_" + model_name + "_decomp_predictions.json","w")
    json.dump(predictions, predictions_file)
    predictions_file.close()
    
    predictions = {"predictions": generated_answers_undecomp}
    predictions_file = open(dataset_name + "_" + model_name + "_undecomp_predictions.json","w")
    json.dump(predictions, predictions_file)
    
    predictions_file.close()
    file.close()
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluation of Question Decomposition')
    parser.add_argument('--model_name', help='model to be used')
    parser.add_argument('--dataset_name',help='dataset to be used')
    parser.add_argument('--API_TOKEN',help='API token for the model to be used')
    args = parser.parse_args()
    file_name = args.dataset_name + "_" + args.model_name + "_trial.txt"
    
    if os.path.isfile(file_name):
        gold_and_predictions(args.dataset_name, args.model_name)
    else:
        generate_answers(args.dataset_name, args.model_name, args.API_TOKEN)
        gold_and_predictions(args.dataset_name, args.model_name)
    
        
