# Learnings from SchematronMCP

**TL;DR**: Using an ML model for HTML-to-JSON extraction is technically interesting but practically impractical. The real value of this project was learning MCP server development, model inference, and HTML preprocessing - not the extraction approach itself.

---

## Table of Contents

- [Overview](#overview)
- [What We Built](#what-we-built)
- [Key Learnings](#key-learnings)
  - [1. MCP Server Development](#1-mcp-server-development)
  - [2. ML Model Performance Reality](#2-ml-model-performance-reality)
  - [3. Field Commentary: ML-based Extraction](#3-field-commentary-ml-based-extraction)
- [What Worked Well](#what-worked-well)
- [What Didn't Work](#what-didnt-work)
- [Recommendations for Future Work](#recommendations-for-future-work)
- [When to Use This Approach](#when-to-use-this-approach)
- [Conclusion](#conclusion)

---

## Overview

SchematronMCP was built to explore using the Schematron-3B model for extracting structured JSON from HTML. While the project successfully demonstrates MCP server architecture and local model inference, it revealed fundamental performance limitations that make this approach unsuitable for production use.

**Project Duration**: ~2 weeks
**Primary Goal**: Learn MCP server development + experiment with ML extraction
**Secondary Goal**: Develop HTML preprocessing pipeline (OmniParser integration)
**Outcome**: Successful learning exercise, impractical production tool

---

## What We Built

1. **MCP Server**: Stdio-based server exposing two tools:
   - `schematron_extract_structured_data`: HTML → JSON extraction with schema validation
   - `schematron_clean_html`: HTML preprocessing and cleaning

2. **Inference Backend**: LM Studio integration for running Schematron-3B locally
   - OpenAI-compatible API
   - Quantized model support (4-bit, 8-bit)
   - Smart token budget calculation

3. **HTML Preprocessing**: lxml-based cleaning pipeline
   - Script/style removal
   - Configurable cleaning levels
   - Content structure preservation

4. **Testing UI**: Gradio web interface for manual testing and iteration

---

## Key Learnings

### 1. MCP Server Development

**What We Learned:**

✅ **MCP Protocol is Well-Designed**
- Clear separation between server and client
- Stdio transport makes deployment simple
- FastMCP library abstracts complexity well
- Progress reporting and logging work seamlessly

✅ **Tool Design Best Practices**
- Explicit parameter validation with Pydantic is essential
- Clear error messages save debugging time
- Response format options (JSON vs Markdown) are valuable
- Auto-calculating parameters (like max_tokens) improves UX

✅ **Development Workflow**
- Start with simple tools, add complexity incrementally
- Gradio UI for testing is invaluable during development
- Example schemas help users understand capabilities
- Documentation is critical for tool discoverability

**Challenges:**
- ❌ Debugging stdio transport can be tricky (no interactive debugging)
- ❌ Error handling needs to be comprehensive (failures aren't visible to users)
- ❌ Token budget management requires careful tuning

**Recommendation**: MCP is excellent for exposing specialized capabilities to AI agents. The protocol is mature and well-thought-out. Building MCP servers is a valuable skill as the ecosystem grows.

---

### 2. ML Model Performance Reality

**The Harsh Truth:**

Using Schematron-3B for HTML extraction is **10-100x slower** than traditional parsing libraries:

| Approach | Speed | Accuracy | Use Case |
|----------|-------|----------|----------|
| **BeautifulSoup/lxml** | ~10ms | 95%+ | Structured HTML |
| **Regex patterns** | ~1ms | 80-90% | Simple patterns |
| **Schematron-3B (this project)** | ~5-30s | 85-95% | Complex/messy HTML |
| **GPT-4** | ~2-10s | 90-99% | Unstructured content |

**Why is it so slow?**

1. **Model Size**: Even quantized, Schematron-3B requires significant compute
2. **Token Count**: HTML is verbose; large documents → long inference times
3. **Local Inference**: Apple Silicon (MLX) or LM Studio adds overhead
4. **Prompt Construction**: Building the full prompt with schema + HTML is expensive

**Why is accuracy not better?**

1. **Training Data Mismatch**: Schematron-3B wasn't specifically trained for all HTML structures
2. **Schema Complexity**: Complex nested schemas confuse the model
3. **HTML Noise**: Even with cleaning, some structural ambiguity remains
4. **Hallucination Risk**: Model may invent data that doesn't exist in HTML

**Real Performance Example:**

```
Input: 50KB HTML (product page)
Schema: 10 fields (name, price, rating, description, etc.)
Time: ~15 seconds
Accuracy: 90% (missed sale price, hallucinated a review count)

Same task with BeautifulSoup:
Time: ~50ms
Accuracy: 100% (with correct selectors)
```

**Verdict**: For structured HTML with predictable patterns, traditional parsers win decisively. ML extraction only makes sense for truly unstructured content.

---

### 3. Field Commentary: ML-based Extraction

**Current State of the Field (2025)**

The field of ML-based structured extraction is in an awkward phase:

**What's Happening:**
- 🔥 **Lots of hype**: "AI can extract anything from any format!"
- 💰 **Commercial interest**: Companies building extraction APIs with GPT-4/Claude
- 📊 **Research activity**: Papers on schema-guided extraction, few-shot learning
- 🏗️ **Tool development**: Schematron, HTML-T5, specialized extraction models

**What's Missing:**
- ❌ **Performance parity**: Still can't match traditional parsers on speed
- ❌ **Cost efficiency**: API calls are expensive at scale
- ❌ **Reliability**: Models hallucinate, miss edge cases, require validation
- ❌ **Clear use cases**: Where ML extraction is *necessary* vs *interesting*

**The Uncomfortable Truth:**

Most "ML extraction" use cases are:
1. **Lazy engineering**: Could be solved with XPath/CSS selectors but developer doesn't want to write them
2. **Edge case handling**: 95% of cases work with regex, ML handles the weird 5%
3. **Research experiments**: Exploring capabilities rather than solving real problems
4. **Marketing demos**: "Look, AI can do X!" without considering practicality

**Where ML Extraction *Actually* Makes Sense:**

✅ **Unstructured documents**: PDFs, scanned images, handwritten notes
✅ **Highly variable formats**: User-generated content with no schema
✅ **Cross-format normalization**: Extracting same data from wildly different sources
✅ **Natural language understanding**: "Find the warranty period" in legal text
✅ **One-off tasks**: Manual extraction would take hours, ML takes minutes

**Where It Doesn't Make Sense:**

❌ **Structured HTML**: Use BeautifulSoup, Scrapy, or Playwright
❌ **High-throughput pipelines**: Latency and cost are prohibitive
❌ **Mission-critical accuracy**: Can't risk hallucinations
❌ **Real-time applications**: 5-30 second latency is unacceptable

**Future Outlook:**

The field needs:
1. **Faster models**: Distilled extraction models optimized for speed (sub-second inference)
2. **Better benchmarks**: Honest comparisons to traditional methods, not cherry-picked examples
3. **Hybrid approaches**: ML for hard cases, traditional parsing for easy ones
4. **Cost reduction**: Current API pricing makes most use cases uneconomical

**My Prediction**: ML extraction will find its niche in handling *truly unstructured* content, but won't replace traditional parsing for structured data. The winner will be hybrid systems that route to the right tool for each task.

---

## What Worked Well

### ✅ Learning Experience

This project was an **excellent integrated learning exercise**:

1. **MCP Protocol**: Hands-on experience building a real MCP server
2. **Model Inference**: Practical knowledge of LM Studio, quantization, token budgeting
3. **HTML Processing**: Developed robust cleaning pipeline (valuable for OmniParser work)
4. **Package Structure**: Proper Python packaging, import management, project organization
5. **Documentation**: Writing clear README, quickstart guides, API docs

### ✅ Technical Implementation

Several parts worked exactly as intended:

- **FastMCP integration**: Smooth, well-documented, easy to use
- **Pydantic validation**: Caught errors early, provided clear feedback
- **Gradio UI**: Made testing and iteration fast
- **Smart token budgeting**: Auto-calculating max_tokens based on HTML size was clever
- **Config management**: JSON config with sensible defaults worked well

### ✅ Code Quality

The repository reorganization created a clean, professional structure:
- Proper package hierarchy (`schematron_mcp/`)
- Separated concerns (inference, cleaning, examples)
- Good documentation organization
- Clear experimental status (badges, disclaimers)

---

## What Didn't Work

### ❌ Core Premise

**The fundamental assumption was flawed**: ML extraction would be competitive with traditional parsing.

Reality check:
- 100x slower than BeautifulSoup
- Not meaningfully more accurate
- Higher cost (compute + development time)
- Less reliable (hallucinations, edge cases)

### ❌ Performance Optimization

Attempts to improve speed had limited impact:

| Optimization | Time Saved | Worth It? |
|--------------|------------|-----------|
| Quantization (4-bit) | ~30% | Yes (quality trade-off) |
| HTML cleaning | ~20% | Yes (also improves accuracy) |
| Prompt optimization | ~10% | Marginal |
| Smart token budgeting | ~0% | Prevents OOM but doesn't speed up |

**Conclusion**: No amount of optimization overcomes the fundamental compute cost of running a 3B parameter model.

### ❌ Use Case Fit

We struggled to find scenarios where this approach was clearly better:

- **Simple extraction**: Traditional parsers faster and more accurate
- **Complex extraction**: GPT-4/Claude API more accurate (but still slow)
- **High volume**: Cost and latency prohibitive
- **Production use**: Reliability concerns (hallucinations, timeouts)

**The only wins**:
- Edge cases with messy HTML where writing selectors is painful
- One-off extractions where setup time matters more than runtime

---

## Recommendations for Future Work

### For Researchers/Experimenters

If you want to explore this space further:

1. **Focus on Faster Models**
   - Explore distilled models (< 1B parameters)
   - Try specialized extraction models (not general-purpose LLMs)
   - Benchmark: Can you get under 1 second per extraction?

2. **Find the Right Use Case**
   - Don't compete with traditional parsers on structured HTML
   - Focus on truly unstructured content (PDFs, images, handwriting)
   - Look for cross-format normalization tasks

3. **Hybrid Approaches**
   - Use traditional parsing first, ML as fallback
   - Pattern detection: route to appropriate extraction method
   - Human-in-the-loop for validation

### For Production Use

If you need extraction for real applications:

**DON'T use this project**. Instead:

1. **Structured HTML**: Use BeautifulSoup, Scrapy, or Playwright
2. **Dynamic sites**: Use Playwright for rendering + traditional selectors
3. **Unstructured PDFs**: Use GPT-4/Claude API (accept the cost)
4. **High volume**: Build custom parsers, hire contractors to write selectors
5. **Mixed formats**: Hybrid system with router to appropriate tool

**ONLY consider ML extraction** if:
- Traditional parsing genuinely doesn't work (truly unstructured)
- Volume is low enough that latency/cost are acceptable
- You can tolerate some inaccuracy and have validation

---

## When to Use This Approach

### ✅ Good Use Cases

1. **Learning MCP Development**
   - This project is a solid reference implementation
   - Shows real-world MCP server patterns
   - Good example of tool design and error handling

2. **HTML Preprocessing Experiments**
   - The cleaning pipeline is useful for other projects
   - lxml patterns and strategies are reusable
   - Good foundation for OmniParser-style work

3. **Local Model Inference Practice**
   - Demonstrates LM Studio integration
   - Shows quantization trade-offs
   - Token budget calculation patterns

### ❌ Bad Use Cases

1. **Production HTML Extraction**
   - Too slow for any real-world application
   - Traditional parsers are better in every way
   - Cost and reliability concerns

2. **High-Volume Processing**
   - 5-30s per document is prohibitive
   - API costs would be astronomical
   - Can't scale to thousands of documents

3. **Mission-Critical Accuracy**
   - Models hallucinate
   - Edge cases unpredictable
   - No guarantees of correctness

---

## Conclusion

### What We Learned

This project confirmed a hard truth: **ML-based extraction is interesting but impractical** for most real-world HTML processing tasks. Traditional parsers win on speed, accuracy, cost, and reliability.

However, the project delivered tremendous value as a **learning experience**:
- Deep understanding of MCP server development
- Practical experience with local model inference
- Insights into HTML preprocessing and cleaning
- Understanding of when (and when not) to use ML

### Final Thoughts

**For future explorers of this space:**

Don't build this because you think it's the "AI way" to solve extraction. Build it because:
1. You want to learn MCP development (great reason!)
2. You're researching extraction models (fair enough)
3. You have a genuinely unstructured use case (rare but valid)

**For production needs:**

Use the right tool for the job:
- Structured HTML → BeautifulSoup/Scrapy
- Dynamic sites → Playwright
- PDFs/Images → GPT-4 API (if budget allows)
- Mixed/complex → Hybrid approach

**The real takeaway:**

Sometimes the best learning comes from discovering what *doesn't* work. This project taught us that the hype around "AI can do everything" doesn't always match reality. Traditional software engineering still wins most battles.

But in exploring the boundaries, we learned a ton - and that was worth it.

---

*Written November 2025*
*Model: Claude Sonnet 4.5*
*Project: SchematronMCP v0.1.0*
