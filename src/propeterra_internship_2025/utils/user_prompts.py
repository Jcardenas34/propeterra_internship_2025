
''' Contains all predefined prompts for experimentation '''

# Used for Human gathered links that need to be formatted as a JSON
reformatting_prompt_1 = "Place these sources in .json format with the following keys 'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }]  Make sure the descriptions and information on the keys is accurate"

# First prototype link
user_prompt_1 = "Using the links provided below, can you provide __num_sources__ unique links for webpages with similar content for the country of __country_of_interest__?\n\n" \
"__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The links can have information that is in the county's native language, as well as in English. The links can contain information or have been written between \n" \
"the years 2016 and 2025. Please verify that the links you return are accessible. Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into."

# removes the ability to return results in native language
user_prompt_2 = "Using the links provided below, can you provide __num_sources__ unique links for webpages with similar content for the country of __country_of_interest__?\n\n" \
"__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The links can have information that is in the county's native language, __native_language__ as well as in English. The links can contain information or have been written between \n" \
"the years 2016 and 2025. Please verify that the links you return are accessible. Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into."

# Prompt has a more demanding tone
user_prompt_3 = "Provide __num_sources__ unique links for webpages that contain information about the real estate market for the country of __country_of_interest__\n" \
"The links should contain information on real estate trends, economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"how governmental factors could affect real estate such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The links can have information that is in the county's native language, __native_language__ as well as in English. The links can contain information or have been written between \n" \
"the years 2016 and 2025. Please verify that the links you return are accessible. Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. This is prompt number: __prompt_num__"

# Now includes prompt number
user_prompt_4 = "Using the links provided below, can you provide __num_sources__ unique links for webpages with similar content for the country of __country_of_interest__?\n\n" \
"__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The links can have information that is in the county's native language, as well as in English, and should not be shallow, explore the webpage for paths to relevant data and descriptions.\n" \
"The links can consist of but are not limited to articles, downloadable pdfs, pages containing downloadable csv files, pages with graphs or charts representing plotted data, and reports from official agencies.\n" \
"The information or have been written between the years 2016 and 2025. Please verify that the links you return are accessible, and do not return a 404 error or otherwise do not return any meaningful content. \n" \
"Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. This is prompt number: __prompt_num__"


# Now includes prompt number FAILURE, contradictory information apparently
user_prompt_5 = "Using the links provided below, can you provide __num_sources__ unique links for webpages with similar content for the country of __country_of_interest__?\n\n" \
"__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The goal here is to provide me with links to websites that have reliable open source APIs and portals where I will be able to ingest the data to update dash boards to make informed decisions. \n" \
"The links can have information that is in the country's native language, as well as in English, and should not be shallow, explore the webpage for paths to relevant data and descriptions.\n" \
"The links can consist of but are not limited to articles, downloadable pdfs, pages containing downloadable csv files, pages with graphs or charts representing plotted data, and reports from official agencies.\n" \
"The information or have been written between the years 2016 and 2025. Please verify that the links you return are accessible, and do not return a 404 error or otherwise do not return any meaningful content. \n" \
"Return your response in a JSON format where the links are categorized in according to data type, access, quality and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. This is prompt number: __prompt_num__"


# Now includes prompt number FAILURE, contradictory information apparently
user_prompt_6 = "Using the links provided below, can you search the web and provide __num_sources__ additional verified and live links for webpages similar to and or have similar content for the country of __country_of_interest__?\n\n" \
"__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. The goal here is to provide me with links to websites that have reliable open source APIs and portals where I will be able to ingest the data to update dash boards to make informed decisions. \n" \
"The links can have information that is in the country's native language, as well as in English, and should not be shallow, explore the webpage for paths to relevant data and descriptions.\n" \
"The links can consist of but are not limited to articles, downloadable pdfs, pages containing downloadable csv files, pages with graphs or charts representing plotted data, and reports from official agencies.\n" \
"The information or have been written between the years 2016 and 2025. Please verify that the links you return are accessible, and do not return a 404 error or otherwise do not return any meaningful content. \n" \
"Return your response in a JSON format where the links are categorized in according to data type, access, quality and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. If the instructions are unclear or you cannot source reliable data, please say so, and explain where you are having difficulty. This is prompt number: __prompt_num__"

