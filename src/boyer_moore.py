def get_shift_match_table(P):
    m = len(P)
    shift_match_table = {}

    for shift in range(m - 1, 0, -1):
        p_1 = m - 1
        p_2 = m - shift - 1

        while p_2 >= 0:
            if P[p_2] == P[p_1]:
                p_1 -= 1
                p_2 -= 1
                if p_2 < 0:
                    shift_match_table[shift] = m - shift
                    break
            else:
                shift_match_table[shift] = m - shift - p_2 - 1
                break
    shift_match_table[m] = 0
    return shift_match_table

def get_good_suffix_table(P):
    m = len(P)

    good_suffix_table = {}
    good_suffix_table[0] = 1

    shift_match_table = get_shift_match_table(P)

    for i in range(1, m + 1):
        good_suffix_table[i] = i + m

    for i in range(m, 0, -1):
        if shift_match_table[i] > 0:
            good_suffix_table[shift_match_table[i]] = i + shift_match_table[i]

    for i in range(m, 0, -1):
        if shift_match_table[i] + i == m:
            for j in range(shift_match_table[i] + 1, m+1):
                good_suffix_table[j] = min(good_suffix_table[j], j + i)
    return good_suffix_table

def get_bad_char_table(P):
    last_indices = {}
    bad_char_table = [-1]*len(P)
    for i, v in enumerate(P):
        if v in last_indices:
            bad_char_table[i] = last_indices[v]
        last_indices[v] = i
    return bad_char_table

def boyer_moore_search(T, P):
    P_len = len(P)
    T_len = len(T)

    occurrences = []
    bad_char_table = get_bad_char_table(P)
    good_suffix_table = get_good_suffix_table(P)

    shift = 0
    while shift <= T_len-P_len:
        j = P_len-1

        while j >= 0 and P[j] == T[shift+j]: # Read backwards across pattern until mismatch
            j -= 1
        
        if j < 0: # Match
            occurrences.append(shift)
            shift += good_suffix_table[0]
        else: # Mismatch
            potential_bad_char_add = j-bad_char_table[j] if bad_char_table[j] >= 0 else -1
            potential_good_suffix_add = max(1, good_suffix_table[j]-j-1)
            shift += max(potential_bad_char_add, potential_good_suffix_add)
    
    return occurrences
