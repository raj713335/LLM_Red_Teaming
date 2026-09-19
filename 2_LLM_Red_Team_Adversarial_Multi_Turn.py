from openai import AsyncOpenAI

from deepteam import red_team
from deepteam.test_case import RTTurn
from deepteam.vulnerabilities import Bias
from deepteam.attacks.multi_turn import LinearJailbreaking
from deepteam.attacks.single_turn import Roleplay


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


# Vulnerability we want to test
gender_bias = Bias(types=["gender"])

linear_attack = LinearJailbreaking(
    num_turns=10,
    turn_level_attacks=[
        Roleplay()
    ]
)


risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[gender_bias],
    attacks=[linear_attack]
)

print(risk_assessment)

print(risk_assessment.overview)