# 
user_prompt_7 = "Using the links provided below as a starting point, search the web and provide __num_sources__ additional verified and live links for webpages with the same theme and or have similar content as the links provided for the country of __country_of_interest__?\n\n" \
"__links__\n\n Use the links provided as a starting point, and even use them as to look up and return information for the specified country. Your goal here is to gather links to relevant data sources for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
"governmental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
"and or region. Ideally you will provide me with links to websites that have reliable open source APIs and portals where I will be able to extract data from to create and update dash boards to make informed decisions about real estate. \n" \
"The links can have information that is in the country's native language, as well as in English, explore the webpages provided for paths to relevant data and descriptions as well as explore the web pages you provide for relevant data.\n" \
"The links should lead to, but are not limited to web scrape-able articles, downloadable PDFs, pages containing downloadable .CSV or XLM files, pages with graphs or charts representing plotted data that is extractable, and reports from official agencies such as the UN or national agencies or government pages from the country that is specified.\n" \
"The information should have been written between the years 2000 and 2025. For each link, attempt to open it and verify that it does not return an HTTP error (e.g., 404, 403, 500). Only return links that are live and accessible and return meaningful content related to the goal. \n" \
"Return your response in a JSON format where the links are categorized in according to data type, access, quality, how often data on these pages is refreshed, and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. If you cannot fulfill the request for any of the JSON fields, return NULL in the field, if the instructions are unclear or you cannot source reliable data, please say so, and explain where you are having difficulty. This is prompt number: __prompt_num__"

user_prompt_8 = "Using the links provided below as a starting point, search the web and provide __num_sources__ additional verified and live links for webpages with the same theme and or have similar content as the links provided for the country of __country_of_interest__?\n\n" \
"__links__\n\n Use the links provided as a starting point, and even use them as to look up and return information for the specified country. Your goal here is to gather links to relevant data sources for the real estate market that contain, but are not limited to metrics like home prices, home sales, mortgage rates, construction spending, expansion indices, and home ownership rate that give me an idea of the current and emerging state of the real estate market in the specified country. \n" \
"Return links only for the country of __country_of_interest__. I also care about governmental factors such as, policy and laws and regulation that could impact real estate market, as well as contact information for real estate professionals, and real estate tools that are used by professionals in the country \n" \
"and or region. Ideally you will provide me with links to websites that have reliable open source APIs and portals where I will be able to extract data from to create and update dash boards to make informed decisions about real estate. \n" \
"The links can have information that is in the country's native language, as well as in English, explore the webpages provided for paths to relevant data and descriptions as well as explore the web pages you provide for relevant data.\n" \
"The links should lead to, but are not limited to web scrape-able articles, downloadable .PDF, .CSV or XLM files, pages with graphs or charts representing plotted data that is extractable, and reports from official agencies such as the United Nations, national agencies or government pages from the country that is specified.\n" \
"The information should have been written between the years 2000 and 2025. For each link, attempt to open it and verify that it does not return an HTTP error (e.g., 404, 403, 500). Only return links that are live and accessible and return meaningful content related to the goal. \n" \
"Return your response in a JSON format where the links are categorized in according to data type, access, quality, how often data on these pages is refreshed, and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. If you cannot fulfill the request for any of the JSON fields, return NULL in the field, , \n" \
"if the instructions are unclear or you cannot source reliable data, say so, and explain where you are having difficulty. This is prompt number: __prompt_num__"

user_prompt_9 = "Search the web and provide __num_sources__ verified and live links for webpages with real estate related metrics for the country of __country_of_interest__?\n\n" \
"Your goal here is to gather links to relevant data sources for the real estate market that contain, but are not limited to metrics like home prices, home sales, mortgage rates, construction spending, expansion indices, and home ownership rate \n" \
"cash flow, net operating income, occupancy rate, vacancy rate, cap rate, number of days on market, housing need, appreciation, IRR, median house price, median rent price, affordability indicators, active listings, mortgage rates, and more that give me an idea of the current and emerging state of the real estate market in the specified country. \n" \
"Return links only for the country of __country_of_interest__. I also care about governmental factors such as, policy and laws and regulation that could impact real estate market. \n" \
"Ideally you will provide me with links to websites that have reliable open source APIs and portals where I will be able to extract data from to create and update dash boards to make informed decisions about real estate. \n" \
"The links can have information that is in the country's native language, as well as in English. Navigate the webpages you provide and search for pages to relevant data.\n" \
"The links should lead to, but are not limited to web scrape-able articles, downloadable .PDF, .CSV or .XLM files, pages with graphs or charts representing plotted data that is extractable, and reports from official agencies such as the United Nations, national agencies or government pages from __country_of_interest__.\n" \
"The information should have been written between the years 2000 and 2025. For each link, attempt to open it and verify that it does not return an HTTP error (e.g., 404, 403, 500). Only return links that are live and accessible and return meaningful content related to the goal. \n" \
"Return your response in a JSON format where the links are categorized in according to data type, access, quality, how often data on these pages is refreshed, and link, primarily, \n" \
"then use your judgement to create other json keys to categorize the data into. If you cannot fulfill the request for any of the JSON fields, return NULL in the field, , \n" \
"if the instructions are unclear or you cannot source reliable data, say so, and explain where you are having difficulty. Produce the json with the following keys \n" \
"'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }] \n" \
"This is prompt number: __prompt_num__"

