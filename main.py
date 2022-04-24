import fire

from src.algorithm import get_frequent_itemsets
from src.display import format_freq_itemsets, format_assoc_itemsets


def read_csv(dataset_name):
    transactions = []
    with open(dataset_name, "r") as f:
        for i, line in enumerate(f):
            transactions.append(line.strip().split(","))
    return transactions


def main(dataset_name, minsupp, minconf):
    transactions = read_csv(dataset_name)
    freq_itemsets, assoc_itemsets = get_frequent_itemsets(transactions, minsupp, minconf)
    format_freq_itemsets(freq_itemsets, minsupp)
    format_assoc_itemsets(assoc_itemsets, minconf)


if __name__ == "__main__":
    fire.Fire(main)
