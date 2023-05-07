import os
from conllu import parse_incr


def calculate_uas(inputs_dir, outputs_dir, stage_dir, ground_truths_file, experiment_results_file):
    """
    Calculate UAS.

    :param inputs_dir: Inputs Directory.
    :param outputs_dir: Outputs Directory.
    :param stage_dir: Stage Directory.
    :param ground_truths_file: Ground Truths File.
    :param experiment_results_file: Experiment Truth File.
    :return: UAS.
    """
    total_num = 0
    correct_num = 0
    with open(os.path.join(inputs_dir, stage_dir, ground_truths_file), "r", encoding="utf-8") as ground_truths_file:
        with open(os.path.join(outputs_dir, stage_dir, experiment_results_file), "r", encoding="utf-8") as experiment_results_file:
            ground_truth_conllu_list = []
            experiment_result_conllu_list = []
            for ground_truth_token_list in parse_incr(ground_truths_file,
                                                      fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel", "deps",
                                                              "misc"]):
                ground_truth_conllu_list.append(ground_truth_token_list)
            for experiment_result_token_list in parse_incr(experiment_results_file,
                                                           fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel",
                                                                   "deps", "misc"]):
                experiment_result_conllu_list.append(experiment_result_token_list)
            for token_list_index, ground_truth_token_list in enumerate(ground_truth_conllu_list):
                for token_index, ground_truth_token in enumerate(ground_truth_token_list):
                    total_num += 1
                    if ground_truth_token["blank_head"] == experiment_result_conllu_list[token_list_index][token_index]["blank_head"]:
                        correct_num += 1
    return correct_num / total_num


def calculate_las(inputs_dir, outputs_dir, stage_dir, ground_truths_file, experiment_results_file):
    """
    Calculate LAS.

    :param inputs_dir: Inputs Directory.
    :param outputs_dir: Outputs Directory.
    :param stage_dir: Stage Directory.
    :param ground_truths_file: Ground Truths File.
    :param experiment_results_file: Experiment Truth File.
    :return: LAS.
    """
    total_num = 0
    correct_num = 0
    with open(os.path.join(inputs_dir, stage_dir, ground_truths_file), "r", encoding="utf-8") as ground_truths_file:
        with open(os.path.join(outputs_dir, stage_dir, experiment_results_file), "r", encoding="utf-8") as experiment_results_file:
            ground_truth_conllu_list = []
            experiment_result_conllu_list = []
            for ground_truth_token_list in parse_incr(ground_truths_file,
                                                      fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel", "deps",
                                                              "misc"]):
                ground_truth_conllu_list.append(ground_truth_token_list)
            for experiment_result_token_list in parse_incr(experiment_results_file,
                                                           fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel",
                                                                   "deps", "misc"]):
                experiment_result_conllu_list.append(experiment_result_token_list)
            for token_list_index, ground_truth_token_list in enumerate(ground_truth_conllu_list):
                for token_index, ground_truth_token in enumerate(ground_truth_token_list):
                    total_num += 1
                    if ground_truth_token["blank_head"] == experiment_result_conllu_list[token_list_index][token_index]["blank_head"] and \
                            ground_truth_token["blank_deprel"] == experiment_result_conllu_list[token_list_index][token_index]["blank_deprel"]:
                        correct_num += 1
    return correct_num / total_num
