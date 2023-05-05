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
                        if token["upos"] == chunking_rule["components"][tmp_chunking_rule_component_index]:
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
                        if token["upos"] == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] == "nx" and "NP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] == "vx" and "VP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] != tmp_chunking_rule["components"][tmp_chunking_rule_component_index] and \
                                tmp_chunking_rule["components"][tmp_chunking_rule_component_index].islower():
                            del tmp_chunking_rule_list[tmp_chunking_rule_index]
                            tmp_chunking_rule_index -= 1
                        tmp_chunking_rule_index += 1
                    if existed:
                        tmp_chunking_rule_component_index += 1
                        if len(tmp_chunking_rule_list) == 1 and tmp_chunking_rule_component_index == len(tmp_chunking_rule_list[0]["components"]):
                            if chunk_token_index != len(chunk) - 1:
                                chunking_rule_first_component = tmp_chunking_rule_list[0]["type"]
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
                                    for token in chunk[:chunk_token_index + 1]:
                                        if token["upos"] == "vx":
                                            child_chunk_detail["core_word"] = token
                                            break
                                child_chunk_list.append(child_chunk_detail)
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
                                    for token in chunk:
                                        if token["upos"] == "vx":
                                            chunk_detail["core_word"] = token
                                            break
                                if len(child_chunk_list) != 0:
                                    # TODO: if children have siblings or children, then?
                                    chunk_detail["children"] = child_chunk_list
                                chunk_list[chunk_index] = chunk_detail
                                chunk_index += 1
                    else:
                        # TODO: like chunk_by_rules_reversely(chunk_list, chunking_rule_list)?
                        chunk_list.insert(chunk_index + 1, chunk[chunk_token_index:])
                        chunk = chunk[:chunk_token_index]
                        chunk_detail = {"chunk": chunk}
                        if chunking_rule_first_component == "":
                            # TODO: chunking_rule_first_component == "" means len(chunk) == 1?
                            chunk_detail["chunk_type"] = chunk[0]["upos"]
                            chunk_detail["core_word"] = chunk[0]
                        else:
                            if len(child_chunk_list) != 0:
                                child_chunk_list = child_chunk_list[:-1]
                            chunk_detail["chunk_type"] = chunking_rule_first_component
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
                                for token in chunk:
                                    if token["upos"] == "vx":
                                        chunk_detail["core_word"] = token
                                        break
                            if len(child_chunk_list) != 0:
                                # TODO: if children have siblings or children, then?
                                chunk_detail["children"] = child_chunk_list
                        chunk_list[chunk_index] = chunk_detail
                        chunk_index += 1
                chunk_token_index += 1


