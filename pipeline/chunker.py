def chunk_tokens_by_function_words(chunk_list, token_list, function_word_list):
    """
    Chunk Tokens by Function Words.

    :param chunk_list: Chunk List.
    :param token_list: Token List.
    :param function_word_list: Function Word List.
    """
    tmp_token_list = []
    for token in token_list:
        found = False
        for function_word in function_word_list:
            if token["lemma"] == function_word:
                found = True
                break
        if not found:
            tmp_token_list.append(token)
            if token == token_list[-1]:
                chunk_list.append(tmp_token_list)
        else:
            chunk_list.append(tmp_token_list)
            chunk_list.append([token])
            tmp_token_list = []
    tmp_index_list = []
    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 0:
            tmp_index_list.append(index)
    for index in tmp_index_list:
        del chunk_list[index]


def chunk_tokens_by_function_words_pos(chunk_list, token_list, function_word_pos_list):
    """
    Chunk Tokens by Function Words POS.

    :param chunk_list: Chunk List.
    :param token_list: Token List.
    :param function_word_pos_list: Function Word POS List.
    """
    tmp_token_list = []
    for token in token_list:
        found = False
        for function_word_pos in function_word_pos_list:
            if token["upos"] == function_word_pos or token["xpos"] == function_word_pos:
                found = True
                break
        if not found:
            tmp_token_list.append(token)
            if token == token_list[-1]:
                chunk_list.append(tmp_token_list)
        else:
            chunk_list.append(tmp_token_list)
            chunk_list.append([token])
            tmp_token_list = []
    tmp_index_list = []
    for index, chunk in enumerate(chunk_list):
        if len(chunk) == 0:
            tmp_index_list.append(index)
    for index in tmp_index_list:
        del chunk_list[index]


