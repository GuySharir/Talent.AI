# # from distance.DistanceData import ListDistanceData, NumDistanceData, StrDistanceData
# from old.DistanceData import NumDistanceData, StrDistanceData
# from old.DistEnum import ListDistMethod
# # from distance.ListsDistance import ListsDistance
#
#
# class DistanceStrFunctions:
#     """
#         - q2, calculate the categorical distance of two attribute values regarding the domain size that is obtained
#          heuristically.
#             * domain_size_z - represent the domain size for an attribute
#
#         - q3, calculate the distance of two value attribute (k) regarding their occurrence frequencies
#             in a given attribute k
#             * val1_frequency - represent the frequency of a value1 in  attribute k
#             * val2_frequency - represent the frequency of a value2 in  attribute k
#
#         - q10, calculates the distance of two values of attribute k in the data set, exploiting unsupervised
#          information (in our case)
#
#     """
#
#     def __init__(self, str_distance_data: StrDistanceData):
#         self.str_distance_data = str_distance_data
#
#     def q2(self) -> float:
#         if self.str_distance_data.domain_size >= 3:
#             return 1
#         elif 3 < self.str_distance_data.domain_size <= 10:
#             return 1 - (0.05 * (self.str_distance_data.domain_size - 3))
#         elif self.str_distance_data.domain_size > 10:
#             return 0.65 - (0.01 * (self.str_distance_data.domain_size - 10))
#
#     def q3(self) -> float:
#         if not self.str_distance_data.val1:
#             self.str_distance_data.val1 = 'null'
#         if not self.str_distance_data.val2:
#             self.str_distance_data.val2 = 'null'
#
#         min_freq = min(self.str_distance_data.value_frequency.items(), key=lambda x: x[1])[1]
#         print(f'q3; min frequency {min_freq}')
#         val1_frequency = self.str_distance_data.value_frequency.get(self.str_distance_data.val1)
#         val2_frequency = self.str_distance_data.value_frequency.get(self.str_distance_data.val2)
#         print(f'q3; val1 frequency {val1_frequency}')
#         print(f'q3; val2 frequency {val2_frequency}')
#         max_freq = max(val1_frequency, val2_frequency)
#         print(f'q3; max frequency {max_freq}')
#         dist = (abs(val1_frequency - val2_frequency) + min_freq) / max_freq
#
#         return dist
#
#     def q10(self) -> float:
#         print(f'equation q2 return value - {self.q2()}')
#         print(f'equation q3 return value - {self.q3()}')
#         q3result = self.q3()
#         q2result = self.q2()
#
#         if not q3result and not q2result:
#             return 0
#         elif not q3result and q2result:
#             return q2result
#         elif q3result and not q2result:
#             return q3result
#         else:
#             return max(q3result, q2result)
#
#     def q12(self) -> int:
#         if self.str_distance_data.instance_a[self.str_distance_data.attribute] == \
#                 self.str_distance_data.instance_b[self.str_distance_data.attribute]:
#             return 0
#         elif self.str_distance_data.instance_a[self.str_distance_data.attribute] != \
#                 self.str_distance_data.instance_b[self.str_distance_data.attribute]:
#             return 1
#
#
# class DistanceCatFunctions:
#     """
#         - calc_num_distance_q13,
#     """
#     def __init__(self, num_distance_data: NumDistanceData):
#         self.num_distance_data = num_distance_data
#
#     def calc_num_distance_q13(self) -> float:
#         print(f'numeric val1- {self.num_distance_data.val1} , val2- {self.num_distance_data.val2}')
#         if not self.num_distance_data.val1 or not self.num_distance_data.val2:
#             return 0
#         else:
#             return (self.num_distance_data.val1 - self.num_distance_data.val2) ** 2
#
#
# class DistanceNumStr:
#     @staticmethod
#     def distance_per_type(val_type: object, val1, val2, value_frequency: dict, domain_size: int, attribute: str,
#                           instance_a: dict = None, instance_b: dict = None,
#                           lists_dist_method: ListDistMethod = None) -> float:
#
#         # print("################################# New Attribute ########################################")
#         # print(f'attribute- {attribute}')
#         # print(f'value type- {val_type}')
#         # print(f'instanceA value - {val1}')
#         # print(f'instanceB value - {val2}')
#
#         # print(f'frequencies dictionary {value_frequency}')
#         # print(f'domain size {domain_size}')
#
#         if val_type == str:
#             str_data = StrDistanceData(val_type=val_type, val1=val1, val2=val2, value_frequency=value_frequency,
#                                        domain_size=domain_size, attribute=attribute, instance_a=instance_a,
#                                        instance_b=instance_b)
#             str_obj = DistanceStrFunctions(str_distance_data=str_data)
#             q10result = str_obj.q10()
#             q12result = str_obj.q12()
#             # print(f'q10 result {q10result}')
#             # print(f'q12 result {q12result}')
#             return (q10result * q12result) ** 2
#
#         elif val_type == float or val_type == int:
#             num_data = NumDistanceData(val_type=val_type, val1=val1, val2=val2, value_frequency=value_frequency,
#                                        domain_size=domain_size, attribute=attribute)
#             num_obj = DistanceCatFunctions(num_distance_data=num_data)
#             q13result = num_obj.calc_num_distance_q13()
#             print(f'q13 result {q13result}')
#             return q13result
#
#         # elif val_type == list:
#         #     list_data = ListDistanceData(val_type=val_type, list1=val1, list2=val2, value_frequency=value_frequency,
#         #                                  domain_size=domain_size, attribute=attribute,
#         #                                  lists_dist_method=lists_dist_method)
#         #     list_dist_obj = ListsDistance(list_data)
#         #     list_dist_result = list_dist_obj.calc_dist()
#         #     print(f'list distance result {list_dist_result}')
#         #     return list_dist_result
#
#
# if __name__ == '__main__':
#     pass
#
#
