good_keywords = [
    "disaster", "floods", "flood", "earthquake", "tsunami", 
    "cyclone", "hurricane", "wildfire", "avalanche",
    "drought", "tornado", "landslide"
]

error_keywords = [
    "BJP", "Bharatiya Janata Party", "BSP", "Bahujan Samaj Party",
    "CPI", "Communist Party of India", "CPM", "Communist Party of India (Marxist)",
    "INC", "Indian National Congress", "NCP", "Nationalist Congress Party",
    "AIFB", "All India Forward Bloc", "DMDK", "Desiya Murpokku Dravida Kazhagam",
    "INLD", "Indian National Lok Dal", "IUML", "Indian Union Muslim League",
    "JD(U)", "Janata Dal (United)", "JKNPP", "Jammu & Kashmir National Panthers Party",
    "LJP", "Lok Jan Shakti Party", "RLD", "Rashtriya Lok Dal", "SAD", 
    "Shiromani Akali Dal", "SHS", "Shivsena", "SP", "Samajwadi Party", 
    "Aa S P", "Asankhya Samaj Party", "AAAP", "Aam Aadmi Party", 
    "AACP", "Adarshwaadi Congress Party", "ABHM", "Akhil Bharat Hindu Mahasabha",
    "ABSPARTY", "Akhil Bhartiya Sudhar Party", "ABVCP", "Akhil Bhartiya Vikas Congress Party",
    "AIBS", "All India Bahujan Samman Party", "AICP", "New All India Congress Party",
    "ANC", "Ambedkar National Congress", "AP", "Awami Party", 
    "ATBP", "Atulya Bharat Party", "AVIRP", "AARAKSHAN VIRODHI PARTY", 
    "BASMM", "Bahujan Samaj Mukti Morcha", "BASPB", "Bahujan Smajwadi Party (Baba Saheb)"
]


def train(text):
	for word in error_keywords:
		if word.lower() in text.lower():
			return []

	filtered_articles = []

	for word in good_keywords:
		if word.lower() in text.lower():
			filtered_articles.append(text)
			break 

	return filtered_articles

