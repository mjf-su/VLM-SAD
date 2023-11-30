import os
import json
import numpy as np

folder = os.path.dirname(__file__)
scenarios = ["nominal_stop_sign", "nominal_traffic_light"] # scenarios represented in the dataset
response_file = "vlm_responses.npz"
dataset_file = "VQADataset.npz"

questions = []
answers = []
filenames = []

for scenario in scenarios:
    scenario_folder = os.path.join(folder, "data", scenario) # scenario type

    with open(os.path.join(scenario_folder, "incorrect_labels.json"), 'r') as js:
        incorrect_labels = json.load(js)
    for exp in os.listdir(scenario_folder):
        if "exp" not in exp:
            continue

        exp_folder = os.path.join(scenario_folder, exp) # specific experiment
        exp_responses = np.load(os.path.join(exp_folder, response_file))

        for i, image in enumerate(exp_responses["image_names"]):
            if image in incorrect_labels[exp]:
                continue # skip errenous response

            questions.append(exp_responses["vlm_prompt"])
            answers.append(exp_responses["vlm_responses"][i])
            filenames.append(exp_responses["image_names"][i])
    
    np.savez(os.path.join(scenario_folder, dataset_file), questions = questions, answers = answers, filenames = filenames)




