import os
import re
from conllu import parse_incr


def format_manual_marked_corpus(inputs_dir, stage_dir, manual_marked_corpus_file, formatted_marked_corpus_file):
    """
    Remove the redundant spaces in Manual Marked Corpus File and save the results in Formatted Marked Corpus File.

    :param inputs_dir: Inputs Directory.
    :param stage_dir: Stage Directory.
    :param manual_marked_corpus_file: Manual Marked Corpus File.
    :param formatted_marked_corpus_file: Formatted Marked Corpus File.
    """
    with open(os.path.join(inputs_dir, stage_dir, manual_marked_corpus_file), "r", encoding="utf-8") as inputs_file:
        with open(os.path.join(inputs_dir, stage_dir, formatted_marked_corpus_file), "w", encoding="utf-8") as outputs_file:
            for line in inputs_file:
                if line.startswith("#"):
                    continue
                elif line == "\n":
                    outputs_file.write("\n")
                else:
                    tmp_list = re.split("[ \t]", line.strip())
                    for index, item in enumerate(tmp_list):
                        if item == "":
                            continue
                        else:
                            if index == len(tmp_list) - 1:
                                outputs_file.write(item + "\n")
                            else:
                                outputs_file.write(item + "\t")


def transform_marked2unmarked_corpus(inputs_dir, stage_dir, marked_corpus_file, unmarked_corpus_file):
    """
    Transform Marked Corpus File to Unmarked Corpus File.

    :param inputs_dir: Inputs Directory.
    :param stage_dir: Stage Directory.
    :param marked_corpus_file: Marked Corpus File.
    :param unmarked_corpus_file: Unmarked Corpus File.
    """
    with open(os.path.join(inputs_dir, stage_dir, marked_corpus_file), "r", encoding="utf-8") as inputs_file:
        with open(os.path.join(inputs_dir, stage_dir, unmarked_corpus_file), "w", encoding="utf-8") as outputs_file:
            for token_list in parse_incr(inputs_file,
                                         fields=["id", "form", "lemma", "upos", "xpos", "feats", "blank_head", "blank_deprel", "deps", "misc"]):
                for token in token_list:
                    token["blank_head"] = "-"
                    token["blank_deprel"] = "-"
                outputs_file.write(token_list.serialize())
