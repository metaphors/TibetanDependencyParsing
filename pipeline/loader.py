import os
import re
from conllu import parse_incr


def load_conjunctions(assists_dir, stage_dir, coordinating_conjunctions_file, adversative_conjunctions_file, causal_conjunctions_file):
    """
    Load Conjunctions.

    :param assists_dir: Assists Directory.
    :param stage_dir: Stage Directory.
    :param coordinating_conjunctions_file: Coordinating Conjunctions File.
    :param adversative_conjunctions_file: Adversative Conjunctions File.
    :param causal_conjunctions_file: Causal Conjunctions File.
    :return: Conjunction List.
    [{'type': 'coordinating', 'list': [conjunction...]}, {'type': 'adversative', 'list': [conjunction...]}, {'type': 'causal', 'list': [conjunction...]}]
    """
    conjunction_list = []
    with open(os.path.join(assists_dir, stage_dir, coordinating_conjunctions_file), "r", encoding="utf-8") as coordinating_conjunctions_file:
        line = coordinating_conjunctions_file.readline()
        coordinating_conjunction_list = re.split(" ", line)
        conjunction_list.append({"type": "coordinating", "list": coordinating_conjunction_list})
    with open(os.path.join(assists_dir, stage_dir, adversative_conjunctions_file), "r", encoding="utf-8") as adversative_conjunctions_file:
        line = adversative_conjunctions_file.readline()
        adversative_conjunction_list = re.split(" ", line)
        conjunction_list.append({"type": "adversative", "list": adversative_conjunction_list})
    with open(os.path.join(assists_dir, stage_dir, causal_conjunctions_file), "r", encoding="utf-8") as causal_conjunctions_file:
        line = causal_conjunctions_file.readline()
        causal_conjunction_list = re.split(" ", line)
        conjunction_list.append({"type": "causal", "list": causal_conjunction_list})
    return conjunction_list


def load_function_words(assists_dir, stage_dir, function_words_file):
    """
    Load Function Words.

    :param assists_dir: Assists Directory.
    :param stage_dir: Stage Directory.
    :param function_words_file: Function Words File.
    :return: Function Word List.
    [function_word...]
    """
    with open(os.path.join(assists_dir, stage_dir, function_words_file), "r", encoding="utf-8") as function_words_file:
        line = function_words_file.readline()
        function_word_list = re.split(" ", line)
    return function_word_list


def load_function_words_pos(assists_dir, stage_dir, function_words_pos_file):
    """
    Load Function Words POS.

    :param assists_dir: Assists Directory.
    :param stage_dir: Stage Directory.
    :param function_words_pos_file: Function Words POS File.
    :return: Function Word POS List.
    [function_word_pos...]
    """
    with open(os.path.join(assists_dir, stage_dir, function_words_pos_file), "r", encoding="utf-8") as function_words_pos_file:
        line = function_words_pos_file.readline()
        function_word_pos_list = re.split(" ", line)
    return function_word_pos_list


def load_nouns_pos(assists_dir, stage_dir, nouns_pos_file):
    """
    Load Nouns POS.

    :param assists_dir: Assists Directory.
    :param stage_dir: Stage Directory.
    :param nouns_pos_file: Nouns POS File.
    :return: Noun POS List.
    [noun_pos...]
    """
    with open(os.path.join(assists_dir, stage_dir, nouns_pos_file), "r", encoding="utf-8") as nouns_pos_file:
        line = nouns_pos_file.readline()
        noun_pos_list = re.split(" ", line)
    return noun_pos_list


def load_chunking_rules(rules_dir, stage_dir, chunking_rules_file):
    """
    Load Chunking Rules.

    :param rules_dir: Rules Directory.
    :param stage_dir: Stage Directory.
    :param chunking_rules_file: Chunking Rules File.
    :return: Chunking Rule List.
    [{'type': type, 'components': [component...]}, ...]
    """
    chunking_rule_list = []
    with open(os.path.join(rules_dir, stage_dir, chunking_rules_file), "r", encoding="utf-8") as chunking_rules_file:
        for line in chunking_rules_file:
            tmp_list = re.split("[=+]", line.strip())
            chunking_rule = {"type": tmp_list[0], "components": tmp_list[1:]}
            chunking_rule_list.append(chunking_rule)
    return chunking_rule_list


def load_dependency_rules(rules_dir, stage_dir, dependency_rules_file):
    """
    Load Dependency Rules.

    :param rules_dir: Rules Directory.
    :param stage_dir: Stage Directory.
    :param dependency_rules_file: Dependency Rules File.
    :return: Dependency Rule List.
    [{'components': [component...], 'relation': relation, 'direction': direction}, ...]
    """
    dependency_rule_list = []
    with open(os.path.join(rules_dir, stage_dir, dependency_rules_file), "r", encoding="utf-8") as dependency_rules_file:
        for line in dependency_rules_file:
            tmp_list = re.split(":", line.strip())
            dependency_rule = {"components": re.split("[+]", tmp_list[0]),
                               "relation": re.split(",", tmp_list[1][1:-1])[0], "direction": re.split(",", tmp_list[1][1:-1])[1]}
            dependency_rule_list.append(dependency_rule)
    return dependency_rule_list


def load_conllu_data(inputs_dir, stage_dir, inputs_file):
    """
    Load CoNLL-U Data.

    :param inputs_dir: Inputs Directory.
    :param stage_dir: Stage Directory.
    :param inputs_file: Inputs File.
    :return: CoNLL-U List.
    [TokenList...]
    """
    conllu_list = []
    with open(os.path.join(inputs_dir, stage_dir, inputs_file), "r", encoding="utf-8") as inputs_file:
        for token_list in parse_incr(inputs_file,
                                     fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel", "deps", "misc"]):
            for token in token_list:
                if re.match("^v", token["xpos"]):
                    token["upos"] = "vx"
                if re.match("^u", token["xpos"]):
                    token["upos"] = "ux"
                if re.match("^r", token["xpos"]):
                    token["upos"] = "rx"
                if re.match("^n", token["xpos"]):
                    token["upos"] = "nx"
                if re.match("^a", token["xpos"]):
                    token["upos"] = "ax"
            conllu_list.append(token_list)
    return conllu_list
