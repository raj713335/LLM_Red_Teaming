import asyncio
from openai import AsyncOpenAI

from deepteam import red_team
from deepteam.test_case import RTTurn
from deepteam.vulnerabilities import Bias
from deepteam.attacks.single_turn import PromptInjection


# Initialize OpenAI client
client = AsyncOpenAI()


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
        model="gpt-4o-mini",
        messages=messages
    )

    llm_response = response.choices[0].message.content

    print("Response:", llm_response)

    return RTTurn(
        role="assistant",
        content=llm_response
    )


# Test our LLM application normally
async def dummy_test_llm():
    result = await model_callback("Who is Virat Kohli?")
    print("\nFinal Result:")
    print(result.content)


asyncio.run(dummy_test_llm())


# Vulnerability to test
bias = Bias(types=["race"])


# Attack technique
prompt_injection = PromptInjection()


# Start Red Teaming
risk_assessment = red_team(
    model_callback=model_callback,
    vulnerabilities=[bias],
    attacks=[prompt_injection]
)


print(risk_assessment)

# Overall pass/fail rate for each vulnerability
print(risk_assessment.overview)


risk_assessment.overview.to_df()

print(risk_assessment.overview.cvss_score)  # assessment-level average
print(risk_assessment.test_cases[0].cvss_score)  # per test case