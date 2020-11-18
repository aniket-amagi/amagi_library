#!/usr/bin/python3
# coding= utf-8
import re

sample_rule = [
    {
        "Type": {
            "match_type": "exact",
            "values": ["", ""],
            "invert": False
        },
        "Asset Id": {
            "match_type": "regex",
            "patterns": [],
            "values": ["", ""],
            "invert": False
        },
        "Time": {
            "match_type": "range",
            "start": "",
            "end": "",
            "invert": False
        },
        "Owner": "Amagi"
    }
]


class Matcher(object):

    def __init__(self, rules):
        self.rules = rules

    def iterable(self, obj):
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return isinstance(obj, str)

    def is_matching_rule(self, rule, asset, asset_key):
        matched = False
        if rule[asset_key]["match_type"] == "exact":
            matched = (asset[asset_key] in rule[asset_key]["values"]) ^ rule[asset_key]["invert"]
        elif rule[asset_key]["match_type"] == "regex":
            pattern_matched = False
            for pattern_str in rule[asset_key]["patterns"]:
                pattern = re.compile(pattern_str)
                if pattern.match(asset[asset_key]):
                    pattern_matched = True
            matched = pattern_matched ^ rule[asset_key]["invert"]
        elif rule[asset_key]["match_type"] == "range":
            matched = (rule[asset_key]["start"] <= asset[asset_key] <= rule[asset_key]["end"]) ^ rule[asset_key][
                "invert"]
        else:
            matched = False
        return matched

    def match(self, asset, return_key):
        matched = False
        for rule in self.rules:
            for asset_key in asset:
                if asset_key in rule and asset_key != return_key:
                    matched = self.is_matching_rule(rule, asset, asset_key)
                    if not matched:
                        break
            if matched:
                return rule[return_key]
