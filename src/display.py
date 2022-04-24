def format_freq_itemsets(freq_itemsets, minsupp):
    print("==Frequent itemsets (min_sup={:.1f}%)".format(minsupp * 100.0))
    with open('output.txt', 'w+') as f:
        f.write("==Frequent itemsets (min_sup={:.1f}%)\n".format(minsupp * 100.0))
    freq = [(k, v) for k, v in freq_itemsets.items()]
    freq.sort(key=lambda x: (x[1], x[0]), reverse=True)
    for k, v in freq:
        print("[{}], {:.1f}%".format(",".join(k), v * 100.0))
        with open('output.txt', 'a+') as f:
            f.write("[{}], {:.1f}%\n".format(",".join(k), v * 100.0))


def format_assoc_itemsets(assoc_itemsets, minconf):
    print("==High-confidence association rules (min_conf={:.1f}%)".format(minconf * 100.0))
    with open('output.txt', 'a+') as f:
        f.write("==High-confidence association rules (min_conf={:.1f}%)\n".format(minconf * 100.0))
    assoc = [(k, v) for k, v in assoc_itemsets.items()]
    assoc.sort(key=lambda x: (x[1][0], x[1][1], x[0]), reverse=True)
    for k, v in assoc:
        print("[{}] => [{}] (Conf: {:.1f}%, Supp: {:.1f}%)".format(",".join(k[0]), k[1], v[0] * 100.0, v[1] * 100.0))
        with open('output.txt', 'a+') as f:
            f.write("[{}] => [{}] (Conf: {:.1f}%, Supp: {:.1f}%)\n".format(",".join(k[0]), k[1], v[0] * 100.0, v[1] * 100.0))