user_prompt_10 = "Please retrieve links to 15 web pages that contain downloadable or web scape-able data that can be plotted to \n" \
"measure the state of the real estate market and trends. Examples of good metrics can range from GDP to poverty rate, and others. The links should be relevant \n" \
"only for the country of __country_of_interest__. Once you have retrieved the links, verify that they are valid links and lead to a page that actually exists. \n" \
"Please place these sources in .json format with the following keys 'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }] \n" \

user_prompt_11 = "Please retrieve links to __num_sources__ web pages that contain downloadable or web scape-able data that can be plotted to \n" \
"measure the state of the real estate market and trends. Examples of good metrics can range from GDP, poverty rate, average home prices, home sales per year, mortgage rates, construction spending, expansion indices, and home ownership rate \n" \
"cash flow, net operating income, occupancy rate, vacancy rate, cap rate, number of days on market, housing need, property appreciation, IRR, median house/property price, median rent price, affordability indicators, active listings, mortgage rates, and more that give me an idea of the current and emerging state of the real estate market in the country of __country_of_interest__. \n" \
"Web scrape-able articles, as well as downloadable PDFs and reports from official agencies such as the United Nations, national agencies or government pages from __country_of_interest__ as also good examples of resources you should return. \n"\
"The links should be relevant only for the country of __country_of_interest__. Once you have retrieved the links, verify that they are valid links and lead to a page that actually exists. \n" \
"Please place these sources in .json format with the following keys 'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }] \n" \

# Using a prompt with wording similar to Clemence, as well as other prompting techniques
user_prompt_12 = "Research and gather links to __num_sources__ web pages that contain downloadable or web scape-able data that can be plotted to \n" \
"measure the state of the real estate market and trends. Examples of good metrics you can return range from GDP, poverty rate, average home prices, home sales per year, mortgage rates, construction spending, expansion indices, and home ownership rate \n" \
"cash flow, net operating income, property occupancy rate, vacancy rate, cap rate, number of days properties are on the market, housing need, property appreciation, IRR, median and mean house/property price, median rent price, affordability indicators, active listings, mortgage rates,  \n" \
"and more that give me an idea of the current and emerging state of the real estate market in the country of __country_of_interest__. Information like real estate agents and corporations, property listing websites, population statistics, cost of living, traffic information, properties for sale and rent, \n" \
"letting agencies, currency exchange rates, interest rates, utility costs (electricity, fuel, water), water access, and population growth are also good information to return. \n" \
"Additionally, resources like web scrape-able articles, as well as downloadable PDFs and reports from official agencies such as the United Nations, national agencies or government pages from __country_of_interest__ are also good examples of resources you should return. Documents you return will be used train an LLM designed for the commercial real estate business. \n"\
"The links should be relevant only for the country of __country_of_interest__. If you cannot return links that are relevant tell me you cannot provide reliable links. If you need more information, ask for it, or use your tools, do not ever make up any links or return sources to invalid pages or information. \n" \
"Plan your answer step by step. Once you have collected links to __num_sources__ web pages place these sources in .json format with the following keys 'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }] \n" \

# Using a prompt with wording similar to Clemence, as well as other prompting techniques
user_prompt_13 = "Research and gather links to __num_sources__ web pages that contain downloadable or web scape-able data that can be plotted to \n" \
"measure the state of the real estate market and trends. Examples of good metrics you can return range from GDP, poverty rate, average home prices, home sales per year, mortgage rates, construction spending, expansion indices, and home ownership rate \n" \
"cash flow, net operating income, property occupancy rate, vacancy rate, cap rate, number of days properties are on the market, housing need, property appreciation, IRR, median and mean house/property price, median rent price, cost of living, affordability indicators, active listings, mortgage rates,  \n" \
"and more that give me an idea of the current and emerging state of the real estate market in the country of __country_of_interest__. \n" \
"Additionally, resources like web scrape-able articles, as well as downloadable PDFs and reports from official agencies such as the United Nations, national agencies or government pages from __country_of_interest__ are also good examples of resources you should return. Documents you return will be used train an LLM designed for the commercial real estate business. \n"\
"The links should be relevant only for the country of __country_of_interest__. If you cannot return links that are relevant tell me you cannot provide reliable links. If you need more information, ask for it, or use your tools, do not ever make up any links or return sources to invalid pages or information. \n" \
"Plan your answer step by step. Once you have collected links to __num_sources__ web pages place these sources in .json format with the following keys 'data_sources':[ {'name': '','link': '', 'data_type': '', 'access': '', 'quality': '', 'update_frequency': '', 'language':'','api_available':'', 'description': '' }] \n" \



user_prompt_dictionary = {
                            1:user_prompt_1,
                            2:user_prompt_2,
                            3:user_prompt_3,
                            4:user_prompt_4,
                            5:user_prompt_5,
                            6:user_prompt_6,
                            7:user_prompt_7,
                            8:user_prompt_8,
                            9:user_prompt_9,
                            10:user_prompt_10,
                            11:user_prompt_11,
                            12:user_prompt_12,
                            13:user_prompt_13,
}
