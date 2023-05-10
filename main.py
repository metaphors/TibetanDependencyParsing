# configuration begin

# stage: dev or test
STAGE_DIR = "test"

# inputs
INPUTS_DIR = "inputs"
INPUTS_FILE = "corpus.conllu"
FORMATTED_MARKED_CORPUS_FILE = "formatted_marked_corpus.conllu"
MANUAL_MARKED_CORPUS_FILE = "manual_marked_corpus.conllu"

# outputs
OUTPUTS_DIR = "outputs"
OUTPUTS_FILE = "results.conllu"

# assists
ASSISTS_DIR = "assists"
COORDINATING_CONJUNCTIONS_FILE = "coordinating_conjunctions.txt"
ADVERSATIVE_CONJUNCTIONS_FILE = "adversative_conjunctions.txt"
CAUSAL_CONJUNCTIONS_FILE = "causal_conjunctions.txt"
FUNCTION_WORDS_FILE = "function_words.txt"
FUNCTION_WORDS_POS_FILE = "function_words_pos.txt"
NOUNS_POS_FILE = "nouns_pos.txt"

# rules
RULES_DIR = "rules"
CHUNKING_RULES_FILE = "chunking.txt"
DEPENDENCY_RULES_FILE = "dependency.txt"

# configuration end

# ----------------------------------------------------------------------------------------------------

# demo begin

from pipeline.preprocessor import *

format_manual_marked_corpus(INPUTS_DIR, STAGE_DIR, MANUAL_MARKED_CORPUS_FILE, FORMATTED_MARKED_CORPUS_FILE)
transform_marked2unmarked_corpus(INPUTS_DIR, STAGE_DIR, FORMATTED_MARKED_CORPUS_FILE, INPUTS_FILE)

from pipeline.loader import *

conjunction_list = load_conjunctions(ASSISTS_DIR, STAGE_DIR, COORDINATING_CONJUNCTIONS_FILE, ADVERSATIVE_CONJUNCTIONS_FILE, CAUSAL_CONJUNCTIONS_FILE)
# print(conjunction_list)
function_word_pos_list = load_function_words_pos(ASSISTS_DIR, STAGE_DIR, FUNCTION_WORDS_POS_FILE)
# print(function_word_pos_list)
noun_pos_list = load_nouns_pos(ASSISTS_DIR, STAGE_DIR, NOUNS_POS_FILE)
# print(noun_pos_list)
chunking_rule_list = load_chunking_rules(RULES_DIR, STAGE_DIR, CHUNKING_RULES_FILE)
# print(chunking_rule_list)
dependency_rule_list = load_dependency_rules(RULES_DIR, STAGE_DIR, DEPENDENCY_RULES_FILE)
# print(dependency_rule_list)
conllu_list = load_conllu_data(INPUTS_DIR, STAGE_DIR, INPUTS_FILE)
# print(conllu_list)

from pipeline.chunker import *
from pipeline.parser import *

for token_list in conllu_list:
    # print(token_list.serialize())
    chunk_list = []
    chunk_tokens_by_function_words_pos(chunk_list, token_list, function_word_pos_list)
    # print_chunks(chunk_list)
    chunk_by_rules_sequentially(chunk_list, chunking_rule_list, noun_pos_list)
    # print_chunks(chunk_list)
    if is_a_single_sentence(chunk_list):
        # print("This is a single sentence.\n")
        parse_a_single_sentence(token_list, chunk_list, dependency_rule_list)
        # print(token_list.serialize())
        output_token_list(token_list, OUTPUTS_DIR, STAGE_DIR, OUTPUTS_FILE)
    else:
        # print("This is a complex sentence.\n")
        parse_a_complex_sentence(token_list, chunk_list, dependency_rule_list, conjunction_list)
        # print(token_list.serialize())
        output_token_list(token_list, OUTPUTS_DIR, STAGE_DIR, OUTPUTS_FILE)

from pipeline.evaluator import *

uas = calculate_uas(INPUTS_DIR, OUTPUTS_DIR, STAGE_DIR, FORMATTED_MARKED_CORPUS_FILE, OUTPUTS_FILE)
print("UAS: " + str(uas))
las = calculate_las(INPUTS_DIR, OUTPUTS_DIR, STAGE_DIR, FORMATTED_MARKED_CORPUS_FILE, OUTPUTS_FILE)
print("LAS: " + str(las))

# from pipeline.postprocessor import *
#
# draw_dependency_trees(OUTPUTS_DIR, STAGE_DIR, OUTPUTS_FILE)

# demo end
