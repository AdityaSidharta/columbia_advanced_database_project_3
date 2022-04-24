from collections import defaultdict
from itertools import combinations


def get_l1_itemset(transactions, minsupp):
    k1_itemset = []
    item_count = defaultdict(int)
    freq_itemset = dict()
    n_transaction = len(transactions)
    for transaction in transactions:
        for item in transaction:
            item_count[(item,)] = item_count[(item,)] + 1
    for key, value in item_count.items():
        supp = value / n_transaction
        if supp >= minsupp:
            k1_itemset.append([key[0]])
            freq_itemset[key] = supp
    return sorted(k1_itemset), item_count, freq_itemset


def get_lk_candidate(pruned_itemset, transactions, minsupp):
    k_itemset = []
    item_count = {}
    freq_itemset = {}
    k = len(pruned_itemset[0])
    for pruned in pruned_itemset:
        item_count[tuple(pruned)] = 0
    n_transaction = len(transactions)
    for transaction in transactions:
        if len(transaction) >= k:
            for comb in combinations(transaction, k):
                if comb in item_count:
                    item_count[comb] = item_count[comb] + 1
    for key, value in item_count.items():
        supp = value / n_transaction
        if supp >= minsupp:
            k_itemset.append(sorted(list(key)))
            freq_itemset[key] = supp
    return sorted(k_itemset), item_count, freq_itemset


def apriori_gen(k_itemset):
    candidate_itemset = set()
    for item1, item2 in combinations(k_itemset, 2):
        if item1[:-1] == item2[:-1]:
            if item1[-1] < item2[-1]:
                candidate_itemset.add(tuple(item1 + [item2[-1]]))
    candidate_itemset = list(candidate_itemset)
    return sorted([list(x) for x in candidate_itemset])


def prune(candidate_itemset, prev_itemset):
    k = len(prev_itemset[0]) + 1
    pruned_itemset = []
    for itemset in candidate_itemset:
        valid = True
        for combination in combinations(itemset, k - 1):
            if list(combination) not in prev_itemset:
                valid = False
        if valid:
            pruned_itemset.append(itemset)
    return pruned_itemset


def get_assoc_itemsets(lk_itemsets, minconf, item_count_dict, freq_itemsets, max_k):
    assoc_itemsets = dict()
    all_assoc_itemsets = dict()
    for k in range(2, max_k + 1):
        assoc_k_itemset = set()
        k_itemset = lk_itemsets[k]
        for itemset in k_itemset:
            for i in range(k):
                full = tuple(itemset)
                left, right = itemset[:i] + itemset[i + 1 :], itemset[i]
                assoc_k_itemset.add((tuple(full), tuple(left), right))
        for full, left, right in assoc_k_itemset:
            conf = item_count_dict[full] / item_count_dict[left]
            supp = freq_itemsets[full]
            all_assoc_itemsets[(left, right)] = conf
            if conf >= minconf:
                assoc_itemsets[(left, right)] = (conf, supp)
    return assoc_itemsets, all_assoc_itemsets


def get_frequent_itemsets(transactions, minsupp, minconf):
    freq_itemsets = dict()
    lk_itemsets = dict()
    item_count_dict = dict()
    k = 1
    k1_itemset, item_count, freq_itemset = get_l1_itemset(transactions, minsupp)
    if len(k1_itemset) == 0:
        raise ValueError("None of the k1-itemset is frequent")
    item_count_dict.update(item_count)
    freq_itemsets.update(freq_itemset)
    lk_itemsets[k] = k1_itemset
    prev_itemset = k1_itemset
    while len(prev_itemset) > 0:
        candidate_itemset = apriori_gen(prev_itemset)
        if len(candidate_itemset) == 0:
            break
        pruned_itemset = prune(candidate_itemset, prev_itemset)
        if len(pruned_itemset) == 0:
            break
        k_itemset, item_count, freq_itemset = get_lk_candidate(pruned_itemset, transactions, minsupp)
        item_count_dict.update(item_count)
        if len(k_itemset) != 0:
            k = k + 1
            freq_itemsets.update(freq_itemset)
            lk_itemsets[k] = k_itemset
        else:
            break
        prev_itemset = k_itemset
    assoc_itemsets, all_assoc_itemsets = get_assoc_itemsets(lk_itemsets, minconf, item_count_dict, freq_itemsets, k)
    return freq_itemsets, assoc_itemsets
