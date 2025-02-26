# -*- coding: utf-8 -*-
import os
import itertools
from collections import defaultdict


class solution:
    def __init__(self, min_support=100):
        """
        Initializes class variables.
        """
        self.min_support = min_support
        self.transactions = []
        self.frequent_items = {}
        self.frequent_pairs = {}
        self.frequent_triples = {}
        self.pair_confidence_list = []
        self.triple_confidence_list = []

    def load_data(self, file_path):
        """
        Load transaction data from the given file path and storing them in self.transactions
        """
        apriori.load_data("browsing.txt")
        with open("CISC483-HW2-4\browsing.txt", "r") as f:
            for line in f:
                items = line.strip().split()
                if items:
                    self.transactions.append(set(items))
    
        return self

    def count_items(self):
        """
        Count individual item occurrences and stores the frequent items in self.frequent_items.
        """
        for transaction in self.transactions:
            for item in transaction:
                item_counts[item] += 1

        item_counts = defaultdict(int)
        for item in self.transactions:
          for item in transaction:
            item_counts[item] += 1
        self.frequent_items = {item: count for item, count in item_counts.items() if count >= self.min_support}

        return self

    def generate_frequent_pairs(self):
        """
        Generate frequent pairs from the transactions and stores the frequent pairs in self.frequent_pairs.
        """
        pair_counts = defaultdict(int)
        freq_items_set = set(self.frequent_items.keys())
        for transaction in self.transactions:
            items = sorted(transaction.intersection(freq_items_set))
            for pair in itertools.combinations(items, 2):
                pair_counts[pair] += 1

        self.frequent_pairs = {pair: count for pair, count in pair_counts.items()
                               if count >= self.min_support}

        return self

    def generate_frequent_triples(self):
        """
        Generate frequent triples from the transactions and stores the frequent triples in self.frequent_triples.
        """
        triple_counts = defaultdict(int)
        freq_items_set = set(self.frequent_items.keys())
        for transaction in self.transactions:
            items = sorted(transaction.intersection(freq_items_set))
            for triple in itertools.combinations(items, 3):
                if ((triple[0], triple[1]) in self.frequent_pairs and
                    (triple[0], triple[2]) in self.frequent_pairs and
                    (triple[1], triple[2]) in self.frequent_pairs):
                    triple_counts[triple] += 1
        self.frequent_triples = {triple: count for triple, count in triple_counts.items()
                                 if count >= self.min_support}

        return self

    def compute_pair_confidence(self):
        """
        Compute confidence for each frequent pair and store in self.pair_confidence_list.
        """
        self.pair_confidence_list = []
        for (a, b), pair_support in self.frequent_pairs.items():
            conf_ab = pair_support / self.frequent_items[a]
            conf_ba = pair_support / self.frequent_items[b]
            self.pair_confidence_list.append((a, b, conf_ab))
            self.pair_confidence_list.append((b, a, conf_ba))
        self.pair_confidence_list.sort(key=lambda x: (-x[2], x[0], x[1]))

        return self

    def compute_triple_confidence(self):
        """
        Compute confidence for each frequent triple and store in self.triple_confidence_list.
        """
        self.triple_confidence_list = []
        for triple, triple_support in self.frequent_triples.items():
            a, b, c = triple
            
            if (a, b) in self.frequent_pairs:
                conf_ab = triple_support / self.frequent_pairs[(a, b)]
                self.triple_confidence_list.append(((a, b), c, conf_ab))
            
            if (a, c) in self.frequent_pairs:
                conf_ac = triple_support / self.frequent_pairs[(a, c)]
                self.triple_confidence_list.append(((a, c), b, conf_ac))
            
            if (b, c) in self.frequent_pairs:
                conf_bc = triple_support / self.frequent_pairs[(b, c)]
                self.triple_confidence_list.append(((b, c), a, conf_bc))
       
        self.triple_confidence_list.sort(key=lambda x: (-x[2], x[0], x[1]))


        return self

    def eval(self, input_str) -> str:
        """
        Returns the confidence and rank for a rule in the format specified in the pdf. You will have to write the return statement in additio to the code here.
        """
        if len(input_str) == 16:
            lhs = input_str[:8]
            rhs = input_str[8:16]
            for idx, (l, r, conf) in enumerate(self.pair_confidence_list):
                if l == lhs and r == rhs:
                    rank = idx + 1
                    return f"{conf} , {rank}"
            return "NA"

        elif len(input_str) == 24:
            item1 = input_str[:8]
            item2 = input_str[8:16]
            # The left-hand side is the sorted pair of the two items.
            lhs_tuple = tuple(sorted([item1, item2]))
            rhs = input_str[16:24]
            for idx, (lhs, r, conf) in enumerate(self.triple_confidence_list):
                if lhs == lhs_tuple and r == rhs:
                    rank = idx + 1
                    return f"{conf} , {rank}"
            return "NA"
        else:
            return "NA"

    def sanity_check(self):
        """
        Performs sanity checks:
        (1) Verify that the number of frequent items (L1) after the first pass is 647.
        (2) Ensure that the top 5 pairs produced have confidence scores greater than 0.985.
        """
        check1 = (len(self.frequent_items) == 647)
        check2 = True
        if len(self.pair_confidence_list) < 5:
            check2 = False
        else:
            for i in range(5):
                if self.pair_confidence_list[i][2] <= 0.985:
                    check2 = False
                    break
        if check1 and check2:
            return "Sanity Check Passed"
        else:
            return "Sanity Check Failed"

if __name__ == "__main__":
    apriori = solution(min_support=100)

    # Load and process data
    apriori.load_data("browsing.txt") \
        .count_items() \
        .generate_frequent_pairs() \
        .generate_frequent_triples() \
        .compute_pair_confidence() \
        .compute_triple_confidence()

    # Test a sample rule
    test_rule = "ELE12951FRO40251"
    print(apriori.eval(test_rule))