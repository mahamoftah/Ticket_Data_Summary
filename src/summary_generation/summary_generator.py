import logging
from typing import List, Dict, Tuple
from datetime import datetime, timezone

class SummaryGenerator:
    """Generates storytelling summaries for ticket categories using an LLM."""

    def __init__(self, llm):
        """
        Args:
            llm (object): LLM instance that provides a `.generate_response(messages)` method.
        """
        self.llm = llm
        self.logger = logging.getLogger(__name__)

    def generate_summary(self, category: str, data: List[Dict[str, str]]) -> Tuple[str, str]:
        """
        Generates a structured summary from category data.

        Args:
            category (str): The ticket category (e.g., "VOD").
            data (List[Dict]): List of ticket records (rows as dictionaries).

        Returns:
            Tuple[str, str]: Summary text and timestamp.
        """
        if not data:
            return f"No ticket data available for category: {category}", self._current_timestamp()

        prompt = self._build_prompt(category, data)

        try:
            messages = [
                {"role": "system", "content": "You are a telecom support analyst assistant."},
                {"role": "user", "content": prompt}
            ]
            response = self.llm.generate_response(messages)

            if not response or not response.strip():
                response = "I'm sorry, no summary could be generated at this time."

        except Exception as e:
            self.logger.error(f"Summary Generation Error: {e}")
            response = "There was an error while generating the summary."

        return response, self._current_timestamp()

    def _build_prompt(self, category: str, data: List[Dict[str, str]]) -> str:
        """Constructs the storytelling prompt with detailed instructions."""
        prompt = (
            f"You are tasked with generating a storytelling summary for the ticket category '{category}'.\n\n"
            "The summary must be structured into five sections directly, without any extra introductions or phrases.\n"
            "Do NOT start the output with phrases like 'Based on the provided data', 'Here is the summary', 'According to the following', etc.\n"
            "Just start the storytelling directly, organized exactly under the following sections:\n\n"


            "1. Initial Issue:\n"
                "- Timeframe: Identify the period when the initial issues began.\n"
                "- Ticket Numbers: List the relevant ticket numbers.\n"
                "- Narrative: Describe the customer's initial problems, including the nature of the issues, the customer's feedback, and any immediate actions taken.\n\n"

            "2. Follow-ups:\n"
                "- Timeframe: Document the period of follow-up activities.\n"
                "- Ticket Numbers: List the related ticket numbers.\n"
                "- Narrative: Detail the follow-up actions, including further customer interactions, additional feedback, and any responses from the support team.\n\n"

            "3. Developments:\n"
                "- Timeframe: Specify the period during which significant developments occurred.\n"
                "- Ticket Numbers: List the relevant ticket numbers.\n"
                "- Narrative: Explain the developments, such as new issues arising, advancements in resolving existing problems, and any changes in customer experiences.\n\n"

            "4. Later Incidents:\n"
                "- Timeframe: Note the timeframe for later incidents.\n"
                "- Ticket Numbers: List the related ticket numbers.\n"
                "- Narrative: Describe recurring issues or new problems that emerged, including how they were handled and the customer's ongoing feedback.\n\n"

            "5. Recent Events:\n"
                "- Timeframe: Highlight the most recent period.\n"
                "- Ticket Numbers: List the relevant ticket numbers.\n"
                "- Narrative: Provide a summary of the latest events, including current issues, recent resolutions, and the customer's final feedback.\n\n"

            "Use the ticket data below to create your storytelling summary. Focus on clarity, chronological order, and meaningful insights.\n\n"
            "Here is the ticket data:\n"
        )

        for row in data:
            ticket_info = "; ".join(f"{key}: {value}" for key, value in row.items() if value)
            prompt += f"- {ticket_info}\n"

        return prompt.strip()


    @staticmethod
    def _current_timestamp():
        """Returns the current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

