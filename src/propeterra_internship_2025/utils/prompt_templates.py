from propeterra_internship_2025.data.reference_material import clean_reference_material, unclean_reference_material, country_languages
from propeterra_internship_2025.utils.user_prompts import user_prompt_dictionary
from propeterra_internship_2025.utils.system_prompts import system_prompt_dictionary

def create_prompt(n_sources:int, country_of_interest:str, prompt_num:int, system_prompt_num:int) -> tuple[str, str]:
    ''' Generates the prompt according to specified template "prompt_num" '''
    prompt = Prompt(num_sources=n_sources, country_of_interest=country_of_interest, prompt_num=prompt_num, system_prompt_num=system_prompt_num)
    n_established_prompts = len(user_prompt_dictionary)

    if prompt_num > n_established_prompts:
        raise ValueError(f'Prompts above {n_established_prompts} are not supported yet')

    return prompt.construct_prompt()


class Prompt:
    '''
    Class that will allow one to develop a number of prompts as well
    as construct the prompt according to the region of interest and specify how many links to 
    '''
    def __init__(self, num_sources:int=15, country_of_interest:str="Mexico", prompt_num:int=1, system_prompt_num:int=1):
        
        self.num_sources: str  = str(num_sources)
        self.prompt_num: int = prompt_num
        self.system_prompt_num: int = system_prompt_num
        self.country_of_interest: str = country_of_interest
        self.native_language: dict = country_languages
        self.links: list = clean_reference_material



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


