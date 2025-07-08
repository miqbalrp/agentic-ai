from pydantic import BaseModel, Field
from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    WebSearchTool
)

from schemas.finance_app import GuardrailViolationInfo

# Guardrail 1: Check if the query is related to IDX-listed companies only
class IDXOnlyQuery(BaseModel):
    """
    A guardrail to ensure that the query is related to IDX-listed companies only.
    It is used to trigger a tripwire if the query does not meet the criteria.
    The `is_idx_only_query` field indicates if the query is related to IDX companies,
    and the `reasoning` field provides an explanation for the decision.
    """
    is_idx_only_query: bool = Field(
        description="Indicates if the query is related to companies in Indonesia Stock Exchange." \
        "True if the query is related to IDX companies, False otherwise.")
    reasoning: str = Field(
        description="Explanation of why the query is considered related to IDX companies or not."
    )

query_analysis_agent = Agent(
    name="IDX Query Analysis Agent",
    instructions="Analyzes the user's query to determine if it is related to companies in Indonesia Stock Exchange." \
    "Use WebSearchTool to verify if the query is related to IDX companies.",
    output_type=IDXOnlyQuery,
    model="gpt-4o-mini",  # Use a smaller model for efficiency
)

@input_guardrail
async def idx_only_query_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    """
    Guardrail to ensure that the query is related to IDX-listed companies only.
    """
    result = await Runner.run(
        query_analysis_agent,
        input=input,
        context=ctx.context
    )
    tripwire = not result.final_output.is_idx_only_query
    return GuardrailFunctionOutput(
        output_info=GuardrailViolationInfo(
            guardrail="IDX Only Query Guardrail",
            violated=tripwire,
            reason=result.final_output.reasoning,
            details=f"Query: {input}" if tripwire else ""
        ), 
        tripwire_triggered=tripwire
    )

# Guardrail 2: Prevent investment advice language
@input_guardrail
async def compliance_guardrail(ctx, agent, input) -> GuardrailFunctionOutput:
    forbidden_phrases = ["guaranteed profit", "100% return", "insider tip"]
    if isinstance(input, list): # Handle historical input format
        latest_input = input[-1]
        input = latest_input['content']
    violated = any(phrase in input.lower() for phrase in forbidden_phrases)
    reason = (
        "Non-compliant investment advice detected."
        if violated else "No compliance issue."
    )
    return GuardrailFunctionOutput(
        output_info=GuardrailViolationInfo(
            guardrail="Compliance Guardrail",
            violated=violated,
            reason=reason,
            details=f"Query: {input}" if violated else ""
        ),
        tripwire_triggered=violated)

if __name__ == "__main__":
    import asyncio

    from utils.config import setup_openai_api_key, setup_sectors_api_key
    setup_openai_api_key()  # Set up OpenAI API key
    setup_sectors_api_key()  # Set up Sectors API key   


    # Example usage of the IDX-only query guardrail
    async def main():
        ctx = RunContextWrapper()
        input_query = "What are the top companies in Indonesia Stock Exchange?"
        result = await idx_only_query_guardrail(ctx, None, input_query)
        print(result.output_info)

    asyncio.run(main())