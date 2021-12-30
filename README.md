
# Question Decomposition and Answering for SVAMP and MultiRC

 For each dataset, there are two files: 
 
 1) {dataset_name}_undecomp.json which contains id, context, question and answer sets for original, undecomposed questions
 
 2) {datset_name}_decomp.json which contains id, context, question and answer sets for decomposed questions

 # Here is an example of how each file looks:

 ### {dataset_name}_undecomp.json:

 {

     "id": "1",
    "context": "ABC DEF...\n",
    "question": "PQR STU?\n",
    "answer": "QWE."
 }

### {dataset_name}_decomp.json:
{

    "id": "1",
    "context": "ABC DEF..\n",
    "question": "PQR?\n",
    "answer": "Q."
}

{

    "id": "1",
    "context": "ABC DEF..\n",
    "question": "STU?\n",
    "answer": "WE."
}

NOTE: Context and question should end with \n. For each id in {dataset_name}_undecomp.json, the id should be same for the decomposed versions of the original question in the {dataset_name}_decomp.json file

## decomposition_answers.py --by pruthvi

The script takes three arguments as its input:

1) --dataset_name 
2) --model_name (Currently takes "GPT3" or "T0pp" as its value)
3) --API_TOKEN (Optional: to enable making changes in the script without having to always predict something, e.g. the output file format with the already generated answers)

Usage example: python decomposition_answers.py --dataset_name "hotpot" --model_name "T0pp" --API_TOKEN {API_TOKEN}

This script generates the following output files in the current directory:

1) {dataset_name}_{model_name}_trial.txt <br >
   looks something like this: <br >
   ![Alt text](images/trial_image.jpg?raw=true "Title") <br >

2) {dataset_name}_{model_name}_undecomp_true_answers.txt
    <br > <br >
   This is a text file with each line containing the true answer for each undecomposed question present in the {dataset_name}\_{model_name}_undecomp.json file <br > <br >
3) {dataset_name}_{model_name}_undecomp_predictions.json
<br > <br >
   This is a json file which looks like this: <br > 
   {
    "predictions" : ["prediction1", "prediction2"...]
   }
   <br > <br >
4) {dataset_name}_{model_name}_decomp_true_answers.txt
<br > <br >
   This is a text file with each line containing the true answer for each decomposed question present in the {dataset_name}\_{model_name}_decomp.json file <br > <br >
5) {dataset_name}_{model_name}_decomp_predictions.json
<br > <br >
   This is a json file which looks like this: <br > 
   {
    "predictions" : ["prediction1", "prediction2"...]
   }
   <br > <br >

## evaluate.py

**Before running this file, you need to run install_dependencies.py to install required libraries**

This script takes two arguments: <br >
1) --dataset_file, which is {dataset_name}_{model_name}_decomp_true_answers.txt for example <br >
2) --prediction_file, which is {dataset_name}_{model_name}_decomp_predictions.json for example

This file prints 5 metrics to the console in the following way:  <br >
{"sacrebleu": 0.0, "bleurt": 0.4123998790979385, "rouge": 0.5, "f1": 0.5, "exact_match": 0.5}

Note: You can directly run my SVAMP_MultiRC_Scores.ipynb file I uploaded to get the scores.

Results:

For GPT3 model:


![image](https://user-images.githubusercontent.com/90678416/144792981-60f2e524-3bda-4b42-a6b3-420f1ef1282b.png)

For T0pp model:


![image](https://user-images.githubusercontent.com/90678416/144921951-21ec6f1b-9e9b-4015-8727-c84dbcaf365e.png)


I used the below given prompts for GPT3:

For SVAMP dataset:
Prompt: Given some context, answer the question.
Context: ABC PQR
Question: EFG
Answer: {Generated Answer}
Temperature: 1
Max length tokens: 10

For MultiRC datset:
Prompt: Answer the below questions based on the context.
Context: ABC PQR
Question: EFG
Answer: {Generated Answer}
Temperature: 1
Max length: 10-15 ( I have manually found the answers using GPT3 playground for MultiRC as answer length varies based on the question. I manually adjusted answer length based on the question.)


Prompt used for T0pp for both SVAMP and MultiRC datasets:

Question: EFG
Answer based on the following passage.
{passage/context}



Results Analysis:
GPT3:
Based on the results, for SVAMP dataset,which contains simple math word problem descriptions as the context, the prediction accuracy of GPT3 for decomposed questions was impressive compared to undecomposed questions. When it comes to MultiRC dataset which contains Reading Comprehension passage as a context, there is a slight improvement in the accuracy for decomposed questions compared to undecomposed questions using GPT3.

T0pp:
There is huge improvement in the scores for decomposed question in SVAMP dataset compared to undecomposed questions while tested using T0pp model. But when it comes to MultiRC there is not much difference observed in scores between decomposed and undecomposed questions.


Conclusion:
Based on my analysis, the question decomposition is a good technique to employ for certain set of datasets where its difficult for the model to comprehend a complex question and context. But GPT3 is fairly doing good on certain datasets without even decomposing the questions. So, I believe it depends on the context and complexity of the question whether a question decomposition works better or not. The more complex the question and the context, the more improvement you can see with decomposed questions.



