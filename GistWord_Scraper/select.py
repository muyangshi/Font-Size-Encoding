import json

bad_topics = ["A_Treasure_Trove_(or_Laundry_List)_of_Awesome_Alliterations",
				"Adjectives",
				"Adjectives_Describing_People_and_Personal_Qualities_—",
				"Adverbs",
				"April_Fools_Day",
				"Chinese_New_Year",
				"Christmas_(Secular)",
				"Columbus_Day",
				"Common_Opposites___Antonyms",
				"Compound_Words",
				"Conjunctions_(and_Subordinating_Conjunctions)",
				"Container",
				"Dolch_Words_List",
				"Famous_and_Common_Duos",
				"Food_Web___Food_Chain",
				"Friends__Acquaintances__and_Other_People_—",
				"Good_Luck_Symbols_from_Many_Cultures_—",
				"Grammar_Related_Terms",
				"Groundhog_Day",
				"Interjections",
				"Irregular_Verbs_in_English",
				"Job_and_Occupation",
				"Legal_Terms",
				"Long_E",
				"Long_U_+_Long_OO_Words",
				"Martin_Luther_King__Jr_",
				"Mothers_Day",
				"Negative",
				"New_Years",
				"Positive_Words_List",
				"Prepositions",
				"Pronouns",
				"Regular_Verbs__",
				"St_Patricks_Day",
				"Thanksgiving",
				"Types_of_Dances_—",
				"Types_of_Leaders",
				"Types_of_Rooms",
				"US_Constitution",
				"US_Flag_Day",
				"US_States_(plus_DC)",
				"Valentines_Day",
				"Verbs__",
				"Ways_to_say_Big__",
				"Ways_to_say_Many__",
				"Ways_to_Say_Said",
				"Words_That_Are_Both_Nouns_And_Verbs",
				"Yard_and_Backyard"]

good_topics = {}

with open('dict.json') as json_file:
	mywords = json.load(json_file)
	for topic in mywords:
		if topic not in bad_topics:
			good_topics[topic] = mywords[topic]

good_json_file = json.dumps(good_topics)
f = open("good_dict.json","w")
f.write(good_json_file)
f.close()