def chunk_by_rules_sequentially(chunk_list, chunking_rule_list, noun_pos_list):
    """
    Chunk by Chunking Rules sequentially.

    :param chunk_list: Chunk List.
    :param chunking_rule_list: Chunking Rule List.
    :param noun_pos_list: Noun POS List.
    """
    chunk_index = 0
    while chunk_index < len(chunk_list):
        chunk = chunk_list[chunk_index]
        chunking_rule_first_component = ""
        child_chunk_list = []
        if len(chunk) == 1:
            chunk_detail = {"chunk": chunk, "chunk_type": chunk[0]["upos"], "core_word": chunk[0]}
            chunk_list[chunk_index] = chunk_detail
            chunk_index += 1
        elif len(chunk) > 1:
            tmp_chunking_rule_component_index = 0
            tmp_chunking_rule_list = []
            chunk_token_index = 0
            while chunk_token_index < len(chunk):
                token = chunk[chunk_token_index]
                existed = False
                if tmp_chunking_rule_component_index == 0:
                    for chunking_rule in chunking_rule_list:
                        if token["upos"] == chunking_rule["components"][tmp_chunking_rule_component_index] or \
                                token["xpos"] == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                        if token["upos"] == "nx" and "NP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                        if token["upos"] == "vx" and "VP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                    if existed:
                        tmp_chunking_rule_component_index += 1
                    else:
                        chunk_list.insert(chunk_index + 1, chunk[chunk_token_index + 1:])
                        chunk = chunk[:chunk_token_index + 1]
                        chunk_detail = {"chunk": chunk, "chunk_type": chunk[0]["upos"], "core_word": chunk[0]}
                        chunk_list[chunk_index] = chunk_detail
                        chunk_index += 1
                elif tmp_chunking_rule_component_index > 0:
                    tmp_chunking_rule_index = 0
                    while tmp_chunking_rule_index < len(tmp_chunking_rule_list):
                        tmp_chunking_rule = tmp_chunking_rule_list[tmp_chunking_rule_index]
                        if tmp_chunking_rule_component_index >= len(tmp_chunking_rule["components"]):
                            counter = 0
                            for index, component in enumerate(tmp_chunking_rule["components"]):
                                if chunk[index]["upos"] == component or chunk[index]["xpos"] == component:
                                    counter += 1
                            if counter == len(tmp_chunking_rule["components"]):
                                chunking_rule_first_component = tmp_chunking_rule["type"]
                            del tmp_chunking_rule_list[tmp_chunking_rule_index]
                            tmp_chunking_rule_index -= 1
                        else:
                            if token["upos"] == tmp_chunking_rule["components"][tmp_chunking_rule_component_index] or \
                                    token["xpos"] == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                                existed = True
                            elif token["upos"] == "nx" and "NP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                                existed = True
                            elif token["upos"] == "vx" and "VP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                                existed = True
                            else:
                                del tmp_chunking_rule_list[tmp_chunking_rule_index]
                                tmp_chunking_rule_index -= 1
                        tmp_chunking_rule_index += 1
                    if existed:
                        tmp_chunking_rule_component_index += 1
                        if len(tmp_chunking_rule_list) == 1 and tmp_chunking_rule_component_index == len(tmp_chunking_rule_list[0]["components"]):
                            if chunk_token_index != len(chunk) - 1:
                                child_chunk_detail = {"chunk": chunk[:chunk_token_index + 1], "chunk_type": tmp_chunking_rule_list[0]["type"]}
                                if tmp_chunking_rule_list[0]["type"] == "NP":
                                    for token in reversed(chunk[:chunk_token_index + 1]):
                                        flag = False
                                        for noun_pos in noun_pos_list:
                                            if token["upos"] == noun_pos:
                                                child_chunk_detail["core_word"] = token
                                                flag = True
                                                break
                                        if flag:
                                            break
                                if tmp_chunking_rule_list[0]["type"] == "VP":
                                    found_vx = False
                                    found_nv = False
                                    found_ax = False
                                    for token in chunk[:chunk_token_index + 1]:
                                        if token["upos"] == "vx":
                                            found_vx = True
                                            child_chunk_detail["core_word"] = token
                                            break
                                    if not found_vx:
                                        for token in chunk[:chunk_token_index + 1]:
                                            if token["xpos"] == "nv":
                                                found_nv = True
                                                child_chunk_detail["core_word"] = token
                                                break
                                    if not found_vx and not found_nv:
                                        for token in reversed(chunk[:chunk_token_index + 1]):
                                            if token["upos"] == "ax":
                                                found_ax = True
                                                child_chunk_detail["core_word"] = token
                                                break
                                    if not found_vx and not found_nv and not found_ax:
                                        for token in chunk[:chunk_token_index + 1]:
                                            if token["upos"] == "ux":
                                                child_chunk_detail["core_word"] = token
                                                break
                                if tmp_chunking_rule_list[0]["type"] == "QP":
                                    if len(chunk[:chunk_token_index + 1]) == 3:
                                        child_chunk_detail["core_word"] = chunk[:chunk_token_index + 1][-1]
                                    elif len(chunk[:chunk_token_index + 1]) == 2:
                                        if (chunk[:chunk_token_index + 1][0]["upos"] == "mx" and chunk[:chunk_token_index + 1][1]["upos"] == "qx") or \
                                                (chunk[:chunk_token_index + 1][0]["upos"] == "rx" and chunk[:chunk_token_index + 1][1][
                                                    "upos"] == "mx") or \
                                                (chunk[:chunk_token_index + 1][0]["upos"] == "ax" and chunk[:chunk_token_index + 1][1][
                                                    "upos"] == "mx") or \
                                                (chunk[:chunk_token_index + 1][0]["upos"] == "tt" and chunk[:chunk_token_index + 1][1][
                                                    "upos"] == "mx"):
                                            child_chunk_detail["core_word"] = chunk[:chunk_token_index + 1][0]
                                        if (chunk[:chunk_token_index + 1][0]["upos"] == "qx" and chunk[:chunk_token_index + 1][1]["upos"] == "mx") or \
                                                (chunk[:chunk_token_index + 1][0]["upos"] == "mx" and chunk[:chunk_token_index + 1][1][
                                                    "upos"] == "mx") or \
                                                (chunk[:chunk_token_index + 1][0]["upos"] == "tt" and chunk[:chunk_token_index + 1][1][
                                                    "upos"] == "tt"):
                                            child_chunk_detail["core_word"] = chunk[:chunk_token_index + 1][1]
                                child_chunk_list.append(child_chunk_detail)
                                chunking_rule_first_component = tmp_chunking_rule_list[0]["type"]
                                tmp_chunking_rule_component_index = 0
                                tmp_chunking_rule_list = []
                                for chunking_rule in chunking_rule_list:
                                    if chunking_rule_first_component == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                        tmp_chunking_rule_list.append(chunking_rule)
                                tmp_chunking_rule_component_index += 1
                            else:
                                chunk_detail = {"chunk": chunk, "chunk_type": tmp_chunking_rule_list[0]["type"]}
                                if chunk_detail["chunk_type"] == "NP":
                                    for token in reversed(chunk):
                                        flag = False
                                        for noun_pos in noun_pos_list:
                                            if token["upos"] == noun_pos:
                                                chunk_detail["core_word"] = token
                                                flag = True
                                                break
                                        if flag:
                                            break
                                if chunk_detail["chunk_type"] == "VP":
                                    found_vx = False
                                    found_nv = False
                                    found_ax = False
                                    for token in chunk:
                                        if token["upos"] == "vx":
                                            found_vx = True
                                            chunk_detail["core_word"] = token
                                            break
                                    if not found_vx:
                                        for token in chunk:
                                            if token["xpos"] == "nv":
                                                found_nv = True
                                                chunk_detail["core_word"] = token
                                                break
                                    if not found_vx and not found_nv:
                                        for token in reversed(chunk):
                                            if token["upos"] == "ax":
                                                found_ax = True
                                                chunk_detail["core_word"] = token
                                                break
                                    if not found_vx and not found_nv and not found_ax:
                                        for token in chunk:
                                            if token["upos"] == "ux":
                                                chunk_detail["core_word"] = token
                                                break
                                if chunk_detail["chunk_type"] == "QP":
                                    if len(chunk) == 3:
                                        chunk_detail["core_word"] = chunk[-1]
                                    elif len(chunk) == 2:
                                        if (chunk[0]["upos"] == "mx" and chunk[1]["upos"] == "qx") or \
                                                (chunk[0]["upos"] == "rx" and chunk[1]["upos"] == "mx") or \
                                                (chunk[0]["upos"] == "ax" and chunk[1]["upos"] == "mx") or \
                                                (chunk[0]["upos"] == "tt" and chunk[1]["upos"] == "mx"):
                                            chunk_detail["core_word"] = chunk[0]
                                        if (chunk[0]["upos"] == "qx" and chunk[1]["upos"] == "mx") or \
                                                (chunk[0]["upos"] == "mx" and chunk[1]["upos"] == "mx") or \
                                                (chunk[0]["upos"] == "tt" and chunk[1]["upos"] == "tt"):
                                            chunk_detail["core_word"] = chunk[1]
                                if len(child_chunk_list) != 0:
                                    # TODO: if children have siblings or children, then?
                                    chunk_detail["children"] = child_chunk_list
                                chunk_list[chunk_index] = chunk_detail
                                chunk_index += 1
                        elif len(tmp_chunking_rule_list) == 1 and tmp_chunking_rule_component_index > len(tmp_chunking_rule_list[0]["components"]):
                            counter = 1
                            for token in reversed(chunk):
                                if token["id"] != chunk[0]["id"]:
                                    counter += 1
                                    chunk_detail = {"chunk": [token], "chunk_type": token["upos"], "core_word": token}
                                    chunk_list.insert(chunk_index + 1, chunk_detail)
                                else:
                                    chunk_detail = {"chunk": [token], "chunk_type": token["upos"], "core_word": token}
                                    chunk_list[chunk_index] = chunk_detail
                            chunk_index += counter
                    else:
                        if chunking_rule_first_component == "":
                            chunk_list.insert(chunk_index + 1, chunk[chunk_token_index:])
                            chunk = chunk[:chunk_token_index]
                            counter = 1
                            for token in reversed(chunk):
                                if token["id"] != chunk[0]["id"]:
                                    counter += 1
                                    chunk_detail = {"chunk": [token], "chunk_type": token["upos"], "core_word": token}
                                    chunk_list.insert(chunk_index + 1, chunk_detail)
                                else:
                                    chunk_detail = {"chunk": [token], "chunk_type": token["upos"], "core_word": token}
                                    chunk_list[chunk_index] = chunk_detail
                            chunk_index += counter
                        else:
                            if tmp_chunking_rule_component_index == 1:
                                chunk_list.insert(chunk_index + 1, chunk[chunk_token_index:])
                                chunk = chunk[:chunk_token_index]
                            elif tmp_chunking_rule_component_index == 2:
                                if tmp_chunking_rule_component_index < chunk_token_index:
                                    chunk_list.insert(chunk_index + 1, chunk[chunk_token_index - 1:])
                                    chunk = chunk[:chunk_token_index - 1]
                                else:
                                    chunk_list.insert(chunk_index + 1, chunk[chunk_token_index:])
                                    chunk = chunk[:chunk_token_index]
                            chunk_detail = {"chunk": chunk, "chunk_type": chunking_rule_first_component}
                            if chunk_detail["chunk_type"] == "NP":
                                for token in reversed(chunk):
                                    flag = False
                                    for noun_pos in noun_pos_list:
                                        if token["upos"] == noun_pos or token["xpos"] == noun_pos:
                                            chunk_detail["core_word"] = token
                                            flag = True
                                            break
                                    if flag:
                                        break
                            if chunk_detail["chunk_type"] == "VP":
                                found_vx = False
                                found_nv = False
                                found_ax = False
                                for token in chunk:
                                    if token["upos"] == "vx":
                                        found_vx = True
                                        chunk_detail["core_word"] = token
                                        break
                                if not found_vx:
                                    for token in chunk:
                                        if token["xpos"] == "nv":
                                            found_nv = True
                                            chunk_detail["core_word"] = token
                                            break
                                if not found_vx and not found_nv:
                                    for token in reversed(chunk):
                                        if token["upos"] == "ax":
                                            found_ax = True
                                            chunk_detail["core_word"] = token
                                            break
                                if not found_vx and not found_nv and not found_ax:
                                    for token in chunk:
                                        if token["upos"] == "ux":
                                            chunk_detail["core_word"] = token
                                            break
                            if chunk_detail["chunk_type"] == "QP":
                                if len(chunk) == 3:
                                    chunk_detail["core_word"] = chunk[-1]
                                elif len(chunk) == 2:
                                    if (chunk[0]["upos"] == "mx" and chunk[1]["upos"] == "qx") or \
                                            (chunk[0]["upos"] == "rx" and chunk[1]["upos"] == "mx") or \
                                            (chunk[0]["upos"] == "ax" and chunk[1]["upos"] == "mx") or \
                                            (chunk[0]["upos"] == "tt" and chunk[1]["upos"] == "mx"):
                                        chunk_detail["core_word"] = chunk[0]
                                    if (chunk[0]["upos"] == "qx" and chunk[1]["upos"] == "mx") or \
                                            (chunk[0]["upos"] == "mx" and chunk[1]["upos"] == "mx") or \
                                            (chunk[0]["upos"] == "tt" and chunk[1]["upos"] == "tt"):
                                        chunk_detail["core_word"] = chunk[1]
                            if len(child_chunk_list) != 0:
                                child_chunk_list = child_chunk_list[:-1]
                            if len(child_chunk_list) != 0:
                                # TODO: if children have siblings or children, then?
                                chunk_detail["children"] = child_chunk_list
                            chunk_list[chunk_index] = chunk_detail
                            chunk_index += 1
                chunk_token_index += 1
    for index, chunk in enumerate(chunk_list):
        if len(chunk["chunk"]) == 1 and \
                (chunk_list[index]["chunk"][0]["upos"] == "ux" or
                 chunk_list[index]["chunk"][0]["upos"] == "ax" or
                 chunk_list[index]["chunk"][0]["xpos"] == "df"):
            chunk_list[index]["chunk"][0]["upos"] = "vx"
            chunk_list[index]["chunk_type"] = "vx"
            chunk_list[index]["core_word"]["upos"] = "vx"


def print_chunks(chunk_list):
    """
    Print Chunks.

    :param chunk_list: Chunk List.
    """
    for chunk_index, chunk in enumerate(chunk_list):
        print(chunk_index)
        print(chunk)
    print("\n")
