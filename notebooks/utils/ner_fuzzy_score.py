from thefuzz import fuzz
from collections import Counter

def fuzzy_overlap(y_true: list, y_pred: list, threshold=80):
    y_true_match = [False] * len(y_true)
    y_pred_match = [False] * len(y_pred)
    
    for true_idx, true_item in enumerate(y_true):
        for pred_idx, pred_item in enumerate(y_pred):
            if fuzz.partial_ratio(true_item.lower(), pred_item.lower()) >= threshold:
                y_true_match[true_idx] = True
                y_pred_match[pred_idx] = True

    return sum(y_true_match) / (len(y_true) + sum(not x for x in y_pred_match))

def score_record(y_true: dict, y_pred: dict):
    scores = dict()

    for entity_name, entity_values in y_true.items():
        scores[entity_name] = fuzzy_overlap(entity_values, y_pred.get(entity_name, []))

    return scores

def calculate_mean_score(y_true: list, y_pred: list):
    scores = Counter()
    occurrences = Counter()

    for true_dict, pred_dict in zip(y_true, y_pred):
        occurrences.update(true_dict.keys())
        scores.update(score_record(true_dict, pred_dict))
    
    # calculate entity-wise mean
    for key in scores.keys():
        scores[key] = scores[key] / occurrences[key]
    
    # calculate overall mean
    mean = sum(scores.values()) / len(scores)

    return mean, scores