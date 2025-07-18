from propeterra_internship_2025.data.all_countries      import country_capitals
from propeterra_internship_2025.utils.system_prompts    import system_prompt_dictionary
from propeterra_internship_2025.data.reference_material import clean_reference_material, unclean_reference_material, country_languages
from propeterra_internship_2025.utils.user_prompts      import user_prompt_dictionary, real_estate_professionals_prompt_dictionary

def create_prompt(n_sources:int, country_of_interest:str, prompt_num:int, system_prompt_num:int) -> tuple[str, str]:
    ''' Generates the prompt according to specified template "prompt_num" '''
    prompt = Prompt(num_sources=n_sources, country_of_interest=country_of_interest, prompt_num=prompt_num, system_prompt_num=system_prompt_num)
    n_established_prompts = len(user_prompt_dictionary)

    if prompt_num > n_established_prompts:
        raise ValueError(f'Prompts above {n_established_prompts} are not supported yet')

    return prompt.construct_prompt()

def create_real_estate_question_prompt(country_of_interest:str, system_prompt_num:int, user_prompt:str) -> tuple[str, str]:
    ''' Generates the prompt for real estate questions for a given country '''
    prompt = Prompt(country_of_interest=country_of_interest, system_prompt_num=system_prompt_num, user_prompt=user_prompt)
    return prompt.construct_real_estate_question_prompt()


def create_real_estate_professional_prompt(country_of_interest:str, system_prompt_num:int, prompt_num:int) -> tuple[str, str]:
    ''' Generates the prompt for real estate questions for a given country '''
    prompt = Prompt(country_of_interest=country_of_interest, system_prompt_num=system_prompt_num, prompt_num=prompt_num)
    return prompt.construct_real_estate_professional_prompt()

class Prompt:
    '''
    Class that will allow one to develop a number of prompts as well
    as construct the prompt according to the region of interest and specify how many links to 
    '''
    def __init__(self, num_sources:int=15, country_of_interest:str="Mexico", prompt_num:int=1, system_prompt_num:int=1, user_prompt:str=""):
        
        self.num_sources: str  = str(num_sources)
        self.prompt_num: int = prompt_num
        self.system_prompt_num: int = system_prompt_num
        self.country_of_interest: str = country_of_interest
        self.native_language: dict = country_languages
        self.links: list = clean_reference_material
        self.user_prompt: str = user_prompt



    def construct_prompt(self) -> tuple[str, str]:
        '''
        Will add in the user defined selections to the prompt such as 
        number of sources to return
        country of interest
        the native language in the country
        the specified reference material for the model (links regarding real estate industry created by Lee Cashell)

        '''
        user_prompt = user_prompt_dictionary.get(self.prompt_num, "")
        system_prompt = system_prompt_dictionary.get(self.system_prompt_num, "")

        if user_prompt == "":
            raise Exception
        
        if system_prompt == "":
            raise Exception
                # print("Selected prompt number not defined: {e}, please choose a valid prompt number")

        system_prompt = system_prompt.replace('__num_sources__', self.num_sources)
        system_prompt = system_prompt.replace('__country_of_interest__', self.country_of_interest)
        system_prompt = system_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        system_prompt = system_prompt.replace('__links__', " \n".join(self.links[:30]))
        system_prompt = system_prompt.replace('__prompt_num__', str(self.prompt_num))

    
        user_prompt = user_prompt.replace('__num_sources__', self.num_sources)
        user_prompt = user_prompt.replace('__country_of_interest__', self.country_of_interest)
        user_prompt = user_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        user_prompt = user_prompt.replace('__links__', " \n".join(self.links[:30]))
        user_prompt = user_prompt.replace('__prompt_num__', str(self.prompt_num))


        return system_prompt, user_prompt

    def construct_real_estate_professional_prompt(self) -> tuple[str, str]:
        '''
        Will add in the user defined selections to the prompt such as 
        number of sources to return
        country of interest
        the native language in the country
        the specified reference material for the model (links regarding real estate industry created by Lee Cashell)

        '''
        user_prompt = real_estate_professionals_prompt_dictionary.get(self.prompt_num, "")
        system_prompt = system_prompt_dictionary.get(self.system_prompt_num, "")

        if user_prompt == "":
            raise Exception
        
        if system_prompt == "":
            raise Exception
                # print("Selected prompt number not defined: {e}, please choose a valid prompt number")

        system_prompt = system_prompt.replace('__num_sources__', self.num_sources)
        system_prompt = system_prompt.replace('__country_of_interest__', self.country_of_interest)
        system_prompt = system_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        system_prompt = system_prompt.replace('__links__', " \n".join(self.links[:30]))
        system_prompt = system_prompt.replace('__prompt_num__', str(self.prompt_num))

    
        user_prompt = user_prompt.replace('__num_sources__', self.num_sources)
        user_prompt = user_prompt.replace('__country_of_interest__', self.country_of_interest)
        user_prompt = user_prompt.replace('__prompt_num__', str(self.prompt_num))


        return system_prompt, user_prompt

    def construct_real_estate_question_prompt(self) -> tuple[str, str]:
        ''' Processes user defined prompt, replacing country with country_of_interest '''

        system_prompt = system_prompt_dictionary.get(self.system_prompt_num, "")

        question_types = [
            "Commercial vs. Residential Real Estate,",
            "Country-Specific Real Estate Queries,",
            "Future Market Predictions & Trends,",
            "Investment Strategy & ROI,",
            "Macroeconomic & Regulatory Impacts,",
            "Property Management & Rental Markets,",
            "Property Prices & Market Trends,",
            "Real Estate Financing & Mortgages,",
            "Technology & AI in Real Estate,",
            "Zoning, Development, and Infrastructure,"
        ]


        split_text = self.user_prompt

        for q_type in question_types:
            if q_type in self.user_prompt:
                split_text = self.user_prompt.split(q_type)[1]
                


        split_text = split_text.replace("[country]", self.country_of_interest)
        split_text = split_text.replace("[region]", "Latin America")
        split_text = split_text.replace("[city/country]",self.country_of_interest)
        split_text = split_text.replace("[city]", country_capitals[self.country_of_interest])
        split_text = split_text.replace("[location]", country_capitals[self.country_of_interest])
        
        if "[" in split_text or "]" in split_text:
            print(split_text)

        if self.user_prompt == "":
            raise Exception
        
                # print("Selected prompt number not defined: {e}, please choose a valid prompt number")

        # system_prompt = system_prompt.replace('__num_sources__', self.num_sources)
        system_prompt = system_prompt.replace('__country_of_interest__', self.country_of_interest)
        # system_prompt = system_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        # system_prompt = system_prompt.replace('__links__', " \n".join(self.links[:30]))
        # system_prompt = system_prompt.replace('__prompt_num__', str(self.prompt_num))

    
        # user_prompt = user_prompt.replace('__num_sources__', self.num_sources)
        split_text = split_text.replace('__country_of_interest__', self.country_of_interest)
        # user_prompt = user_prompt.replace('__native_language__', self.native_language.get(self.country_of_interest, ""))
        # user_prompt = user_prompt.replace('__links__', " \n".join(self.links[:30]))
        # user_prompt = user_prompt.replace('__prompt_num__', str(self.prompt_num))




        return system_prompt, split_text
