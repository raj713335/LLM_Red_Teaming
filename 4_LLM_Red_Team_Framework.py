from deepteam.red_teamer import risk_assessment
from openai import AsyncOpenAI

from deepteam import red_team
from deepteam.test_case import RTTurn
from deepteam.frameworks import OWASPTop10


client = AsyncOpenAI()


# Target LLM Application
# Our LLM Application
async def model_callback(input: str, turns=None):

    print("\nInput:", input)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

    # Add previous conversation turns if present
    for turn in (turns or []):
        messages.append({
            "role": turn.role,
            "content": turn.content
        })

    # Add current adversarial input
    messages.append({
        "role": "user",
        "content": input
    })

    response = await client.chat.completions.create(
        model="gpt-5-nano",
        messages=messages
    )

    llm_response = response.choices[0].message.content

    print("Response:", llm_response)

    return RTTurn(
        role="assistant",
        content=llm_response
    )

framework = OWASPTop10(
    categories=[
        "LLM_01",
        "LLM_02",
        "LLM_07",
        "LLM_09"
    ]
)

risk_assessment = red_team(
    model_callback=model_callback,
    framework=framework
)

print(risk_assessment.overview)









