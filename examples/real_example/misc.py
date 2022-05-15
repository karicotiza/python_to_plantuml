# import cld2
# import operator
#
# # dictionary_with_transcriptions = {
# #     'english': 'patomany wigilans o the ber who st shaisium',
# #     'russian': 'потом они видели что наверху настоящеесзм'
# # }
#
# dictionary_with_transcriptions = {
#     'english': 'it has o accupnet signal of katoro parhode chiris filter informi rot reaction',
#     'russian': 'сигналы это совокупность сигналов которую проходит через фильтры и формируют реакцию'
# }
#
# results = {}
# for key, value in dictionary_with_transcriptions.items():
#     detection = cld2.detect(value)
#     print(detection)
#     results[key] = detection[2][0][2]
#
# # print(results)
#
# language = max(results.items(), key=operator.itemgetter(1))[0]
# # print(language)
#
# # language = max(result, key=result.get())[0]
# # print(language)
# print(language, dictionary_with_transcriptions[language])