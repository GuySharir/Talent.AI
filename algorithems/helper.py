# # george lo->('matt widmann', 6.464088833272981)
# import pandas as pd
#
# data = {}
# with open('data.txt') as file:
#     for line in file:
#         if line.startswith('\n'):
#             continue
#
#         tmp = line.strip()
#         who = line.split('-')[0]
#         dist = float(line.split(', ')[-1].split(')')[0])
#
#         if who not in data:
#             data[who] = [dist]
#         else:
#             data[who].append(dist)
#
# # print(data)
#
# cleand = {}
# mins = []
# maxs = []
# totals = []
# means = []
# for key in data:
#     tmp = data[key]
#     total = sum(tmp)
#     min_ = min(tmp)
#     max_ = max(tmp)
#     mean_ = total / len(tmp)
#
#     cleand[key] = {"total": total,
#                    "min": min_,
#                    "max": max_,
#                    "mean": mean_}
#     totals.append(total)
#     mins.append(min_)
#     maxs.append(max_)
#     means.append(mean_)
#
# # for key in cleand:
# #     print(f"{key}: ", cleand[key])
#
#
# print(min(cleand, key=lambda k: cleand[k]["total"]))
#
# print(cleand[min(cleand, key=lambda k: cleand[k]["total"])])
#
# print(max(cleand, key=lambda k: cleand[k]["total"]))
# print(cleand[max(cleand, key=lambda k: cleand[k]["total"])])
#
# # mins = pd.DataFrame(mins)
# # maxs = pd.DataFrame(maxs)
# # totals = pd.DataFrame(totals)
# # means = pd.DataFrame(means)
#
# tmp = pd.DataFrame.from_dict(data, orient='index')
# print(tmp.describe())
# # print(tmp)
#
# # print(t.describe())
# print(totals.describe())
# # print(mins)
# # print(maxs)
