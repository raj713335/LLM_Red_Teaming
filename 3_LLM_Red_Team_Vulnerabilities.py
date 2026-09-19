from openai import AsyncOpenAI

from deepteam import red_team
from deepteam.test_case import RTTurn
from deepteam.vulnerabilities import (
    Bias,
    Toxicity,
    PIILeakage,
    PromptLeakage,
    Misinformation
)


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

vulnerabilities = [
    Bias(
        types=["race", "gender"]
    ),

    Toxicity(
        types=["insults", "profanity"]
    ),

    PIILeakage(
        types=["api_and_database_access"]
    ),

    PromptLeakage(
        types=["secrets_and_credentials", "instructions"]
    ),

    Misinformation(
        types=["factual_errors", "unsupported_claims"]
    )
]

risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=vulnerabilities
)


print(risk_assessment.overview)




















