import asyncio
import os
from presentationAnalyzer import PresentationAnalyzer


async def main():
    """
    Main function that runs the presentation analysis.
    """
    file_name = "data structures and relavant packages"
    api_key = os.getenv("OPENAI_API_KEY")

    presentation_analyzer = PresentationAnalyzer(file_name, api_key)
    await presentation_analyzer.analyze_presentation()


if __name__ == '__main__':
    asyncio.run(main())

