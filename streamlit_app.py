import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Function Best Practices | The Connor Group",
    page_icon="🏢",
    layout="wide",
)

# ── Connor Group Brand Styling ────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
  }
  h1, h2 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #111827 !important;
  }
  h3 { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; color: #111827 !important; }

  section[data-testid="stSidebar"] { background-color: #0f1b2d !important; }
  section[data-testid="stSidebar"] h1,
  section[data-testid="stSidebar"] h2,
  section[data-testid="stSidebar"] h3,
  section[data-testid="stSidebar"] p,
  section[data-testid="stSidebar"] span,
  section[data-testid="stSidebar"] label { color: #e8e8e8 !important; }

  .connor-header {
    background: linear-gradient(135deg, #11567F 0%, #0f1b2d 100%);
    padding: 28px 36px; border-radius: 10px; margin-bottom: 24px;
  }
  .connor-header h1 {
    color: #ffffff !important; font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important; font-size: 1.9em !important; margin: 0 !important;
  }
  .connor-header .subtitle {
    color: #29B5E8; font-family: 'Inter', sans-serif; font-size: 0.85em;
    font-weight: 500; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 6px;
  }

  .callout-warn { background:#fef9e7; border-left:4px solid #f59e0b;
                  padding:12px 16px; border-radius:4px; margin:10px 0; }
  .callout-good { background:#ecfdf5; border-left:4px solid #29B5E8;
                  padding:12px 16px; border-radius:4px; margin:10px 0; }
  .callout-info { background:#eff6ff; border-left:4px solid #29B5E8;
                  padding:12px 16px; border-radius:4px; margin:10px 0; }

  .section-divider {
    border: none; border-top: 2px solid #29B5E8; margin: 40px 0 32px 0; opacity: 0.3;
  }
  .section-num {
    display: inline-block; background: #29B5E8; color: #fff; width: 28px; height: 28px;
    border-radius: 50%; text-align: center; line-height: 28px; font-size: 0.85em;
    font-weight: 600; margin-right: 10px; vertical-align: middle;
  }
  h2:has(.section-num), h3:has(.section-num) {
    background: linear-gradient(90deg, #eff6ff 0%, #f8fafc 100%);
    border-left: 4px solid #29B5E8;
    padding: 12px 16px;
    border-radius: 6px;
    margin-top: 0 !important;
  }

  /* Tabs */
  .stTabs [aria-selected="true"] { border-bottom-color: #29B5E8 !important; color: #11567F !important; font-weight: 600 !important; }

  [data-testid="stMetric"] { background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: 12px 16px; }
  [data-testid="stMetricValue"] { color: #11567F !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
import base64, pathlib
logo_b64 = base64.b64encode(pathlib.Path("connor_logo.png").read_bytes()).decode()
st.markdown(f"""
<div class="connor-header">
  <div style="display:flex; align-items:center; gap:24px;">
    <img src="data:image/png;base64,{logo_b64}" style="height:50px; border-radius:4px; padding:4px 8px;">
    <div>
      <h1>Snowflake AI Function Best Practices</h1>
      <div class="subtitle">Comprehensive Reference Guide &mdash; August 2026</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_guide, tab_audit, tab_opps, tab_ent, tab_pg = st.tabs(["📖 Best Practices Guide", "🔍 Code Audit", "💡 Account Optimization", "🏢 Enterprise Edition Case", "🐘 Snowflake Postgres"])

with tab_guide:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">1</span> Use the Right Function</h2>', unsafe_allow_html=True)
    st.markdown("""
`AI_COMPLETE` is the **most expensive** AI function. Many tasks already have a cheaper,
purpose-built alternative. Using the dedicated function gives you lower cost, more
consistent output, and often better accuracy.
""")
    st.markdown("""
| Task | Wrong (expensive) | Right (cheaper) |
|---|---|---|
| Classify text into categories | `AI_COMPLETE` with classify prompt | **`AI_CLASSIFY`** |
| Filter rows by natural language | `AI_COMPLETE` returning true/false | **`AI_FILTER`** |
| Extract structured fields from text | `AI_COMPLETE` with extraction prompt | **`AI_EXTRACT`** |
| Score sentiment | `AI_COMPLETE('what is the sentiment?')` | **`AI_SENTIMENT`** |
| Translate text | `AI_COMPLETE('translate to Spanish…')` | **`AI_TRANSLATE`** |
| Summarize across many rows | `AI_COMPLETE` in a loop | **`AI_SUMMARIZE_AGG`** |
| Redact PII | `AI_COMPLETE` with masking prompt | **`AI_REDACT`** |
""")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">2</span> AI_FILTER as a Pre-Filter Gate</h2>', unsafe_allow_html=True)
    st.markdown("""
`AI_FILTER` is the **cheapest** AI function — it returns a boolean. It also includes a
built-in optimization that provides **2–10x faster performance** and up to **60% lower
token usage** on qualifying queries. Always use it to reduce row count before running
expensive downstream functions.
""")
    st.markdown("**Correct text syntax** — combine condition and data into ONE string:")
    st.code("""
-- CONCAT style
SELECT * FROM support_tickets
WHERE AI_FILTER(
  CONCAT('This ticket mentions a billing issue: ', ticket_text)
);

-- PROMPT style (cleaner for multi-column)
SELECT * FROM support_tickets
WHERE AI_FILTER(
  PROMPT('This is a complaint needing immediate attention: {0}', ticket_text)
);
""", language="sql")

    st.markdown("""
<div class="callout-info">
💡 <strong>Key rule:</strong> For text filtering, combine your instruction and the data into a 
single string using <code>CONCAT('instruction: ', column)</code> or 
<code>PROMPT('instruction: {0}', column)</code>. 
Don't pass them as two separate arguments — that only works for image files.
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">3</span> AI_EXTRACT — Correct Syntax</h2>', unsafe_allow_html=True)
    st.markdown("""
`AI_EXTRACT` pulls structured fields from text or documents. The `responseFormat` values
must be **natural language questions or descriptions** — not type names like `'string'`.
""")
    col_wrong, col_right = st.columns(2)
    with col_wrong:
        st.markdown('<div class="callout-warn">❌ <b>Wrong</b> — type names as values</div>', unsafe_allow_html=True)
        st.code("""
AI_EXTRACT(ticket_text, {
  'customer_name': 'string',
  'issue': 'string'
})
""", language="sql")
    with col_right:
        st.markdown('<div class="callout-good">✅ <b>Correct</b> — natural language descriptions</div>', unsafe_allow_html=True)
        st.code("""
AI_EXTRACT(
  text => ticket_text,
  responseFormat => {
    'customer_name': 'What is the customer full name?',
    'issue': 'What is the primary issue described?'
  }
)
""", language="sql")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">4</span> Model Selection for AI_COMPLETE</h2>', unsafe_allow_html=True)
    st.markdown("""
When you must use `AI_COMPLETE`, the model choice has a **major cost impact**. Start with
the smallest model, test quality on 50–100 rows, then upgrade only if accuracy is insufficient.
""")
    models = pd.DataFrame([
        {"Model": "llama3.1-8b",       "Provider": "Meta",      "Tier": "Economy",  "Best For": "Simple classification, structured extraction"},
        {"Model": "mistral-7b",        "Provider": "Mistral",   "Tier": "Economy",  "Best For": "Lightweight tasks, European languages"},
        {"Model": "openai-gpt-5-mini", "Provider": "OpenAI",    "Tier": "Economy",  "Best For": "Fast, cheap general completions"},
        {"Model": "llama3.1-70b",      "Provider": "Meta",      "Tier": "Standard", "Best For": "Moderate reasoning, summarization"},
        {"Model": "llama3.3-70b",      "Provider": "Meta",      "Tier": "Standard", "Best For": "Improved reasoning over 3.1-70b"},
        {"Model": "snowflake-arctic",  "Provider": "Snowflake", "Tier": "Standard", "Best For": "SQL/data-oriented tasks, enterprise Q&A"},
        {"Model": "mistral-large2",    "Provider": "Mistral",   "Tier": "Advanced", "Best For": "Complex structured outputs, JSON"},
        {"Model": "claude-3-5-sonnet", "Provider": "Anthropic", "Tier": "Advanced", "Best For": "Complex nuanced language, long context"},
        {"Model": "claude-4-sonnet",   "Provider": "Anthropic", "Tier": "Advanced", "Best For": "High-quality reasoning + documents"},
        {"Model": "claude-4-opus",     "Provider": "Anthropic", "Tier": "Premium",  "Best For": "Most demanding accuracy-critical tasks"},
        {"Model": "openai-gpt-5",      "Provider": "OpenAI",    "Tier": "Premium",  "Best For": "Frontier OpenAI capability"},
    ])
    st.dataframe(models, use_container_width=True, hide_index=True)
    st.markdown("""
<div class="callout-warn">
⚠️ <strong>Model names that do NOT exist</strong> (common mistakes):<br>
&nbsp;&nbsp;• <code>snowflake-arctic-instruct</code> → correct name is <code>snowflake-arctic</code><br>
&nbsp;&nbsp;• <code>claude-3-opus</code> → correct name is <code>claude-4-opus</code>
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">5</span> Pipeline Pattern — Chain Cheap to Expensive</h2>', unsafe_allow_html=True)
    st.markdown("""
Build a **funnel**: cheapest functions first, most expensive last. `AI_FILTER` (boolean)
→ `AI_CLASSIFY` (dedicated) → `AI_EXTRACT` (only on classified rows).
""")
    st.code("""
-- Full pipeline: filter → classify → extract (only on relevant rows)
SELECT
  ticket_id,
  AI_CLASSIFY(ticket_text, ['billing', 'technical', 'account']) AS category,
  AI_EXTRACT(
    text => ticket_text,
    responseFormat => {
      'urgency': 'How urgent is this? (low/medium/high)',
      'product': 'What product or feature is affected?'
    }
  ) AS details
FROM support_tickets
WHERE AI_FILTER(PROMPT('This is a customer complaint needing immediate attention: {0}', ticket_text))
  AND created_at >= DATEADD('day', -1, CURRENT_DATE);
""", language="sql")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">6</span> Batch Processing — Never Row-by-Row</h2>', unsafe_allow_html=True)
    st.markdown("Always apply AI functions in **set-based SQL**. Row-by-row loops kill performance and exhaust concurrency.")
    col_bad, col_good = st.columns(2)
    with col_bad:
        st.markdown('<div class="callout-warn">❌ <b>Bad — row-by-row loop</b></div>', unsafe_allow_html=True)
        st.code("""
FOR rec IN (SELECT * FROM my_table) DO
  LET result := AI_CLASSIFY(
    rec.text, ['A','B','C']
  );
  -- one row at a time = slow + expensive
END FOR;
""", language="sql")
    with col_good:
        st.markdown('<div class="callout-good">✅ <b>Good — set-based single pass</b></div>', unsafe_allow_html=True)
        st.code("""
INSERT INTO results
SELECT id,
  AI_CLASSIFY(text, ['A','B','C']) AS category
FROM my_table
WHERE processed_at IS NULL;
-- all rows in parallel
""", language="sql")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">7</span> Dynamic Tables — Use ADAPTIVE Refresh</h2>', unsafe_allow_html=True)
    st.markdown("""
`REFRESH_MODE = ADAPTIVE` is the **recommended mode** for pipelines that use AI functions.
Snowflake's ADAPTIVE heuristic automatically **skips reinitialization** when it detects
Cortex AI functions (because re-running them across all rows is too costly). It processes
only new/changed rows by default.
""")
    st.code("""
CREATE OR REPLACE DYNAMIC TABLE customer_sentiment
  TARGET_LAG = '1 hour'
  WAREHOUSE = my_wh
  REFRESH_MODE = ADAPTIVE   -- recommended for AI function workloads
AS
SELECT
  customer_id,
  review_text,
  AI_SENTIMENT(review_text) AS sentiment   -- must be in SELECT clause
FROM raw_reviews;
""", language="sql")
    st.markdown("""
<div class="callout-warn">
⚠️ <strong>Key constraint:</strong> AI functions in dynamic tables are only supported in the
<code>SELECT</code> clause. They are <strong>not supported</strong> in <code>WHERE</code>,
<code>GROUP BY</code>, <code>HAVING</code>, or <code>QUALIFY</code>.
</div>
""", unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">8</span> Trim Text to Reduce Token Costs</h2>', unsafe_allow_html=True)
    st.markdown("""
AI functions are billed by token. Sending HTML, boilerplate headers, extra whitespace,
or duplicate context inflates cost with zero accuracy benefit.
""")
    st.code("""
-- Strip HTML tags and trim whitespace before sending to AI
SELECT AI_CLASSIFY(
  TRIM(REGEXP_REPLACE(raw_email_body, '<[^>]+>', '')),
  ['billing', 'technical', 'general']
)
FROM emails;
""", language="sql")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">9</span> Remove the Deprecated SNOWFLAKE.CORTEX.* Namespace</h2>', unsafe_allow_html=True)
    st.markdown("This namespace is **deprecated and will be removed by end of 2026.** Migrate all code now.")
    col_dep, col_new = st.columns(2)
    with col_dep:
        st.markdown('<div class="callout-warn">❌ <b>Deprecated — remove</b></div>', unsafe_allow_html=True)
        st.code("SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-8b', prompt);\nSELECT SNOWFLAKE.CORTEX.CLASSIFY_TEXT(text, labels);\nSELECT SNOWFLAKE.CORTEX.SENTIMENT(text);", language="sql")
    with col_new:
        st.markdown('<div class="callout-good">✅ <b>Current — use these</b></div>', unsafe_allow_html=True)
        st.code("SELECT AI_COMPLETE('llama3.1-8b', prompt);\nSELECT AI_CLASSIFY(text, labels);\nSELECT AI_SENTIMENT(text);", language="sql")

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">10</span> Sample Before Running at Scale</h2>', unsafe_allow_html=True)
    st.markdown("Always validate accuracy and estimate cost on a small sample before committing to millions of rows.")
    st.code("""
-- Test on 100 rows first
SELECT
  AI_EXTRACT(
    text => note_text,
    responseFormat => {
      'priority': 'What is the priority level? (P1/P2/P3)',
      'action_item': 'What is the recommended next action?'
    }
  )
FROM case_notes
TABLESAMPLE (100 ROWS);
""", language="sql")

with tab_audit:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Audit Existing Code for Inefficient Patterns")
    st.markdown("""
Run these queries against your `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` to find AI function
usage that may be costing more than necessary. Copy and run each audit in a worksheet.
""")

    st.markdown("#### Audit 1: Find queries using the deprecated SNOWFLAKE.CORTEX.* namespace")
    st.code("""
-- Find deprecated namespace usage (migrate these to AI_* functions)
SELECT
  query_id,
  user_name,
  start_time,
  SUBSTR(query_text, 1, 200) AS query_preview
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE (query_text ILIKE '%SNOWFLAKE.CORTEX.COMPLETE%'
    OR query_text ILIKE '%SNOWFLAKE.CORTEX.CLASSIFY_TEXT%'
    OR query_text ILIKE '%SNOWFLAKE.CORTEX.SENTIMENT%'
    OR query_text ILIKE '%SNOWFLAKE.CORTEX.SUMMARIZE%'
    OR query_text ILIKE '%SNOWFLAKE.CORTEX.TRANSLATE%')
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP)
ORDER BY start_time DESC;
""", language="sql")

    st.markdown("#### Audit 2: Find AI_COMPLETE calls that should be a dedicated function")
    st.code("""
-- Queries using AI_COMPLETE for tasks a dedicated function handles better
SELECT
  query_id,
  user_name,
  start_time,
  SUBSTR(query_text, 1, 300) AS query_preview,
  CASE
    WHEN query_text ILIKE '%classif%' OR query_text ILIKE '%categoriz%'
      THEN 'Consider AI_CLASSIFY'
    WHEN query_text ILIKE '%sentiment%' OR query_text ILIKE '%positive%negative%'
      THEN 'Consider AI_SENTIMENT'
    WHEN query_text ILIKE '%translat%'
      THEN 'Consider AI_TRANSLATE'
    WHEN query_text ILIKE '%extract%' OR query_text ILIKE '%parse%'
      THEN 'Consider AI_EXTRACT'
    WHEN query_text ILIKE '%filter%' OR query_text ILIKE '%true or false%'
      THEN 'Consider AI_FILTER'
    ELSE 'Review manually'
  END AS recommendation
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_text ILIKE '%AI_COMPLETE%'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP)
  AND execution_status = 'SUCCESS'
ORDER BY start_time DESC
LIMIT 50;
""", language="sql")

    st.markdown("#### Audit 3: Find expensive models used for potentially simple tasks")
    st.code("""
-- Spot queries using premium models that might work with cheaper ones
SELECT
  query_id,
  user_name,
  start_time,
  SUBSTR(query_text, 1, 200) AS query_preview,
  CASE
    WHEN query_text ILIKE '%claude-4-opus%' THEN 'claude-4-opus (Premium)'
    WHEN query_text ILIKE '%openai-gpt-5%' THEN 'openai-gpt-5 (Premium)'
    WHEN query_text ILIKE '%claude-4-sonnet%' THEN 'claude-4-sonnet (Advanced)'
    WHEN query_text ILIKE '%claude-3-5-sonnet%' THEN 'claude-3-5-sonnet (Advanced)'
    ELSE 'Other'
  END AS model_tier
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE (query_text ILIKE '%claude-4-opus%'
    OR query_text ILIKE '%openai-gpt-5%'
    OR query_text ILIKE '%claude-4-sonnet%'
    OR query_text ILIKE '%claude-3-5-sonnet%')
  AND query_text ILIKE '%AI_COMPLETE%'
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP)
ORDER BY start_time DESC
LIMIT 50;
""", language="sql")

    st.markdown("#### Audit 4: Find AI functions running without pre-filtering (full table scans)")
    st.code("""
-- Queries calling AI functions on large tables without a WHERE clause
SELECT
  query_id,
  user_name,
  start_time,
  rows_produced,
  total_elapsed_time / 1000 AS seconds,
  SUBSTR(query_text, 1, 300) AS query_preview
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE (query_text ILIKE '%AI_COMPLETE%'
    OR query_text ILIKE '%AI_CLASSIFY%'
    OR query_text ILIKE '%AI_EXTRACT%')
  AND query_text NOT ILIKE '%AI_FILTER%'
  AND query_text NOT ILIKE '%WHERE%'
  AND query_text NOT ILIKE '%TABLESAMPLE%'
  AND rows_produced > 1000
  AND start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP)
ORDER BY rows_produced DESC
LIMIT 30;
""", language="sql")

    st.markdown("#### Audit 5: Find row-by-row loop patterns in stored procedures")
    st.code("""
-- Stored procedures that call AI functions inside loops
SELECT
  p.procedure_name,
  p.procedure_schema,
  p.procedure_definition
FROM SNOWFLAKE.ACCOUNT_USAGE.PROCEDURES p
WHERE (p.procedure_definition ILIKE '%AI_COMPLETE%'
    OR p.procedure_definition ILIKE '%AI_CLASSIFY%'
    OR p.procedure_definition ILIKE '%AI_EXTRACT%'
    OR p.procedure_definition ILIKE '%SNOWFLAKE.CORTEX%')
  AND (p.procedure_definition ILIKE '%FOR %'
    OR p.procedure_definition ILIKE '%LOOP%'
    OR p.procedure_definition ILIKE '%CURSOR%')
  AND p.deleted IS NULL;
""", language="sql")

    st.markdown("""
<div class="callout-good">
✅ <strong>After running these audits:</strong> Prioritize fixes by potential savings —
Audit 4 (full scans without filters) and Audit 2 (AI_COMPLETE misuse) typically yield
the largest cost reductions.
</div>
""", unsafe_allow_html=True)

with tab_opps:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Account Optimization Opportunities")
    st.markdown("""
**Account:** PZA77439 | **Analysis Date:** August 18, 2026  
Based on trailing 95-day warehouse telemetry, token-level AI billing data, and full usage history.
""")

    # ── Opportunity 1 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">1</span> Auto-Suspend Configuration — Immediate, Low-Risk Savings</h3>', unsafe_allow_html=True)
    st.markdown("""
Three warehouses have auto-suspend set to **600 seconds (10 minutes)**. For intermittent or 
batch workloads, this causes idle compute burn after the last query completes. Standard 
recommendation is **60 seconds**.
""")
    suspend_data = pd.DataFrame([
        {"Warehouse": "COMPUTE_WH", "Size": "XSmall", "Current Suspend": "600s", "Credits (95d)": "1,253", "Note": "Highest volume — prioritize"},
        {"Warehouse": "GITHUB_WORKFLOWS_WH", "Size": "XSmall", "Current Suspend": "600s", "Credits (95d)": "73", "Note": "Bursty CI/CD jobs"},
        {"Warehouse": "KINSTA_WH", "Size": "XSmall", "Current Suspend": "600s", "Credits (95d)": "22", "Note": "Low volume"},
    ])
    st.dataframe(suspend_data, use_container_width=True, hide_index=True)
    st.markdown("""
<div class="callout-good">
✅ <strong>Already correct:</strong> LLM_GATEWAY (10s), DATA_PIPELINE_WH (60s), REPORTING_WH, BACKUP_WH, GDS_APP_WH (≤60s)
</div>
""", unsafe_allow_html=True)
    st.code("""
ALTER WAREHOUSE COMPUTE_WH SET AUTO_SUSPEND = 60;
ALTER WAREHOUSE GITHUB_WORKFLOWS_WH SET AUTO_SUSPEND = 60;
ALTER WAREHOUSE KINSTA_WH SET AUTO_SUSPEND = 60;
""", language="sql")

    # ── Opportunity 2 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">2</span> DATA_PIPELINE_WH — Snowpark UDF Overhead</h3>', unsafe_allow_html=True)
    st.markdown("""
Snowpark credits on DATA_PIPELINE_WH (**1,700**) exceed base warehouse compute (**1,263**) 
over 95 days. Of those, **472 credits** are Python UDF execution — nearly a third of total 
Snowpark cost is from UDF overhead.
""")
    st.markdown("""
**Root cause:** Python UDFs running row-by-row are the most expensive Snowpark pattern.

**Fixes (in priority order):**
1. **Convert to vectorized UDFs** — receive a Pandas Series, return a Pandas Series (10–50x reduction)
2. **Replace with native SQL** or built-in functions where possible
3. **Snowpark-Optimized Warehouse** (Medium+) — 16x memory headroom for heavy data science work

Given the `SVC_GITLAB_PIPELINES` usage pattern (dbt + Snowpark DE + COPY), this is the 
**single highest-leverage engineering optimization** available.
""")

    # ── Opportunity 3 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">3</span> AI Model Selection — Material Credit Reduction</h3>', unsafe_allow_html=True)
    st.markdown("Token-level billing shows significant cost variation across models:")
    model_costs = pd.DataFrame([
        {"Model": "openai-gpt-5-mini", "Credits/M Tokens": 0.18, "Tier": "Economy"},
        {"Model": "llama3.1-70b", "Credits/M Tokens": 0.43, "Tier": "Standard"},
        {"Model": "llama3.1-405b", "Credits/M Tokens": 1.42, "Tier": "Advanced"},
        {"Model": "openai-gpt-4.1", "Credits/M Tokens": 1.47, "Tier": "Advanced"},
        {"Model": "openai-gpt-5.2 (AI_COMPLETE)", "Credits/M Tokens": 1.65, "Tier": "Premium"},
    ])
    st.dataframe(model_costs, use_container_width=True, hide_index=True)
    st.markdown("""
<div class="callout-warn">
⚠️ <strong>Key finding:</strong> The AI_COMPLETE workload using gpt-5.2 consumed <strong>577 credits</strong>. 
The same token volume at gpt-5-mini rates = ~62 credits — a <strong>9x cost difference</strong>.<br><br>
The July 27 burst alone (366 credits via gpt-5.2): at llama3.1-70b = ~96 credits; at gpt-5-mini = ~40 credits. 
That's <strong>270–326 credits saved on a single day's run</strong>.
</div>
""", unsafe_allow_html=True)
    st.markdown("""
**Recommended tiered routing policy:**
- **Bulk/batch** (backfills, scoring, embedding refreshes) → `llama3.1-70b` or `openai-gpt-5-mini`
- **Real-time user-facing** (where quality justifiably matters) → `openai-gpt-5.2` or `openai-gpt-4.1`

The team already ran multi-model benchmarking on July 15 — you have the data to make this decision.
""")

    # ── Opportunity 4 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">4</span> EMBED_TEXT Bulk Runs — Batching Strategy</h3>', unsafe_allow_html=True)
    st.markdown("""
The June 8–10 embedding burst (**10.2 billion tokens in 3 days**) consumed ~508 credits. 
The concentration suggests it ran without throttling or batching controls.

**If re-embedding is needed** (e.g., model switch — already done once), spreading across 
10–14 nightly batches prevents credit spike days that trigger billing alerts.

**Good news:** Current production model `snowflake-arctic-embed-m-v1.5` costs only 
**0.03 credits/M tokens** — one of the most efficient options available. Model choice is sound.
""")

    # ── Opportunity 5 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">5</span> Resource Monitors — Spike Prevention</h3>', unsafe_allow_html=True)
    st.markdown("""
April 2025 (1,491 credits) and May 2025 (2,700 credits) are the two largest months since 
account creation. **No resource monitors are currently visible** in the account.

Without monitors, a runaway Snowpark job, unbounded COPY, or misconfigured task loop can 
generate these volumes before anyone notices.
""")
    st.code("""
-- Account-level resource monitor (adjust quota to your baseline)
CREATE RESOURCE MONITOR account_monthly_guard
  WITH CREDIT_QUOTA = 2000  -- 120% of trailing 3-month average
  TRIGGERS
    ON 80 PERCENT DO NOTIFY
    ON 100 PERCENT DO SUSPEND_IMMEDIATE;

ALTER ACCOUNT SET RESOURCE_MONITOR = account_monthly_guard;

-- Per-warehouse monitors for the two biggest spenders
CREATE RESOURCE MONITOR compute_wh_guard
  WITH CREDIT_QUOTA = 500
  TRIGGERS ON 90 PERCENT DO NOTIFY ON 100 PERCENT DO SUSPEND;

ALTER WAREHOUSE COMPUTE_WH SET RESOURCE_MONITOR = compute_wh_guard;
""", language="sql")

    # ── Opportunity 6 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">6</span> SENTIMENT_DETECT Growth Trajectory — Monitor Before It Scales</h3>', unsafe_allow_html=True)
    st.markdown("""
Running daily since May 20, 2026 (90+ consecutive days). Token volume has grown **110x**: 
from 317 tokens/day → 35,000+ tokens/day in August. At this rate, could reach 100K–200K 
tokens/day by Q4 2026.

Cost per token is low (sentiment_sf_v3 is lightweight), but the **growth curve signals a 
production AI workload that has quietly become load-bearing**. Any disruption would have 
operational downstream effects.
""")
    st.code("""
-- Alert on unusual SENTIMENT_DETECT volume spikes
CREATE ALERT sentiment_volume_alert
  WAREHOUSE = COMPUTE_WH
  SCHEDULE = 'USING CRON 0 8 * * * America/New_York'
  IF (EXISTS (
    SELECT 1
    FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_AI_FUNCTIONS_USAGE_HISTORY
    WHERE FUNCTION_NAME = 'SENTIMENT_DETECT'
      AND START_TIME >= DATEADD('day', -1, CURRENT_TIMESTAMP)
    HAVING SUM(CREDITS) > 0.5  -- adjust threshold as volume grows
  ))
  THEN
    CALL SYSTEM$SEND_EMAIL(
      'my_email_integration',          -- notification integration name
      'ops-team@connorgroup.com',      -- recipient(s)
      'SENTIMENT_DETECT spike detected',
      'Daily AI function volume exceeded threshold. Review usage in CORTEX_AI_FUNCTIONS_USAGE_HISTORY.'
    );
""", language="sql")

    # ── Opportunity 7 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">7</span> Dynamic Tables — Target Lag Review</h3>', unsafe_allow_html=True)
    st.markdown("""
**1,088 credits** from DT REFRESH across **152,313 refresh jobs** over the trailing period 
(~1,600 refresh jobs/day). If any tables have a target lag of ≤1 minute but serve dashboards 
that only need 5–15 minute freshness, relaxing the lag saves credits proportionally.

**A 5x lag increase** on a 1-minute table saves ~80% of that table's refresh credits.

The Retool and Power BI workloads are the primary consumers — ops dashboards typically 
do not require sub-minute freshness.
""")
    st.code("""
-- Check current target lags on all dynamic tables
SHOW DYNAMIC TABLES;

-- Example: relax a table from 1 minute to 5 minutes
ALTER DYNAMIC TABLE my_db.my_schema.my_dt SET TARGET_LAG = '5 minutes';
""", language="sql")

    # ── Opportunity 8 ─────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">8</span> Dual CI/CD Platforms — Redundancy Cost</h3>', unsafe_allow_html=True)
    st.markdown("""
Both **GitLab CI/CD** (`SVC_GITLAB_PIPELINES` — 658 credits, dbt + ingestion) and 
**GitHub Actions** (`SVC_GITHUB_WORKFLOWS` — 73 credits, lighter workflows) are active.

Running both means maintaining two sets of service accounts, secrets, pipeline definitions, 
and paying for overlapping Snowflake execution. Unless there is a deliberate architectural 
reason, **consolidating to one platform** eliminates operational overhead and removes the 
GitHub warehouse entirely.
""")

    st.markdown("""
<div class="callout-good">
✅ <strong>Summary of estimated savings:</strong><br>
&nbsp;&nbsp;• Auto-suspend fix: immediate, low-effort<br>
&nbsp;&nbsp;• AI model tiering: up to <strong>~500 credits saved</strong> on batch runs<br>
&nbsp;&nbsp;• Vectorized UDFs: up to <strong>~400 credits saved</strong> on DATA_PIPELINE_WH<br>
&nbsp;&nbsp;• DT lag relaxation: proportional to current refresh frequency<br>
&nbsp;&nbsp;• Resource monitors: prevents future spikes like the 2,700-credit May 2025 incident
</div>
""", unsafe_allow_html=True)

with tab_ent:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Enterprise Edition Case")
    st.markdown("""
**Account:** PZA77439 | **Current Edition:** Standard | **Analysis Date:** August 18, 2026
""")

    # ── Reason 1 ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">1</span> A Governance Crisis Hidden in Plain Sight</h3>', unsafe_allow_html=True)
    st.markdown("""
The account has **no MFA policy** at any level. Combined with the current admin assignments, 
this creates material security exposure:
""")
    security_data = pd.DataFrame([
        {"User": "LEADLIFECYCLE", "Role": "ACCOUNTADMIN", "Volume": "1M+ queries, 1,337 credits", "Risk": "No MFA, no RSA key, SAML only"},
        {"User": "ROSS", "Role": "ACCOUNTADMIN + ORG_ADMIN", "Volume": "Admin operations", "Risk": "No MFA, no RSA key"},
        {"User": "SVC_GITLAB_PIPELINES", "Role": "SYSADMIN (over-privileged)", "Volume": "All dbt + COPY pipelines", "Risk": "NOT HEALTHY, should be lower role"},
    ])
    st.dataframe(security_data, use_container_width=True, hide_index=True)
    st.markdown("""
**Enterprise unlocks:**
- **Authentication Policies** — enforce MFA for humans, RSA key pair for service accounts, block password-only auth
- **Row Access Policies** — control which users see data for which properties/markets (critical with Retool, Power BI, Copilot Studio all querying same tables)
- **Dynamic Data Masking** — mask PII (tenant contacts, income, lead details) by role without building separate views
- **Object Tagging & Data Classification** — systematic sensitive column governance across Bright Data ingestion + Copilot Studio integration
""")

    # ── Reason 2 ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">2</span> Multi-Cluster Warehouses — Workload Has Outgrown Single-Cluster</h3>', unsafe_allow_html=True)
    st.markdown("""
**22 users** and **5 million query jobs** from **49 tools/connectors** share single-cluster 
XSmall warehouses. COMPUTE_WH alone: 1,253 credits in 95 days — heavily utilized and continuously running.

Concurrent workloads competing for the same cluster:
""")
    concurrency_data = pd.DataFrame([
        {"User/Service": "LEADLIFECYCLE", "Workload": "Python Connector, high-volume SELECT"},
        {"User/Service": "CBURKE", "Workload": "Snowpark + Python + DML"},
        {"User/Service": "SVC_DATA_ANALYTICS", "Workload": "Retool dashboards"},
        {"User/Service": "SVC_PRICING_TOOL", "Workload": "IIS live pricing lookups"},
        {"User/Service": "COPILOT_SERVICE_PRINCIPAL", "Workload": "Copilot Studio"},
    ])
    st.dataframe(concurrency_data, use_container_width=True, hide_index=True)
    st.markdown("""
<div class="callout-warn">
⚠️ Single-cluster warehouses cannot scale horizontally. When multiple workloads queue, 
later queries wait regardless of urgency. For a leasing team running live pricing lookups 
alongside bulk Snowpark ingestion, contention = application latency.
</div>
""", unsafe_allow_html=True)
    st.markdown("""
**Enterprise unlocks Multi-Cluster Warehouses** — auto-scale clusters up when queuing is 
detected, wind down when concurrency drops. Eliminates contention between Retool, Power BI, 
and pipeline workloads.
""")

    # ── Reason 3 ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">3</span> Search Optimization Service — Addresses Highest-Volume Workload</h3>', unsafe_allow_html=True)
    st.markdown("""
LEADLIFECYCLE: **1 million+ query jobs**, 1,337 credits, primarily Python Connector SELECT 
queries. For a multifamily operator, this almost certainly includes selective point-lookups — 
finding a lead by ID, retrieving unit history, filtering by property or move-in date.

**Search Optimization Service (Enterprise only)** maintains hidden optimization structures 
for exact match and range predicates. Even a **20% reduction** in scan cost across 1M+ 
selective queries = meaningful credit savings + faster IIS application response times.
""")

    # ── Reason 4 ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">4</span> 90-Day Time Travel — Required for Your Industry</h3>', unsafe_allow_html=True)
    st.markdown("""
Standard Edition: **1 day** of Time Travel.  
Enterprise Edition: **up to 90 days.**

You handle resident applications, lease agreements, maintenance records, and 
financial data. **Fair housing compliance and landlord-tenant law** in many jurisdictions 
requires producing historical data records for audits, disputes, or legal discovery. 

One day of Time Travel is operationally inadequate for that environment.
""")

    # ── Reason 5 ──────────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h3><span class="section-num">5</span> Materialized Views — Pre-Compute Dashboard Aggregations</h3>', unsafe_allow_html=True)
    st.markdown("""
DASHBOARD_WH (308 credits) + REPORTING_WH (308 credits) = **616 credits** dedicated to 
BI query serving over 95 days. Both run daily with consistent, repeating query patterns.

**Materialized Views (Enterprise only)** pre-compute and persist results, then maintain 
them incrementally. The most repeated aggregations — occupancy by property, lead conversion 
rates, pricing summaries — could be served at a fraction of per-query compute cost.
""")

    # ── Enterprise-Unlocked Optimizations ─────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("Enterprise-Unlocked Optimizations")
    st.markdown("With Enterprise in place, these actions become available:")

    st.markdown("#### Search Optimization on Lead & Tenant Tables")
    st.markdown("""
Enable SOS on columns used as selective filters in LEADLIFECYCLE's highest-frequency queries — 
prospect IDs, unit identifiers, property codes, move-in date ranges.
""")
    st.code("""
ALTER TABLE leads ADD SEARCH OPTIMIZATION ON EQUALITY(prospect_id, property_code);
ALTER TABLE leads ADD SEARCH OPTIMIZATION ON EQUALITY(unit_id) SUBSTRING(prospect_name);
ALTER TABLE tenants ADD SEARCH OPTIMIZATION ON EQUALITY(tenant_id, unit_id);
""", language="sql")

    st.markdown("#### Materialized Views for BI Warehouses")
    st.code("""
-- Example: pre-compute daily occupancy by property
CREATE MATERIALIZED VIEW mv_occupancy_by_property AS
SELECT
  property_code,
  DATE_TRUNC('day', report_date) AS report_day,
  COUNT_IF(status = 'OCCUPIED') AS occupied_units,
  COUNT(*) AS total_units,
  COUNT_IF(status = 'OCCUPIED') / COUNT(*) AS occupancy_rate
FROM unit_status
GROUP BY property_code, report_day;
""", language="sql")

    st.markdown("#### Multi-Cluster on COMPUTE_WH")
    st.code("""
ALTER WAREHOUSE COMPUTE_WH SET
  MIN_CLUSTER_COUNT = 1,
  MAX_CLUSTER_COUNT = 2,
  SCALING_POLICY = 'ECONOMY';  -- scale up only when fully queued
""", language="sql")

    st.markdown("#### Authentication Policy")
    st.code("""
-- Enforce MFA for all human users, key pair for service accounts
CREATE AUTHENTICATION POLICY account_auth_policy
  MFA_AUTHENTICATION_METHODS = ('TOTP')
  CLIENT_TYPES = ('SNOWFLAKE_UI', 'DRIVERS', 'SNOWSQL')
  AUTHENTICATION_METHODS = ('SAML', 'PASSWORD');

ALTER ACCOUNT SET AUTHENTICATION POLICY = account_auth_policy;

-- Force LEADLIFECYCLE and ROSS into compliant posture
ALTER USER LEADLIFECYCLE SET MINS_TO_BYPASS_MFA = 0;
ALTER USER ROSS SET MINS_TO_BYPASS_MFA = 0;

-- Restrict service accounts to key pair only
ALTER USER SVC_GITLAB_PIPELINES SET AUTHENTICATION POLICY = svc_key_only_policy;
ALTER USER SVC_DATA_PIPELINE SET AUTHENTICATION POLICY = svc_key_only_policy;
""", language="sql")

    st.markdown("#### Dynamic Data Masking on PII Columns")
    st.code("""
-- Masking policy: full value for privileged roles, masked for everyone else
CREATE MASKING POLICY mask_pii AS (val STRING)
  RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ACCOUNTADMIN', 'DATA_ADMIN')
      THEN val
    ELSE '***MASKED***'
  END;

-- Apply to PII columns
ALTER TABLE leads MODIFY COLUMN email SET MASKING POLICY mask_pii;
ALTER TABLE leads MODIFY COLUMN phone SET MASKING POLICY mask_pii;
ALTER TABLE tenants MODIFY COLUMN ssn_last4 SET MASKING POLICY mask_pii;
ALTER TABLE tenants MODIFY COLUMN income SET MASKING POLICY mask_pii;
""", language="sql")

    # ── The Alignment Argument ────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.header("The Alignment Argument")
    st.markdown("""
<div class="callout-info">
💡 <strong>This is your most active account.</strong> PZA77439 has run <strong>5 million query jobs</strong>, 
14,249 total credits, 22 users, and 49 integrated tools. Leaving the most active account on the 
least-capable edition creates a capability and governance gap that only grows as usage scales.
</div>
""", unsafe_allow_html=True)
    st.markdown("""
<div class="callout-warn">
⚠️ <strong>The governance gap is a liability today, not a future concern.</strong> 
LEADLIFECYCLE — highest-volume query user, ACCOUNTADMIN, processing tenant and lead PII daily — 
has no MFA. That is a <strong>live exposure</strong> that Authentication Policies (Enterprise only) 
resolve immediately. The risk is measurable and the fix is available.
</div>
""", unsafe_allow_html=True)
with tab_pg:
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">↗</span> Snowflake Postgres — Eliminate the Sync Layer</h2>', unsafe_allow_html=True)
    st.markdown("""
**The opportunity:** You currently run ~12 Python web apps on Sevalla that read 
from a co-hosted Postgres database synced hourly from Snowflake. Snowflake Postgres can 
replace that external Postgres entirely — your apps connect via standard `psql` / `psycopg2` 
to a Postgres-compatible endpoint backed directly by Snowflake data.
""")

    # ── Current Architecture ──────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">1</span> Current Architecture</h2>', unsafe_allow_html=True)
    st.markdown("""
```
┌─────────────────────────────────────────────────────────────┐
│                    CURRENT STATE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Snowflake (source of truth)                                │
│       │                                                     │
│       │  hourly incremental sync (KINSTA_WH)                │
│       ▼                                                     │
│  Postgres on Sevalla (app database)                         │
│       │                                                     │
│       │  fast reads                                         │
│       ▼                                                     │
│  ~12 Python Web Apps (reporting + CRUD)                     │
│       │                                                     │
│       │  user input pushed back                             │
│       ▼                                                     │
│  Snowflake (dims/facts updated)                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
""")
    st.markdown("""
**Pain points of this approach:**
- Hourly sync means data is always up to 60 minutes stale
- Maintaining a separate Postgres instance (Sevalla cost, ops burden)
- Two systems to monitor, backup, and secure
- Schema drift risk between Snowflake and the Postgres replica
- The sync job itself (KINSTA_WH) consuming Snowflake credits
""")

    # ── Proposed Architecture ─────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">2</span> Proposed Architecture with Snowflake Postgres</h2>', unsafe_allow_html=True)
    st.markdown("""
```
┌─────────────────────────────────────────────────────────────┐
│                    PROPOSED STATE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Snowflake (source of truth)                                │
│       │                                                     │
│       │  Snowflake Postgres endpoint                        │
│       │  (native psql/psycopg2 compatible)                  │
│       ▼                                                     │
│  ~12 Python Web Apps (reporting + CRUD)                     │
│       │  ← connect via standard Postgres wire protocol      │
│       │  ← reads are live (no sync delay)                   │
│       │  ← writes go directly to Snowflake                  │
│       │                                                     │
│  No external Postgres needed                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
""")
    st.markdown("""
**What changes:**
- You swap your Postgres connection string → Snowflake Postgres endpoint
- No code rewrite — standard `psycopg2`, SQLAlchemy, Django ORM all work
- Sync layer eliminated entirely (no more hourly job, no KINSTA_WH credits)
- Data is always fresh — no 60-minute staleness window
- One system to govern, monitor, and secure
""")

    # ── What is Snowflake Postgres ────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">3</span> What is Snowflake Postgres?</h2>', unsafe_allow_html=True)
    st.markdown("""
Snowflake Postgres is a **Postgres-compatible interface** to Snowflake. It speaks the 
PostgreSQL wire protocol natively, so existing tools and applications that connect to 
Postgres can connect to Snowflake without modification.

**Key capabilities:**
- Standard Postgres connection via `psql`, `psycopg2`, `pg8000`, SQLAlchemy, Django ORM
- Read and write access to Snowflake tables
- Supports transactions, prepared statements, parameterized queries
- Works with any Postgres client library in any language (Python, Node.js, Go, Java, etc.)
- Managed by Snowflake — no server to provision, patch, or scale

**Learn more:**
- [Snowflake Postgres Product Page](https://www.snowflake.com/en/product/features/postgres/)
- [Postgres Data Mirroring Blog](https://www.snowflake.com/en/blog/postgres-data-mirroring/)
""")

    # ── Migration Path ────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">4</span> Migration Path for Connor Group Apps</h2>', unsafe_allow_html=True)
    st.markdown("""
**Phase 1 — Prove it out (1 app, read-only)**
1. Create a Snowflake Postgres instance
2. Pick the simplest reporting app (read-only, no user input)
3. Change the connection string from Sevalla Postgres → Snowflake Postgres
4. Validate: correct data, acceptable latency, no code changes needed

**Phase 2 — Add write-back**
1. Pick an app with user input (CRUD)
2. Test INSERT/UPDATE operations via the Postgres endpoint
3. Verify data lands correctly in Snowflake tables

**Phase 3 — Migrate remaining apps**
1. Systematically move apps off Sevalla Postgres
2. Decommission the hourly sync job
3. Drop KINSTA_WH (or repurpose)

**Phase 4 — Decommission Sevalla Postgres**
1. Cancel the external Postgres hosting
2. All apps now read/write directly to Snowflake via Postgres protocol
""")

    st.code("""
-- Create a Snowflake Postgres instance
CREATE POSTGRES INSTANCE connor_apps_pg
  WAREHOUSE = COMPUTE_WH;

-- Your apps connect with standard psycopg2:
-- import psycopg2
-- conn = psycopg2.connect(
--     host="<account>.snowflakecomputing.com",
--     port=5432,
--     database="<database>",
--     user="<user>",
--     password="<password>"
-- )
""", language="sql")

    # ── Cost Impact ───────────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">5</span> Cost & Operational Impact</h2>', unsafe_allow_html=True)

    cost_data = pd.DataFrame([
        {"Item": "KINSTA_WH (hourly sync)", "Current Cost": "22 credits/95 days", "After Migration": "Eliminated"},
        {"Item": "Sevalla Postgres hosting", "Current Cost": "Monthly hosting fee", "After Migration": "Eliminated"},
        {"Item": "Sync job maintenance", "Current Cost": "Engineering time", "After Migration": "Eliminated"},
        {"Item": "Data staleness", "Current Cost": "Up to 60 min stale", "After Migration": "Live / real-time"},
        {"Item": "Snowflake Postgres compute", "Current Cost": "N/A", "After Migration": "Included in warehouse usage"},
    ])
    st.dataframe(cost_data, use_container_width=True, hide_index=True)

    st.markdown("""
<div class="callout-good">
✅ <strong>Net effect:</strong> Eliminate Sevalla Postgres hosting cost + KINSTA_WH credits + 
sync job maintenance, in exchange for direct Snowflake compute (which you're already paying for). 
Data goes from 60-min stale to live. One fewer system to manage.
</div>
""", unsafe_allow_html=True)

    # ── Why Not Streamlit ─────────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown('<h2><span class="section-num">6</span> Why This Fits (and Why Streamlit Didn\'t)</h2>', unsafe_allow_html=True)
    st.markdown("""
You evaluated Streamlit and moved away for valid reasons:
- **Cost** — warehouse spin-up for every app interaction
- **Capability** — full-stack apps need custom JS/CSS/HTML that Streamlit can't do
- **Logins** — you didn't want end users needing Snowflake credentials

**Snowflake Postgres solves a different problem entirely:**
- It doesn't replace your web apps — it replaces the **database layer** behind them
- Your Python apps stay on Sevalla exactly as-is
- The only change is the connection string (Sevalla Postgres → Snowflake Postgres)
- End users never interact with Snowflake directly — they still use your web apps
- No new login system, no UI migration, no capability loss
""")
    st.markdown("""
<div class="callout-info">
💡 <strong>Key framing for the conversation:</strong> "We're not asking you to change your apps 
or your UX. We're asking if you'd like to remove the Postgres middleman and let your apps 
talk directly to Snowflake using the same Postgres protocol your apps already speak."
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#969494; font-size:0.85em; padding: 20px 0;">
  Prepared for <strong>The Connor Group</strong> by Snowflake · All syntax verified against current documentation · August 2026
</div>
""", unsafe_allow_html=True)
