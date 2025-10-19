#!/usr/bin/env python3
"""
Context7 Smart Detection Hook
Analyzes prompts to suggest Context7 MCP when appropriate for library documentation needs.
"""

import sys
import json
import re
from typing import Dict, List, Set

# High-value libraries where Context7 provides significant benefit
# Fast-moving frameworks with frequent updates
FAST_MOVING_LIBS = {
    "next.js", "nextjs", "next", "app router",
    "react query", "tanstack query",
    "tailwind", "tailwindcss",
    "zod", "prisma", "trpc",
    "trigger.dev", "trigger",
    "drizzle", "lucia-auth",
    "shadcn", "radix-ui"
}

# Libraries with complex/changing APIs
COMPLEX_API_LIBS = {
    "fastapi", "sqlalchemy", "pydantic",
    "playwright", "puppeteer",
    "stripe", "supabase",
    "openai", "anthropic",
    "langchain", "llamaindex"
}

# Version-sensitive keywords
VERSION_PATTERNS = {
    r"new\s+\w+\s+(feature|function|api|method)",
    r"latest\s+\w+",
    r"(how|what)\s+(do|does|is)\s+\w+\.([\w.]+)\s+work",
    r"@\w+/[\w-]+@[\d.]+",  # npm package versions
    r"version\s+[\d.]+",
    r"upgraded?\s+to"
}

# Context signals that suggest documentation needs
DOCUMENTATION_SIGNALS = {
    "how do i", "how to", "how does", "what is",
    "example", "documentation", "docs",
    "api reference", "usage",
    "implement", "integrate",
    "getting started", "tutorial",
    "breaking change", "migration",
    "deprecated"
}

# Exclude stable/well-known APIs
STABLE_LIBS = {
    "javascript", "python", "typescript",
    "html", "css", "sql",
    "git", "bash", "shell"
}

# Question patterns that benefit from Context7
QUESTION_PATTERNS = {
    r"how\s+do\s+i\s+use\s+(\w+)",
    r"what's\s+the\s+correct\s+way\s+to\s+(\w+)",
    r"how\s+does\s+(\w+\.\w+)\s+work",
    r"(\w+)\s+api\s+example",
    r"implement\s+(\w+)\s+with\s+(\w+)"
}


def detect_libraries(text: str) -> Set[str]:
    """Extract library mentions from text."""
    text_lower = text.lower()
    detected = set()

    # Check fast-moving libraries
    for lib in FAST_MOVING_LIBS:
        if lib in text_lower:
            detected.add(lib)

    # Check complex API libraries
    for lib in COMPLEX_API_LIBS:
        if lib in text_lower:
            detected.add(lib)

    # Remove stable libraries
    detected -= STABLE_LIBS

    return detected


def detect_version_sensitivity(text: str) -> bool:
    """Check if prompt mentions version-specific concerns."""
    text_lower = text.lower()

    for pattern in VERSION_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False


def detect_documentation_need(text: str) -> bool:
    """Check if prompt signals need for documentation."""
    text_lower = text.lower()

    # Check documentation signals
    for signal in DOCUMENTATION_SIGNALS:
        if signal in text_lower:
            return True

    # Check question patterns
    for pattern in QUESTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True

    return False


def calculate_confidence(
    libraries: Set[str],
    version_sensitive: bool,
    doc_need: bool,
    text: str
) -> float:
    """Calculate confidence score for Context7 recommendation."""
    score = 0.0

    # Libraries detected (max 0.4)
    if libraries:
        score += min(0.4, len(libraries) * 0.15)

    # Version sensitivity (0.3)
    if version_sensitive:
        score += 0.3

    # Documentation need (0.3)
    if doc_need:
        score += 0.3

    # Boost for specific high-value patterns
    text_lower = text.lower()

    # "use context7" already mentioned
    if "context7" in text_lower:
        return 0.0  # Already using it

    # "latest" or "new" with library
    if libraries and ("latest" in text_lower or "new " in text_lower):
        score += 0.2

    # API/method questions
    if re.search(r"(how|what)\s+does\s+\w+\.\w+", text_lower):
        score += 0.2

    return min(1.0, score)


def format_library_list(libraries: Set[str]) -> str:
    """Format library list for display."""
    if not libraries:
        return ""

    lib_list = sorted(list(libraries))
    if len(lib_list) == 1:
        return lib_list[0]
    elif len(lib_list) == 2:
        return f"{lib_list[0]} and {lib_list[1]}"
    else:
        return ", ".join(lib_list[:-1]) + f", and {lib_list[-1]}"


def generate_reminder(
    libraries: Set[str],
    confidence: float,
    version_sensitive: bool
) -> Dict:
    """Generate reminder JSON for Claude Code."""

    if confidence < 0.5:
        # Low confidence - don't suggest
        return {}

    reminders = []

    if libraries:
        lib_str = format_library_list(libraries)

        if confidence >= 0.8:
            # High confidence - strong recommendation
            reminders.append(f"🎯 Detected {lib_str} - Context7 highly recommended for latest docs")

            if version_sensitive:
                reminders.append(f"⚡ Version-specific query detected - use Context7 for accurate API info")

            # Suggest specific usage
            primary_lib = sorted(list(libraries))[0]
            reminders.append(f"💡 Suggested: Add 'use context7' to get current {primary_lib} documentation")

        elif confidence >= 0.65:
            # Medium-high confidence - gentle suggestion
            reminders.append(f"📚 Consider using Context7 for up-to-date {lib_str} documentation")
            reminders.append(f"💡 Add 'use context7' to your prompt for current API references")

    if not reminders:
        return {}

    return {
        "reminders": reminders,
        "metadata": {
            "detected_libraries": list(libraries),
            "confidence": confidence,
            "version_sensitive": version_sensitive
        }
    }


def main():
    """Hook entry point."""
    if len(sys.argv) < 2:
        # No prompt provided
        sys.exit(0)

    # Get the user's prompt from arguments
    prompt = " ".join(sys.argv[1:])

    # Analyze prompt
    libraries = detect_libraries(prompt)
    version_sensitive = detect_version_sensitivity(prompt)
    doc_need = detect_documentation_need(prompt)

    # Calculate confidence
    confidence = calculate_confidence(libraries, version_sensitive, doc_need, prompt)

    # Generate reminder
    reminder = generate_reminder(libraries, confidence, version_sensitive)

    if reminder:
        print(json.dumps(reminder, indent=2))

    sys.exit(0)


if __name__ == "__main__":
    main()
