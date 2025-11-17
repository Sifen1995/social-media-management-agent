"""
Prompts for Posting Automation Agent.
"""

POSTER_SYSTEM_PROMPT = """You are a social media posting automation specialist.
Your role is to coordinate content publishing across multiple platforms, handle errors gracefully,
and ensure content is posted at optimal times with proper formatting for each platform."""

POSTING_VALIDATION_PROMPT = """Validate this content before posting to {platform}:

Content:
{content}

Platform Requirements:
{requirements}

Check for:
1. Character limits
2. Required fields
3. Media format compatibility
4. Hashtag limits
5. Any platform-specific violations

Return validation result as JSON:
{{
  "valid": true/false,
  "errors": ["list of errors if any"],
  "warnings": ["list of warnings"],
  "suggestions": ["improvement suggestions"]
}}
"""
