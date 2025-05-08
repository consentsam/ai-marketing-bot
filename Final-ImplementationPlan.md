
# Final Unified Implementation Plan (Modular, With Verification Steps)

## Step 20: Comprehensive Automated Testing

**Overview**  
Add or expand tests to cover newly introduced features:
- Image generation  
- Interaction modes  
- Relevancy facts  
- Multi-protocol loading  

### Task Details
1. **Add test modules**  
   - `tests/ai/test_image_generation.py`  
   - `tests/ai/test_relevancy.py`  
   - `tests/test_protocol_templatization.py`  
   - Update existing `test_prompt_engineering.py` and `test_response_generator.py`  
2. **Mock external APIs** (image generation, ephemeral hosting)  
3. **Introduce fixtures** for sample tweets, accounts, modes  

### Affected Files
- **New**:  
  - `tests/ai/test_image_generation.py`  
  - `tests/ai/test_relevancy.py`  
  - `tests/test_protocol_templatization.py`  
- **Updates**: existing tests in `ai/test_response_generator.py`, etc.  

### Implementation Strategy
- Use `unittest.mock` or `pytest-mock` to stub image-generator calls  
- Override `DEFAULT_PROTOCOL` to `"exana"` or `"ethena"` within test scope  
- Verify coverage with `pytest --cov`  

### Edge Cases / Error Handling
- Missing environment variables for image API or hosting  
- Non-existent protocol directories  

### Verification Steps
1. Run `pytest --maxfail=1 --disable-warnings` → all tests pass  
2. Confirm new modules appear in coverage report  
3. Ensure no real external calls (mocks intercept)  

