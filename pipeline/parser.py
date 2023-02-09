import os


def is_a_single_sentence(chunk_list):
    """
    Judge whether a sentence is a single sentence.

    :param chunk_list: Chunk List.
    :return: True or False.
    """
    vp_counter = 0
    for chunk in chunk_list:
        if chunk["chunk_type"] == "VP" or chunk["chunk_type"] == "vx":
            vp_counter += 1
    if vp_counter == 1:
        return True
    elif vp_counter > 1:
        return False


def parse_a_chunk(token_list, chunk, dependency_rule_list):
    """
    Parse a chunk.

    :param token_list: Token List.
    :param chunk: Chunk.
    :param dependency_rule_list: Dependency Rule List.
    """
    buffer_token_list = []
    for token in reversed(chunk):
        if len(buffer_token_list) == 0:
            buffer_token_list.insert(0, token)
            continue
        left_arc_num = 0
        right_arc_num = 0
        need_to_be_marked = False
        head = 0
        deprel = ""
        if len(buffer_token_list) >= 2:
            for index_i in range(0, len(buffer_token_list) - 1):
                for index_j in range(index_i + 1, len(buffer_token_list)):
                    for dependency_rule in dependency_rule_list:
                        if left_arc_num < 1 and len(dependency_rule["components"]) == 3 and buffer_token_list[index_i]["blank_head"] == "-" and \
                                ((token["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (token["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (token["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 (token["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (token["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 (token["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2])):
                            left_arc_num += 1
                            token_list[buffer_token_list[index_i]["id"] - 1]["blank_head"] = token["id"]
                            buffer_token_list[index_i]["blank_head"] = token["id"]
                            if buffer_token_list[index_i]["xpos"] == "yy":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "YY"
                                buffer_token_list[index_i]["blank_deprel"] = "YY"
                            if buffer_token_list[index_i]["xpos"] == "gz":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GZ"
                                buffer_token_list[index_i]["blank_deprel"] = "GZ"
                            if buffer_token_list[index_i]["xpos"] == "gx":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GX"
                                buffer_token_list[index_i]["blank_deprel"] = "GX"
                            if buffer_token_list[index_i]["xpos"] == "gl":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GL"
                                buffer_token_list[index_i]["blank_deprel"] = "GL"
                            need_to_be_marked = True
                            head = buffer_token_list[index_j]["id"]
                            deprel = dependency_rule["relation"]
                            token_list[token["id"] - 1]["blank_head"] = head
                            token_list[token["id"] - 1]["blank_deprel"] = deprel
                        if left_arc_num == 1:
                            break
                    if left_arc_num == 1:
                        break
                if left_arc_num == 1:
                    break
        if len(buffer_token_list) >= 1:
            for buffer_token in buffer_token_list:
                for dependency_rule in dependency_rule_list:
                    if len(dependency_rule["components"]) == 2 and \
                            ((token["xpos"] == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (token["upos"] == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (token["xpos"] == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             (token["upos"] == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             ("xx" == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (token["xpos"] == dependency_rule["components"][0] and
                              "xx" == dependency_rule["components"][1]) or
                             ("xx" == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             (token["upos"] == dependency_rule["components"][0] and
                              "xx" == dependency_rule["components"][1])):
                        if left_arc_num < 1 and dependency_rule["direction"] == "L":
                            need_to_be_marked = True
                            head = buffer_token["id"]
                            deprel = dependency_rule["relation"]
                            token_list[token["id"] - 1]["blank_head"] = head
                            token_list[token["id"] - 1]["blank_deprel"] = deprel
                            left_arc_num += 1
                        if right_arc_num < 1 and dependency_rule["direction"] == "R" and buffer_token["blank_head"] == "-":
                            token_list[buffer_token["id"] - 1]["blank_head"] = token["id"]
                            buffer_token["blank_head"] = token["id"]
                            token_list[buffer_token["id"] - 1]["blank_deprel"] = dependency_rule["relation"]
                            buffer_token["blank_deprel"] = dependency_rule["relation"]
                            right_arc_num += 1
                    if left_arc_num == 1 and right_arc_num == 1:
                        break
                if left_arc_num == 1 and right_arc_num == 1:
                    break
        buffer_token_list.insert(0, token)
        if need_to_be_marked:
            buffer_token_list[0]["blank_head"] = head
            buffer_token_list[0]["blank_deprel"] = deprel


def parse_a_single_sentence(token_list, chunk_list, dependency_rule_list):
    """
    Parse a single sentence.

    :param token_list: Token List.
    :param chunk_list: Chunk List.
    :param dependency_rule_list: Dependency Rule List.
    """
    buffer_token_list = []
    for chunk in reversed(chunk_list):
        if len(chunk["chunk"]) != 1:
            parse_a_chunk(token_list, chunk["chunk"], dependency_rule_list)
        if len(buffer_token_list) == 0:
            buffer_token_list = chunk["chunk"] + buffer_token_list
            continue
        left_arc_num = 0
        right_arc_num = 0
        need_to_be_marked = False
        head = 0
        deprel = ""
        if chunk["core_word"]["upos"] == "vx":
            need_to_be_marked = True
            head = 0
            deprel = "ROOT"
            token_list[chunk["core_word"]["id"] - 1]["blank_head"] = head
            token_list[chunk["core_word"]["id"] - 1]["blank_deprel"] = deprel
        if len(buffer_token_list) >= 2:
            for index_i in range(0, len(buffer_token_list) - 1):
                for index_j in range(index_i + 1, len(buffer_token_list)):
                    for dependency_rule in dependency_rule_list:
                        if left_arc_num < 1 and len(dependency_rule["components"]) == 3 and buffer_token_list[index_i]["blank_head"] == "-" and \
                                ((chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["xpos"] == dependency_rule["components"][2]) or
                                 (chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  buffer_token_list[index_j]["upos"] == dependency_rule["components"][2]) or
                                 (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2]) or
                                 ("xx" == dependency_rule["components"][0] and
                                  buffer_token_list[index_i]["xpos"] == dependency_rule["components"][1] and
                                  "xx" == dependency_rule["components"][2])):
                            left_arc_num += 1
                            token_list[buffer_token_list[index_i]["id"] - 1]["blank_head"] = chunk["core_word"]["id"]
                            buffer_token_list[index_i]["blank_head"] = chunk["core_word"]["id"]
                            if buffer_token_list[index_i]["xpos"] == "yy":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "YY"
                                buffer_token_list[index_i]["blank_deprel"] = "YY"
                            if buffer_token_list[index_i]["xpos"] == "gz":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GZ"
                                buffer_token_list[index_i]["blank_deprel"] = "GZ"
                            if buffer_token_list[index_i]["xpos"] == "gx":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GX"
                                buffer_token_list[index_i]["blank_deprel"] = "GX"
                            if buffer_token_list[index_i]["xpos"] == "gl":
                                token_list[buffer_token_list[index_i]["id"] - 1]["blank_deprel"] = "GL"
                                buffer_token_list[index_i]["blank_deprel"] = "GL"
                            need_to_be_marked = True
                            head = buffer_token_list[index_j]["id"]
                            deprel = dependency_rule["relation"]
                            token_list[chunk["core_word"]["id"] - 1]["blank_head"] = head
                            token_list[chunk["core_word"]["id"] - 1]["blank_deprel"] = deprel
                        if left_arc_num == 1:
                            break
                    if left_arc_num == 1:
                        break
                if left_arc_num == 1:
                    break
        if len(buffer_token_list) >= 1:
            for buffer_token in buffer_token_list:
                for dependency_rule in dependency_rule_list:
                    if len(dependency_rule["components"]) == 2 and \
                            ((chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             ("xx" == dependency_rule["components"][0] and
                              buffer_token["xpos"] == dependency_rule["components"][1]) or
                             (chunk["core_word"]["xpos"] == dependency_rule["components"][0] and
                              "xx" == dependency_rule["components"][1]) or
                             ("xx" == dependency_rule["components"][0] and
                              buffer_token["upos"] == dependency_rule["components"][1]) or
                             (chunk["core_word"]["upos"] == dependency_rule["components"][0] and
                              "xx" == dependency_rule["components"][1])):
                        if left_arc_num < 1 and dependency_rule["direction"] == "L":
                            need_to_be_marked = True
                            head = buffer_token["id"]
                            deprel = dependency_rule["relation"]
                            token_list[chunk["core_word"]["id"] - 1]["blank_head"] = head
                            token_list[chunk["core_word"]["id"] - 1]["blank_deprel"] = deprel
                            left_arc_num += 1
                        if right_arc_num < 1 and dependency_rule["direction"] == "R" and buffer_token["blank_head"] == "-":
                            token_list[buffer_token["id"] - 1]["blank_head"] = chunk["core_word"]["id"]
                            buffer_token["blank_head"] = chunk["core_word"]["id"]
                            token_list[buffer_token["id"] - 1]["blank_deprel"] = dependency_rule["relation"]
                            buffer_token["blank_deprel"] = dependency_rule["relation"]
                            right_arc_num += 1
                    if left_arc_num == 1 and right_arc_num == 1:
                        break
                if left_arc_num == 1 and right_arc_num == 1:
                    break
        buffer_token_list = chunk["chunk"] + buffer_token_list
        if need_to_be_marked:
            buffer_token_list[chunk["core_word"]["id"] - buffer_token_list[0]["id"]]["blank_head"] = head
            buffer_token_list[chunk["core_word"]["id"] - buffer_token_list[0]["id"]]["blank_deprel"] = deprel


def parse_a_complex_sentence(token_list, chunk_list, dependency_rule_list, conjunction_list):
    """
    Parse a complex sentence.
    :param token_list: Token List.
    :param chunk_list: Chunk List.
    :param dependency_rule_list: Dependency Rule List.
    :param conjunction_list: Conjunction List.
    """
    single_sentence_list = []
    vp_index_list = []
    for chunk_index, chunk in enumerate(chunk_list):
        if chunk["chunk_type"] == "VP" or chunk["chunk_type"] == "vx":
            vp_index_list.append(chunk_index)
    for vp_index_index in range(0, len(vp_index_list)):
        if vp_index_index == 0:
            if chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "cx" or \
                    chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "lz":
                single_sentence_list.append(chunk_list[0:vp_index_list[vp_index_index] + 1 + 1])
            elif chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "cx" and \
                    chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "lz":
                single_sentence_list.append(chunk_list[0:vp_index_list[vp_index_index] + 1])
        elif vp_index_index == len(vp_index_list) - 1:
            if chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "cx" or \
                    chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "lz":
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1 + 1:len(chunk_list)])
            elif chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "cx" and \
                    chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "lz":
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1:len(chunk_list)])
        else:
            if (chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "cx" or
                chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "lz") and \
                    (chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "cx" or
                     chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "lz"):
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1 + 1:vp_index_list[vp_index_index] + 1 + 1])
            elif (chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "cx" and
                  chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "lz") and \
                    (chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "cx" or
                     chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "lz"):
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1:vp_index_list[vp_index_index] + 1 + 1])
            elif (chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "cx" or
                  chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] == "lz") and \
                    (chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "cx" and
                     chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "lz"):
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1 + 1:vp_index_list[vp_index_index] + 1])
            elif (chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "cx" and
                  chunk_list[vp_index_list[vp_index_index - 1] + 1]["chunk_type"] != "lz") and \
                    (chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "cx" and
                     chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "lz"):
                single_sentence_list.append(chunk_list[vp_index_list[vp_index_index - 1] + 1:vp_index_list[vp_index_index] + 1])
    for single_sentence in single_sentence_list:
        parse_a_single_sentence(token_list, single_sentence, dependency_rule_list)
    for vp_index_index in range(0, len(vp_index_list) - 1):
        if chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "cx":
            first_vx_id = 0
            second_vx_id = 0
            for token in chunk_list[vp_index_list[vp_index_index]]["chunk"]:
                if token["upos"] == "vx":
                    first_vx_id = token["id"]
                    break
            for token in chunk_list[vp_index_list[vp_index_index + 1]]["chunk"]:
                if token["upos"] == "vx":
                    second_vx_id = token["id"]
                    break
            token_list[first_vx_id - 1]["blank_head"] = second_vx_id
            cx_type = ""
            for conjunction_dict in conjunction_list:
                found = False
                for conjunction in conjunction_dict["list"]:
                    if chunk_list[vp_index_list[vp_index_index] + 1]["core_word"]["lemma"] == conjunction:
                        cx_type = conjunction_dict["type"]
                        found = True
                        break
                if found:
                    break
            if cx_type == "coordinating":
                token_list[first_vx_id - 1]["blank_deprel"] = "BLFH"
            if cx_type == "adversative":
                token_list[first_vx_id - 1]["blank_deprel"] = "ZZFH"
            if cx_type == "causal":
                token_list[first_vx_id - 1]["blank_deprel"] = "YGFH"
            token_list[chunk_list[vp_index_list[vp_index_index] + 1]["core_word"]["id"] - 1]["blank_head"] = first_vx_id
            token_list[chunk_list[vp_index_list[vp_index_index] + 1]["core_word"]["id"] - 1]["blank_deprel"] = "GLC"
        elif chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] == "lz":
            first_vx_id = 0
            second_vx_id = 0
            for token in chunk_list[vp_index_list[vp_index_index]]["chunk"]:
                if token["upos"] == "vx":
                    first_vx_id = token["id"]
                    break
            for token in chunk_list[vp_index_list[vp_index_index + 1]]["chunk"]:
                if token["upos"] == "vx":
                    second_vx_id = token["id"]
                    break
            token_list[first_vx_id - 1]["blank_head"] = second_vx_id
            token_list[first_vx_id - 1]["blank_deprel"] = "FH"
            token_list[chunk_list[vp_index_list[vp_index_index] + 1]["core_word"]["id"] - 1]["blank_head"] = first_vx_id
            token_list[chunk_list[vp_index_list[vp_index_index] + 1]["core_word"]["id"] - 1]["blank_deprel"] = "PUNCT"
        elif chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "cx" and \
                chunk_list[vp_index_list[vp_index_index] + 1]["chunk_type"] != "lz":
            first_vx_id = 0
            second_vx_id = 0
            for token in chunk_list[vp_index_list[vp_index_index]]["chunk"]:
                if token["upos"] == "vx":
                    first_vx_id = token["id"]
                    break
            for token in chunk_list[vp_index_list[vp_index_index + 1]]["chunk"]:
                if token["upos"] == "vx":
                    second_vx_id = token["id"]
                    break
            token_list[first_vx_id - 1]["blank_head"] = second_vx_id
            token_list[first_vx_id - 1]["blank_deprel"] = "FH"


def output_token_list(token_list, outputs_dir, stage_dir, outputs_file):
    """
    Output Token List.

    :param token_list: Token List.
    :param outputs_dir: Outputs Directory.
    :param stage_dir: Stage Directory.
    :param outputs_file: Outputs File.
    """
    with open(os.path.join(outputs_dir, stage_dir, outputs_file), "a", encoding="utf-8") as outputs_file:
        outputs_file.write(token_list.serialize())
