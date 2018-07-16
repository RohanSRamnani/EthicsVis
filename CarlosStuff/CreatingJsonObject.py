import lxml
import nltk
import json
from progressbar import ProgressBar
from bs4 import BeautifulSoup
from urllib.parse import urlparse

pbar = ProgressBar()
search_dict = {}

#Starts by turning the HTML entry into a BeautifulSoup
#Returns that soup object
def make_soup() -> 'beautiful soup object':
	with open("Takeout/My Activity/Search/MyActivity.html", encoding='utf-8') as f:
		print("Making your soup! This may take a moment...")
		soup = BeautifulSoup(f, 'lxml') #beautiful soup is slower than using just lxml,
										# but using lxml is faster than html.parser
		print("Soup complete! Thanks for waiting.")
		return soup

#Finds every entry in the HTMl document by finding the container that holds each entry.
#Returns a list of all those containers.
def find_entries(soup) -> list:
	print('Now finding all entries! This may take a moment...')
	entry_list = soup.findAll("div", {"class": "outer-cell mdl-cell mdl-cell--12-col mdl-shadow--2dp"})
	print('Found them all! Thanks for waiting.')
	return entry_list

#This is the main function that does most of the heavy lifting.
#Iterates through the list of entry dividers and gets the
#search query, tokenizes it, gets the lat and lon, and creates and writes to the JSON file.
def parse_entries(entry_list):
	print('Now parsing those entries! This may take a moment...')
	for entry in pbar(entry_list):
		try:
			search_area = entry.find("div", {"class": "content-cell mdl-cell mdl-cell--6-col mdl-typography--body-1"})
			action_string = search_area.contents[0] #Many of the entries aren't searches, so this filters those out.
			if action_string.startswith('Searched'):
				location_section = entry.find("div", {"class": "content-cell mdl-cell mdl-cell--12-col mdl-typography--caption"})

				datetime = search_area.contents[-1] #grabbing the date by getting the last item in the search area
				search_query = search_area.a.contents[0] #grabbing the query by getting the first item in the search area
				search_tokens = tokenize_entry(search_query) #turning the query into a tokenized list
				location_URL = urlparse( location_section.find("a").contents[0] ) #here we get the URL for the location
				lonlat = get_latlon(location_URL.query) #sending just the query fragment to physically retrieve the string literals from it

				create_JSON(search_tokens, search_query, lonlat, datetime) #takes all above data and builds the JSON dict

		except AttributeError:
			pass #skipping over any rogue entries that don't have lonlat or time data.


	with open('SearchActivityTokenized.json', 'w') as outfile:
		json.dump(search_dict, outfile)
	print("Parsing complete! Your .json file can be found " +
	      "in the root folder under the name SearchActivityTokenized.json.\n" +
	      "Thanks for your patience!")

#This can be used to print out the data, but there are too many entries to be useful mostly.
#			for k, v in sorted(search_dict.items(), key = lambda x : x[1]['Times searched']):
#				print(k, '->', v)

#helper function that takes the query and returns a list of the search words inside
def tokenize_entry(search_query):
	search_tokens = nltk.word_tokenize(search_query)
	return search_tokens

#helper functon that splits the lat,lon from the URL and returns it as lon,lat for d3's use.
def get_latlon(latlon_query):
	latlon_query = latlon_query[2:]
	lat, lon = latlon_query.split(',')
	return [lon, lat]

#function that builds the dictionary for each word in the tokenized list.
#it checks to see if the word already exists in the dictionary, otherwise
#it creates an entry for it.
#this way multiple entries can be iterated through with a single index number.
#For example search_dict["google"][0] was the first time we found it, and [0] across
#all of the subdicts will give the time, date, and location of the first time you searched it.
#then [1] does the next, and so on.
def create_JSON(search_tokens, search_query, lonlat, datetime):
	with open("stop_words.txt") as f:
		stop_words = f.read().split("\n")
		for word in search_tokens:
			if word not in stop_words:
				if word in search_dict:
					search_dict[word]['Times searched'] += 1
					search_dict[word]['Date & time'].append(datetime)
					search_dict[word]['Longitude'].append(lonlat[0])
					search_dict[word]['Latitude'].append(lonlat[1])
				else:
					search_dict[word] = {
						'Search term': word,
						'Times searched': 1,
						'Date & time': [datetime],
						'Longitude': [lonlat[0]],
						'Latitude': [lonlat[1]]}




if __name__ == '__main__':
	print("Generating a JSON dict from MyActivity.html")
	soup = make_soup()
	entry_list = find_entries(soup)
	parse_entries(entry_list)