### Summary  
> *(To be filled when complete—for example: "Coverage reached 83%. Fixed KeyError in `image_generation.py`.)*  

---

## Step 21: Evaluation Framework

**Overview**  
Measure tone adherence, factual correctness, and other quality metrics.

### Task Details
1. Create `src/evaluation/metrics.py` with scoring functions (e.g., `tone_match_score`, `relevance_score`)  
2. Create `src/evaluation/evaluator.py` to run metrics against stored AI responses or a golden set  

### Affected Files
- `src/evaluation/metrics.py`  
- `src/evaluation/evaluator.py`  

### Implementation Strategy
- Define focused scoring functions in `metrics.py`  
- Aggregate results or compare via CSV in `evaluator.py`  

### Edge Cases / Error Handling
- Skip or partial-score when ground-truth references are missing  

### Verification Steps
1. Add golden-set test comparing AI output vs. expected string  
2. Output metrics in table or JSON  

### Summary  
> *(To be filled—for example: "Created `metrics.py`. tone_match_score ~0.75 on test #1.")*  

---

## Step 22: Containerization & Deployment Scripts

**Overview**  
Dockerize the app and provide simple deployment scripts.

### Task Details
1. **Dockerfile**  
   - Base `python:3.9-slim`  
   - Copy code, install dependencies, run Streamlit  
2. **docker-compose.yml**  
   - Define service, map port 8501  
3. **scripts/deploy.sh**  
   - Build and run examples  

### Affected Files
- `Dockerfile`  
- `docker-compose.yml`  
- `scripts/deploy.sh`  

### Implementation Strategy
- Keep minimal—extend for Kubernetes later  
- Test locally with `docker-compose up --build`  

### Edge Cases / Error Handling
- Do not copy `.env` into image  
- Validate logging configuration  

### Verification Steps
1. `docker-compose build` → no errors  
2. `docker-compose up` → accessible at `http://localhost:8501`  
3. Confirm image gen, modes, etc., work inside container  

### Summary  
> *(To be filled—for example: "Container started on port 8501; deployed to staging.")*  

---

## Step 23: Documentation & Final Updates

**Overview**  
Update README and docs for new features and protocols.

### Task Details
1. **README.md**: document new env vars (e.g., `GROK_IMAGE_API_KEY`)  
2. **docs/usage.md**: guide for image gen, mode selection, protocol switch  
3. **docs/api.md**: document `AIResponse.image_url`, `AIResponse.relevancy_fact`  
4. **docs/deployment.md**: Docker usage  

### Affected Files
- `README.md`  
- `docs/usage.md`  
- `docs/api.md`  
- `docs/deployment.md`  

### Implementation Strategy
- Include screenshots or code snippets  
- Summarize config keys clearly  

### Edge Cases / Error Handling
- Avoid exposing secrets in docs  
- Ensure docs mirror file structure  

### Verification Steps
1. New dev follows docs from scratch  
2. Confirm environment and features work as described  
3. Fix missing or outdated references  

### Summary  
> *(To be filled—for example: "Docs updated and validated on a fresh machine.")*  

---

## Step 24: Image Generation (Detailed)

### (a) Backend Implementation
1. **Create** `src/ai/image_generation.py`:
   ```python
   def get_poster_image(prompt: str) -> str:
       # call grok-2-image API; return URL
   ```
2. **Extend** `AIResponse` in `src/models/response.py`:
   ```python
   image_url: Optional[str] = None
   ```
3. **Modify** `generate_tweet_reply()` and `generate_new_tweet()`:
   - Accept `generate_image: bool`
   - If `True`, call `get_poster_image()` and set `ai_response.image_url`

**Verification (Backend)**
1. Mock `get_poster_image` to return a fixed URL  
2. Assert `AIResponse.image_url` is populated  

### (b) UI Integration
1. Add `st.checkbox("Generate Poster Image")` in:
   - `src/ui/tweet_input.py`  
   - `src/ui/category_select.py`  
2. Pass checkbox state to response generator  
3. If `AIResponse.image_url` exists, display via `st.image()` and add a “Copy URL” button  

**Verification (UI)**
1. Box unchecked → `image_url` remains `None`  
2. Box checked → preview appears; copy works  

### Summary  
> *(To be filled—for example: "Image generation tested end-to-end.")*  

---

## Step 25: Interaction Modes & Improved Prompts

**Overview**  
Allow prompt styling by mode: Default, Professional, Degen.

### (a) Mode Data & Loading
1. Populate `data/protocols/<protocol>/mode-instructions/` with:
   - `InstructionsForDefault.md`  
   - `InstructionsForProfessional.md`  
   - `InstructionsForDegen.md`  
2. Add helper in `settings.py` or `prompt_engineering.py`:
   ```python
   def load_mode_instructions(mode: str) -> str: ...
   ```

**Verification**
- Degen mode includes slang (“gm”)  
- Missing file falls back gracefully  

### (b) Prompt Integration
1. In `prompt_engineering.py`, merge mode instructions with base persona  
2. Optionally:
   ```python
   def generate_mode_prompt(mode: str, base_prompt: str) -> str: ...
   ```

**Verification**
- Unit tests confirm presence of mode text  

### (c) UI Mode Selection
1. Add `st.selectbox("Interaction Mode", ["Default","Professional","Degen"])`  
2. Pass selection to generator  

**Verification**
- UI changes reflect in reply style  
- Logs show correct instructions  

### Summary  
> *(To be filled—for example: "Degen mode tested, slang present.")*  

---

## Step 26: Relevancy Fact Generation

**Overview**  
Inject context-based facts into prompts/responses.

### (a) Data & Detection
1. Create `data/input/relevancy_facts.json`:
   ```json
   [
     { "condition": "market down|bearish", "fact": "crypto market is down 20%" },
     { "condition": "after-event|past-event", "fact": "This event already took place." }
   ]
   ```
2. Implement `src/ai/relevancy.py`:
   ```python
   def get_facts(tweet: Tweet) -> List[str]: ...
   ```

**Verification**
- Tweet containing “bearish” yields market-down fact  
- No match → skip injection  

### (b) Prompt / Response Integration
1. Call `get_facts()` in `generate_tweet_reply()`  
2. Append `**Relevancy facts**: [fact1, fact2]` to prompt  

**Verification**
- Tests confirm facts appended when conditions met  

### Summary  
> *(To be filled—for example: "Market-down fact appears for bearish tweets.")*  

---

## Step 27: Protocol Templatization

**Overview**  
Load data according to `DEFAULT_PROTOCOL`.

### (a) Directory Refactor
1. Move existing Ethena data into `data/protocols/ethena/`  
2. Update paths in:
   - `src/knowledge/*.py`  
   - `src/models/category.py`  
   - `src/ai/prompt_engineering.py`  

### (b) Config & Settings
1. Set `DEFAULT_PROTOCOL=ethena` in `.env` or `config.yaml`  
2. Add helper in `settings.py`:
   ```python
   def get_protocol_path(*parts) -> Path: ...
   ```

**Verification**
1. With `ethena`, load Ethena data  
2. Other protocols → fallback or load if available  

### Summary  
> *(To be filled—for example: "Protocol switching tested with no path errors.")*  

---

## Step 28: Alternate Protocol Example

**Overview**  
Demonstrate adding a second protocol (e.g., Exana or YieldFi).

### (a) Directory & Files
- Create `data/protocols/exana/` with:
  - `categories.json`  
  - `knowledge.json`  
  - `docs.md`  
  - `mode-instructions/`  

### (b) Testing
1. Set `DEFAULT_PROTOCOL=exana`  
2. Verify data and instructions load correctly  

**Verification**
- Categories and knowledge differ from Ethena  
- End-to-end generation uses new protocol  

### Summary  
> *(To be filled—for example: "Switched to Exana; verified responses use Exana data.")*  

---

# Final Notes

1. **Modularity**: Keep each step in discrete commits.  
2. **Verification**: Every step includes clear checks.  
3. **Documentation**: Update docs alongside code.  
4. **Outcome**: After Step 28, you’ll have:

   - Image generation  
   - Multiple interaction modes  
   - Relevancy fact injection  
   - Multi-protocol support  
   - Robust tests  
   - Up-to-date documentation  
   - Containerized deployment  

This unified plan ensures a modular, testable, and maintainable LLM-driven assistant that’s easy to extend with future protocols and features.
