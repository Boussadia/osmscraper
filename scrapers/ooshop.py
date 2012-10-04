#!/usr/bin/python
# -*- coding: utf-8 -*-

from osmscraper import OSMScraper

class Ooshop_parser(OSMScraper):
	"""
		Parser for Online SuperMarket Ooshop.com
	"""
	def __init__(self):
		super(Ooshop_parser, self).__init__("http://www.ooshop.com/courses-en-ligne")
		

	def get_menu(self):
		parsed_page = self.get_parsed_page_for_url()
		a_main_menu = parsed_page.find_all("a",{"class":re.compile("univ(\d){1}")})
		li_sub = parsed_page.find(id="navh").find_all("li")
		print "Main menu contains "+str(len(a_main_menu))+" categories."
		categories = {}

		for i in xrange(0,len(li_sub)):
			li = li_sub[i]
			a_main_cats = li.find_all("a",{"class":re.compile("univ(\d){1}")})
			if len(a_main_cats)>0:
				a = a_main_cats[0]
				categories[a.get("class")[0]] = {
					'url':a.get("href"),
					'name': a.findAll(text=True)[0],
					'sub_categories':{}
				}

				sub_cats = li.find("div").find_all("a")

				print "Found "+str(len(sub_cats))+" sub categories for main category "+categories[a.get("class")[0]]["name"]
				
				for j in xrange(0, len(sub_cats)):
					print "Found category "+sub_cats[j].findAll(text=True)[0][2:]
					sub_category = {
						"url" : sub_cats[j].get("href"),
						'name' : sub_cats[j].findAll(text=True)[0][2:],
						'sub_categories':{}
					}
					categories[a.get("class")[0]]["sub_categories"][j] = sub_category

		self.set_categories(categories)

	def get_sub_menu(self):
		categories = self.get_categories()
		

		for key in categories:
			sub_category = categories[key]["sub_categories"]
			
			print "Processing main catagory : "+categories[key]["name"]

			for sub_key in sub_category:
				print "Processing sub catagory level 1 : "+sub_category[sub_key]["name"]
				url_sub_category = sub_category[sub_key]["url"]
				sub_category_level_2 = self.get_sub_menu_level_2_for_url(url_sub_category)

				print "Found "+str(len(sub_category_level_2))+" level 2 sub categories "

				for last_sub_key in sub_category_level_2:
					print "Processing sub catagory level 2 : "+sub_category_level_2[last_sub_key]["name"]

					url_sub_category_level_2 = sub_category_level_2[last_sub_key]["url"]
					sub_category_level_3 = self.get_sub_menu_level_3_for_url(url_sub_category_level_2)

					print "Found "+str(len(sub_category_level_3))+" level 3 sub categories."
					for sub in sub_category_level_3:
						print sub_category_level_3[sub]["name"]

					sub_category_level_2[last_sub_key]["sub_categories"] = sub_category_level_3

				sub_category[sub_key]["sub_categories"] = sub_category_level_2

			categories[key]["sub_categories"] = sub_category

		self.set_categories(categories)


	def get_sub_menu_level_2_for_url(self, url):
		id_sub_level = "ctl00_cphC_ns_rpFilTab_ctl01_ucBns_p1";
		return self.get_sub_menu_for_url(url, id_sub_level)

	def get_sub_menu_level_3_for_url(self, url):
		id_sub_level = "ctl00_cphC_ns_rpFilTab_ctl02_ucBns_p1";
		return self.get_sub_menu_for_url(url, id_sub_level)


	def get_sub_menu_for_url(self, url, id_sub_level):
		parsed_page = self.get_parsed_page_for_url(url)
		print parsed_page.find(id="body").find_all("div", {"class","body"})

		if parsed_page.find(id=id_sub_level) is not None:
			html_sub_categories = parsed_page.find(id=id_sub_level).find_all("a")
			sub_categories = {}
			for a in html_sub_categories:
				str_to_search = a.get("onclick")
				reg = re.compile("'(.)*','(.)*'")
				match = reg.search(str_to_search)
				eventTarget = match.group(0).split("'")[1]
				eventArgument = match.group(0).split("'")[3]

				sub_categories[a.get("id")] = {
					"url_parent": url,
					"url" : a.get("href"),
					"name" : a.findAll(text=True)[0],
					"eventTarget": eventTarget,
					"eventArgument": eventArgument,
					"form": parsed_page.find(id="aspnetForm"),
				}
			return sub_categories
		else:
			return {}

	def get_sub_menu_for_html(self, parsed_page, id_sub_level):
		# parsed_page = self.get_parsed_page_for_url(url)
		if parsed_page.find(id=id_sub_level) is not None:
			html_sub_categories = parsed_page.find(id=id_sub_level).find_all("a")
			sub_categories = {}
			for a in html_sub_categories:
				str_to_search = a.get("onclick")
				reg = re.compile("'(.)*','(.)*'")
				match = reg.search(str_to_search)
				eventTarget = match.group(0).split("'")[1]
				eventArgument = match.group(0).split("'")[3]

				sub_categories[a.get("id")] = {
					"url_parent": url,
					"url" : a.get("href"),
					"name" : a.findAll(text=True)[0],
					"eventTarget": eventTarget,
					"eventArgument": eventArgument,
					"form": parsed_page.find(id="aspnetForm"),

				}
			return sub_categories
		else:
			return {}

	def __do_PostBack(self, eventTarget, eventArgument, form_parsed):
		values = {}
		inputs = form_parsed.find_all('input')
		url = form_parsed.get("action")
		# url = self.get_base_url()

		for i in xrange(0,len(inputs)):
			values[str(inputs[i].get('name'))] = str(inputs[i].get('value'))

		values["__EVENTTARGET"] = eventTarget
		values["__EVENTARGUMENT"] = eventArgument

		print len(values)

		print "Posting data to "+url

		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		
		page = response.read()
		print "Response fetched"
		parsed_page = BeautifulSoup(page)
		print parsed_page.prettify()

		return parsed_page