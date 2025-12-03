# # config.py
# _RULE_B = [False]*9
# _RULE_S = [False]*9

# _RULE_B[3] = True
# _RULE_S[2] = True; _RULE_S[3] = True
# preset_count = 0
# rule_update = True

# def get_rule_upd():
#     return rule_update

# def set_relu_upd_false():
#     global rule_update
#     rule_update = False

# def set_val_of_rule(S_B, n, val=False):
#     global _RULE_B, _RULE_S, rule_update
#     # Проверяем границы массива
#     if 0 <= n < len(_RULE_B) and 0 <= n < len(_RULE_S):
#         if S_B:
#             _RULE_B[n] = not _RULE_B[n]
#         else:
#             _RULE_S[n] = not _RULE_S[n]
#         rule_update = True
#     else:
#         print(f"   >>   Error: Invalid rule index {n} (must be 0-8)")

# sosed_count = 8

# def set_rule_from_preset(preset_i):
#     global _RULE_B, _RULE_S, rule_update
#     # Проверяем допустимый индекс пресета
#     if preset_i >= 1 and preset_i <= preset_count:
#         _RULE_B = preset[preset_i]["B"].copy()
#         _RULE_S = preset[preset_i]["S"].copy()
#         rule_update = True
#     else:
#         print(f"   >>   Error: Invalid preset index {preset_i} (must be 1-{preset_count})")

# def build_preset(preset):
#     global preset_count
#     preset_count = 0
#     for key in preset.keys():
#         item = preset[key]
#         matrix_b = [False]*9
#         if "B" in item and len(item["B"]) > 0:
#             for num in item["B"]:
#                 if 0 <= num < 9:  # Проверяем границы
#                     matrix_b[num] = True
#         item["B"] = matrix_b
        
#         matrix_s = [False]*9
#         if "S" in item and len(item["S"]) > 0:
#             for num in item["S"]:
#                 if 0 <= num < 9:  # Проверяем границы
#                     matrix_s[num] = True
#         item["S"] = matrix_s
#         preset_count += 1

# preset = {
#     1: {"name": "Game of Life", "B": [3], "S": [2, 3]},
#     2: {"name": "HighLife", "B": [3, 6], "S": [2, 3]},
#     3: {"name": "DryLife", "B": [3, 7], "S": [2, 3]},
#     4: {"name": "34 Life", "B": [3, 4], "S": [3, 4]},
#     5: {"name": "Day & Night", "B": [3, 6, 7, 8], "S": [3, 4, 6, 7, 8]},
#     6: {"name": "Life without Death", "B": [3], "S": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
#     7: {"name": "Seeds", "B": [3], "S": []},
#     8: {"name": "B25/S4", "B": [2, 5], "S": [4]},
#     9: {"name": "Live Free or Die", "B": [2], "S": [0]},
#     10: {"name": "Replicator", "B": [1, 3, 5, 7], "S": [1, 3, 5, 7]},
#     11: {"name": "Diamoeba", "B": [3, 5, 6, 7, 8], "S": [5, 6, 7, 8]},
#     12: {"name": "2x2", "B": [3, 6], "S": [1, 2, 5]},
#     13: {"name": "Morley", "B": [3, 6, 8], "S": [2, 4, 5]},
#     14: {"name": "H-trees", "B": [1], "S": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
#     15: {"name": "Anneal", "B": [4, 6, 7, 8], "S": [3, 5, 6, 7, 8]},
#     16: {"name": "Amoeba", "B": [5, 6, 7, 8], "S": [4, 5, 6, 7, 8]},
#     17: {"name": "Maze", "B": [3, 6, 8], "S": [2, 4, 5]},
#     18: {"name": "Mazectric", "B": [3], "S": [1, 2, 3, 4]},
#     19: {"name": "DotLife", "B": [3], "S": [0, 2, 3]},
#     20: {"name": "LowLife", "B": [3], "S": [1, 3]},
#     21: {"name": "Gems", "B": [3, 4, 5, 7], "S": [4, 5, 6, 8]},
#     22: {"name": "Corrosion of Conformity", "B": [3], "S": [1, 2, 4]},
#     23: {"name": "AntiLife", "B": [0, 1, 2, 3, 4, 7, 8], "S": [0, 1, 2, 3, 4, 6, 7, 8]},
#     24: {"name": "Stains", "B": [4, 5, 6, 7], "S": [1, 4, 5, 6]},
#     25: {"name": "Bacteria", "B": [4, 6, 8], "S": [2, 4, 5]},
#     26: {"name": "Assimilation", "B": [4, 5, 6, 7], "S": [3, 4, 5]},
#     27: {"name": "Coagulations", "B": [2, 3, 5, 6, 7, 8], "S": [3, 7, 8]},
#     28: {"name": "Coral", "B": [4, 5, 6, 7, 8], "S": [3]},
#     29: {"name": "Flakes", "B": [3], "S": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
#     30: {"name": "Long life", "B": [5], "S": [3, 4, 5]},
#     31: {"name": "Move", "B": [3, 6, 8], "S": [2, 4, 5]},
#     32: {"name": "Pseudo life", "B": [2, 3, 8], "S": [3, 5, 7]},
#     33: {"name": "Serviettes", "B": [], "S": [2, 3, 4]},
#     34: {"name": "WalledCities", "B": [2, 3, 4, 5], "S": [4, 5, 6, 7, 8]},
#     35: {"name": "a points", "B": [0, 4, 5], "S": [0, 1]},
#     36: {"name": "a circle", "B": [2, 5, 6, 7, 8], "S": [3, 4, 5, 6, 7]},
#     37: {"name": "a circle2", "B": [2, 5, 6, 7, 8], "S": [1, 2, 3, 4, 5, 6]}
# }

# build_preset(preset)

# # Экспортируем правила для импорта
# def get_rules():
#     return _RULE_B.copy(), _RULE_S.copy()