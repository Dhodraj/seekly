# Seekly CLI Copilot Instructions

## Core Principles

1. **No Hardcoding**: Avoid hardcoded solutions. Always implement approaches that work for a variety of inputs rather than being tailored to specific scenarios.

2. **Generic Approach First**: Design solutions that can handle diverse query types and file structures without being overly specialized.

3. **Adaptability Over Specificity**: Favor adaptable algorithms that can work across different programming languages, file types, and query patterns.

## Development Guidelines

### When Implementing Search Functionality

- ✅ Build semantic search capabilities that work with any natural language query
- ✅ Implement flexible embedding generation techniques that work across file types
- ✅ Design scoring systems that adapt to different query contexts
- ❌ Don't optimize for specific keyword patterns or query styles
- ❌ Don't make assumptions about specific programming language constructs
- ❌ Don't implement one-off solutions for particular query patterns

### When Processing Files

- ✅ Use language-agnostic approaches to identify code structures
- ✅ Create flexible chunking mechanisms that work for files of any size or format
- ✅ Implement relevance calculation that adapts to different content types
- ❌ Don't hardcode file path patterns or naming conventions
- ❌ Don't assume specific directory structures
- ❌ Don't rely on particular file extensions for core functionality

### When Calculating Relevance

- ✅ Build statistical approaches that autonomously adapt to content
- ✅ Design dynamic relevance systems that learn from query patterns
- ✅ Implement content-aware weighting that works across different domains
- ❌ Don't create rigid keyword matching systems
- ❌ Don't hardcode similarity thresholds for specific use cases
- ❌ Don't optimize for particular types of code structures

## Code Quality Standards

### Flexibility and Robustness

- All functions should handle unexpected inputs gracefully
- Error handling should be comprehensive and informative
- Functions should accept customizable parameters rather than using hard-coded values

### Testing Requirements

- Test with diverse query types across multiple domains
- Ensure search works well for both common and edge case scenarios
- Verify performance across different programming languages and file structures

### Documentation Standards

- Document the adaptable nature of each algorithm
- Explain how functions handle various input types
- Highlight the generic applicability of core approaches

## Examples of Good vs. Bad Approaches

### Good Approach Example:
```python
def calculate_relevance(embedding, query_embedding):
    """Dynamic relevance calculation that adapts to query context"""
    # Calculate base similarity
    similarity = cosine_similarity(embedding, query_embedding)
    
    # Apply adaptive statistical transformation based on distribution
    # This approach works for any type of content without assumptions
    return apply_adaptive_transformation(similarity)
```

### Bad Approach Example:
```python
def calculate_relevance(embedding, query_embedding):
    """Hardcoded relevance calculation for specific query types"""
    similarity = cosine_similarity(embedding, query_embedding)
    
    # Hardcoded thresholds for specific types of queries
    if "algorithm" in query.lower():
        return similarity * 1.5
    elif "function" in query.lower():
        return similarity * 1.2
    else:
        return similarity
```

Remember: The strength of Seekly is in its flexibility and ability to work with any codebase or query. Always prioritize generic, adaptable approaches over specialized solutions.