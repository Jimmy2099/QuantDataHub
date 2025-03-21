# news_llm_analysis_prompt fast data cleaning through gemma3:1b
```
Below is a prompt template for analyzing news data and generating investment-related information. You can adjust the content based on specific needs:
Prompt:
Please analyze the following news content and generate a structured output in the following format:
Article Sentiment: Determine the overall sentiment tendency of the news (positive, negative, or neutral).
Affected Entities: List only the companies, entities, or individuals mentioned in the news. Use full names (no abbreviations) and limit to the top three most important entities.
Categories: Based on the news content, select relevant category tags (e.g., management capability, market competitiveness, financial performance, customer satisfaction, etc.). Limit to the top six most important categories.
Output in JSON format:
{
"Article Sentiment": "positive/negative/neutral",
"Affected Entities": ["Company A", "Company B"],
"Categories": ["Category 1", "Category 2"]
}
News Content:
[{{#1711708591503.input_text#}}]
```