def chunk_by_rules_reversely(chunk_list, chunking_rule_list, noun_pos_list):
    """
    Chunk by Chunking Rules reversely.

    :param chunk_list: Chunk List.
    :param chunking_rule_list: Chunking Rule List.
    :param noun_pos_list: Noun POS List.
    """
    counter = 1
    chunk_index = 0
    while chunk_index < len(chunk_list):
        chunk = chunk_list[chunk_index]
        chunking_rule_last_component = ""
        child_chunk_list = []
        if len(chunk) == 1:
            chunk_detail = {"chunk": chunk, "chunk_type": chunk[0]["upos"], "core_word": chunk[0]}
            chunk_list[chunk_index] = chunk_detail
            chunk_index += 1
        elif len(chunk) > 1:
            tmp_chunking_rule_component_index = -1
            tmp_chunking_rule_list = []
            tmp_chunking_rule_list2 = []
            chunk_token_index = -1
            while chunk_token_index >= -len(chunk):
                token = chunk[chunk_token_index]
                existed = False
                if tmp_chunking_rule_component_index == -1:
                    for chunking_rule in chunking_rule_list:
                        if token["upos"] == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                        if token["upos"] == "nx" and "NP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                        if token["upos"] == "vx" and "VP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                            tmp_chunking_rule_list.append(chunking_rule)
                            existed = True
                    if existed:
                        if token["id"] != chunk[0]["id"]:
                            tmp_chunking_rule_component_index -= 1
                        else:
                            chunk_detail = {"chunk": chunk, "chunk_type": chunk[0]["upos"], "core_word": chunk[0]}
                            chunk_list[chunk_index] = chunk_detail
                            chunk_index += counter
                            counter = 1
                    else:
                        if token["id"] != chunk[0]["id"]:
                            chunk_detail = {"chunk": chunk[chunk_token_index:], "chunk_type": chunk[chunk_token_index:][-1]["upos"],
                                            "core_word": chunk[chunk_token_index:][-1]}
                            chunk_list.insert(chunk_index + 1, chunk_detail)
                            chunk = chunk[:chunk_token_index]
                            chunk_list[chunk_index] = chunk
                            tmp_chunking_rule_component_index = -1
                            tmp_chunking_rule_list = []
                            chunk_token_index = 0
                            counter += 1
                        else:
                            chunk_detail = {"chunk": chunk, "chunk_type": chunk[0]["upos"], "core_word": chunk[0]}
                            chunk_list[chunk_index] = chunk_detail
                            chunk_index += counter
                            counter = 1
                elif tmp_chunking_rule_component_index < -1:
                    tmp_chunking_rule_index = 0
                    while tmp_chunking_rule_index < len(tmp_chunking_rule_list):
                        tmp_chunking_rule = tmp_chunking_rule_list[tmp_chunking_rule_index]
                        if token["upos"] == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] == "nx" and "NP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] == "vx" and "VP" == tmp_chunking_rule["components"][tmp_chunking_rule_component_index]:
                            existed = True
                        if token["upos"] != tmp_chunking_rule["components"][tmp_chunking_rule_component_index] and \
                                tmp_chunking_rule["components"][tmp_chunking_rule_component_index].islower():
                            del tmp_chunking_rule_list[tmp_chunking_rule_index]
                            tmp_chunking_rule_index -= 1
                        tmp_chunking_rule_index += 1
                    if existed:
                        if len(tmp_chunking_rule_list) == 1 and tmp_chunking_rule_component_index == -len(tmp_chunking_rule_list[0]["components"]):
                            if len(tmp_chunking_rule_list2) == 0:
                                if chunk_token_index != -len(chunk):
                                    chunking_rule_last_component = tmp_chunking_rule_list[0]["type"]
                                    child_chunk_detail = {"chunk": chunk[chunk_token_index:], "chunk_type": tmp_chunking_rule_list[0]["type"]}
                                    if tmp_chunking_rule_list[0]["type"] == "NP":
                                        for token in reversed(chunk[chunk_token_index:]):
                                            flag = False
                                            for noun_pos in noun_pos_list:
                                                if token["upos"] == noun_pos:
                                                    child_chunk_detail["core_word"] = token
                                                    flag = True
                                                    break
                                            if flag:
                                                break
                                    if tmp_chunking_rule_list[0]["type"] == "VP":
                                        for token in chunk[chunk_token_index:]:
                                            if token["upos"] == "vx":
                                                child_chunk_detail["core_word"] = token
                                                break
                                    child_chunk_list.append(child_chunk_detail)
                                    tmp_chunking_rule_component_index = -1
                                    tmp_chunking_rule_list = []
                                    for chunking_rule in chunking_rule_list:
                                        if chunking_rule_last_component == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                            tmp_chunking_rule_list.append(chunking_rule)
                                    tmp_chunking_rule_component_index -= 1
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
                                        for token in chunk:
                                            if token["upos"] == "vx":
                                                chunk_detail["core_word"] = token
                                                break
                                    if len(child_chunk_list) != 0:
                                        # TODO: if children have siblings or children, then?
                                        chunk_detail["children"] = child_chunk_list
                                    chunk_list[chunk_index] = chunk_detail
                                    chunk_index += counter
                                    counter = 1
                            else:
                                # TODO: len(tmp_chunking_rule_list2) == 1 or not?
                                if tmp_chunking_rule_list[0]["type"] == tmp_chunking_rule_list2[0]["components"][0]:
                                    # TODO: have bugs?
                                    child_chunk_detail = {
                                        "chunk": chunk[chunk_token_index:chunk_token_index + len(tmp_chunking_rule_list[0]["components"])],
                                        "chunk_type": tmp_chunking_rule_list[0]["type"]}
                                    if tmp_chunking_rule_list[0]["type"] == "NP":
                                        for token in reversed(
                                                chunk[chunk_token_index:chunk_token_index + len(tmp_chunking_rule_list[0]["components"])]):
                                            flag = False
                                            for noun_pos in noun_pos_list:
                                                if token["upos"] == noun_pos:
                                                    child_chunk_detail["core_word"] = token
                                                    flag = True
                                                    break
                                            if flag:
                                                break
                                    if tmp_chunking_rule_list[0]["type"] == "VP":
                                        for token in chunk[chunk_token_index:chunk_token_index + len(tmp_chunking_rule_list[0]["components"])]:
                                            if token["upos"] == "vx":
                                                child_chunk_detail["core_word"] = token
                                                break
                                    child_chunk_list.append(child_chunk_detail)
                                    tmp_chunking_rule_list = [tmp_chunking_rule_list2[0]]
                                    tmp_chunking_rule_list2 = []
                                    if chunk_token_index != -len(chunk):
                                        chunking_rule_last_component = tmp_chunking_rule_list[0]["type"]
                                        tmp_chunking_rule_component_index = -1
                                        tmp_chunking_rule_list = []
                                        for chunking_rule in chunking_rule_list:
                                            if chunking_rule_last_component == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                                tmp_chunking_rule_list.append(chunking_rule)
                                        if len(tmp_chunking_rule_list) == 0:
                                            chunk_detail = {"chunk": chunk[chunk_token_index:], "chunk_type": chunking_rule_last_component}
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
                                                for token in chunk:
                                                    if token["upos"] == "vx":
                                                        chunk_detail["core_word"] = token
                                                        break
                                            # TODO: if children have siblings or children, then?
                                            chunk_detail["children"] = child_chunk_list
                                            chunk_list.insert(chunk_index + 1, chunk_detail)
                                            chunk = chunk[:chunk_token_index]
                                            chunk_list[chunk_index] = chunk
                                            if len(child_chunk_list) != 0:
                                                # TODO: have other possibilities, then?
                                                child_chunk_list = child_chunk_list[1:]
                                            tmp_chunking_rule_component_index = -1
                                            tmp_chunking_rule_list = []
                                            chunk_token_index = 0
                                            counter += 1
                                        else:
                                            # TODO: if len(tmp_chunking_rule_list) != 0, then?
                                            pass
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
                                            for token in chunk:
                                                if token["upos"] == "vx":
                                                    chunk_detail["core_word"] = token
                                                    break
                                        # TODO: if children have siblings or children, then?
                                        chunk_detail["children"] = child_chunk_list
                                        chunk_list[chunk_index] = chunk_detail
                                        chunk_index += counter
                                        counter = 1
                                else:
                                    # TODO: if tmp_chunking_rule_list[0]["type"] != tmp_chunking_rule_list2[0]["components"][0], then?
                                    pass
                        else:
                            tmp_chunking_rule_component_index -= 1
                    else:
                        if len(tmp_chunking_rule_list) != 0:
                            # TODO: len(tmp_chunking_rule_list) == 1 or not?
                            tmp_chunking_rule_list2 = [tmp_chunking_rule_list[0]]
                            tmp_chunking_rule_component_index = -1
                            tmp_chunking_rule_list = []
                            for chunking_rule in chunking_rule_list:
                                if token["upos"] == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                    tmp_chunking_rule_list.append(chunking_rule)
                                if token["upos"] == "nx" and "NP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                    tmp_chunking_rule_list.append(chunking_rule)
                                if token["upos"] == "vx" and "VP" == chunking_rule["components"][tmp_chunking_rule_component_index]:
                                    tmp_chunking_rule_list.append(chunking_rule)
                            tmp_chunking_rule_component_index -= 1
                        else:
                            if len(tmp_chunking_rule_list2) == 0:
                                if len(chunk[chunk_token_index + 1:]) == 2:
                                    # TODO: like following else?
                                    chunk_detail1 = {"chunk": chunk[chunk_token_index + 1:chunk_token_index + 2],
                                                     "chunk_type": chunk[chunk_token_index + 1:chunk_token_index + 2][0]["upos"],
                                                     "core_word": chunk[chunk_token_index + 1:chunk_token_index + 2][0]}
                                    chunk_detail2 = {"chunk": chunk[chunk_token_index + 2:],
                                                     "chunk_type": chunk[chunk_token_index + 2:][0]["upos"],
                                                     "core_word": chunk[chunk_token_index + 2:][0]}
                                    chunk_list.insert(chunk_index + 1, chunk_detail1)
                                    chunk_list.insert(chunk_index + 2, chunk_detail2)
                                    chunk = chunk[:chunk_token_index + 1]
                                    chunk_list[chunk_index] = chunk
                                    tmp_chunking_rule_component_index = -1
                                    tmp_chunking_rule_list = []
                                    chunk_token_index = 0
                                    counter += 2
                                else:
                                    chunk_detail = {"chunk": chunk[chunk_token_index + 1:]}
                                    if chunking_rule_last_component == "":
                                        # TODO: chunking_rule_first_component == "" means len(chunk) == 1?
                                        chunk_detail["chunk_type"] = chunk[chunk_token_index + 1:][0]["upos"]
                                        chunk_detail["core_word"] = chunk[chunk_token_index + 1:][0]
                                    else:
                                        chunk_detail["chunk_type"] = chunking_rule_last_component
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
                                            for token in chunk:
                                                if token["upos"] == "vx":
                                                    chunk_detail["core_word"] = token
                                                    break
                                    chunk_list.insert(chunk_index + 1, chunk_detail)
                                    chunk = chunk[:chunk_token_index + 1]
                                    chunk_list[chunk_index] = chunk
                                    if len(child_chunk_list) != 0:
                                        # TODO: have other possibilities, then?
                                        del child_chunk_list[0]
                                        child_chunk_list = child_chunk_list[1:]
                                    tmp_chunking_rule_component_index = -1
                                    tmp_chunking_rule_list = []
                                    chunk_token_index = 0
                                    counter += 1
                chunk_token_index -= 1


def print_chunks(chunk_list):
    """
    Print Chunks.

    :param chunk_list: Chunk List.
    """
    for chunk_index, chunk in enumerate(chunk_list):
        print(chunk_index)
        print(chunk)
    print("\n")
