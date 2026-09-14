from deepteam import red_team
from deepteam.vulnerabilities import Bias
from deepteam.attacks.single_turn import PromptInjection

bias = Bias(types=["race"])
prompt_injection = PromptInjection()

red_team(
    model_callback="openai/gpt-5-nano", # Change the model name to your desired model
    vulnerabilities=[bias],
    attacks=[prompt_injection]
)