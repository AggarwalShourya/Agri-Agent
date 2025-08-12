# from crewai.tools import BaseTool
# from typing import Type
# from pydantic import BaseModel, Field


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""
#     argument: str = Field(..., description="Description of the argument.")

# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, your agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."


from crewai.tools import BaseTool
import requests
from pypdf import PdfReader  
from io import BytesIO 
from typing import Type
from pydantic import BaseModel, Field

class PdfExtractorToolInput(BaseModel):  
    """Input schema for PdfExtractorTool."""
    url: str = Field(..., description="PDF URL to extract from.")
    query: str = Field(..., description="Query to search in PDF.")

class PdfExtractorTool(BaseTool):
    name: str = "PDF Extractor"
    description: str = (
        "Extract and summarize text from a PDF URL based on a query. Useful for FAO/AHDB PDFs."
    )
    args_schema: Type[BaseModel] = PdfExtractorToolInput

    def _run(self, url: str, query: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
            pdf = PdfReader(BytesIO(response.content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""

            # Simple keyword summary
            lines = text.split('\n')
            summary = [line.strip() for line in lines if query.lower() in line.lower()]
            return "\n".join(summary) or "No relevant content found for query."
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"