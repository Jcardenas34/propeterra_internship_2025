from propeterra_internship_2025.data.reference_material import unclean_reference_material, country_languages


class Prompt:
    '''
    Class that will allow one to develop a number of prompts as well
    as contruct the prompt according to the region of interest and specify how many links to 
    '''
    def __init__(self, num_sources:int=10, country_of_interest:str="Mexico", prompt_num:int=1):
        
        self.num_sources: str  = str(num_sources)
        self.prompt_num: int = prompt_num
        self.country_of_interest: str = country_of_interest
        self.native_language: dict = country_languages
        self.links: list = unclean_reference_material

        # First prototype link
        self.template_prototype_1 = "Using the links provided below, can you provide __num_sources__ links for webpages with similar content for the country of __country_of_interest__?\n\n" \
        "__links__\n\nI care about gathering relevant data for the real estate market that contain economic metrics that could affect real estate, how climate could affect the real estate market \n" \
        "governemental factors such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
        "and or region. The links can have information that is in the county's native language, __native_language__ as well as in English. The links can contain information or have been written between \n" \
        "the years 2016 and 2025. Please verify that the links you return are accessible. Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
        "then use your judgement to create other json keys to categorize the data into."

        # Prompt has a more demanding tone
        self.template_prototype_2 = "Provide __num_sources__ links for webpages that contain information about the real estate market for the country of __country_of_interest__\n" \
        "The links should contain information on real estate trends, economic metrics that could affect real estate, how climate could affect the real estate market \n" \
        "how governemental factors could affect real estate such as, policy and laws and regulation that could impact real estate market, as well as real estate professionals, and real estate tools that are used in the country \n" \
        "and or region. The links can have information that is in the county's native language, __native_language__ as well as in English. The links can contain information or have been written between \n" \
        "the years 2016 and 2025. Please verify that the links you return are accessible. Return your response in a JSON format where the links are categorized in according to data type and link, primarily, \n" \
        "then use your judgement to create other json keys to categorize the data into."



        self.prompt_dictionary = {
                                    1:self.template_prototype_1,
                                    2:self.template_prototype_2,
        }

    def construct_prompt(self) -> str:
        '''
        Will add in the user defined selections to the prompt such as 
        number of sources to return
        country of interest
        the native language in the country
        the specified reference material for the model (links regarding real estate industry created by Lee Cashell)

        '''
        selected_prompt = self.prompt_dictionary.get(self.prompt_num, "")

        if selected_prompt == "":
            raise Exception
                # print("Selected prompt number not defined: {e}, please choose a valid prompt number")


    
        selected_prompt = selected_prompt.replace('__num_sources__', self.num_sources)
        selected_prompt = selected_prompt.replace('__country_of_interest__', self.country_of_interest)
        selected_prompt = selected_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        selected_prompt = selected_prompt.replace('__links__', " \n".join(unclean_reference_material[:10]))


        return selected_prompt


