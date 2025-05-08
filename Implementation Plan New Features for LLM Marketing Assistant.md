# **Implementation Plan: New Features for LLM Marketing Assistant**

This plan details the steps required to integrate the requested new features (Protocol Templatization, Interaction Modes, Image Generation, Relevancy Fact Generation, Exana Example) into the existing LLM Marketing Assistant project.

*(Steps continue from the existing plan, assuming Steps 1-23 are complete)*

## **Section: Protocol Templatization & Configuration**

-   [ ] **Step 24: Enhance Configuration for Protocol Selection**

-   **Task**: Modify the configuration system (src/config/settings.py) to recognize and manage an ACTIVE_PROTOCOL setting. This setting, likely driven by an environment variable (e.g., ACTIVE_PROTOCOL=yieldfi), will determine which protocol's specific data (knowledge, prompts, categories) the application loads. Implement a helper function get_protocol_data_path(subpath) to construct file paths relative to the active protocol's data directory (e.g., data/protocols/yieldfi/knowledge.json). Ensure load_config identifies the active protocol early.
-   **Files**:

-   src/config/settings.py
-   .env.example
-   .env
-   config.yaml
-   tests/config/test_settings.py

-   **Step Dependencies**: Step 5 (Existing Config System)
-   **User Instructions**: Define the ACTIVE_PROTOCOL environment variable in your .env file (e.g., ACTIVE_PROTOCOL=yieldfi). Review the updated configuration loading logic.

-   [ ] **Step 25: Restructure Data for Protocol Templatization**

-   **Task**: Reorganize the data/ directory to support multiple protocols. Create a base data/protocols/ directory. Move all current YieldFi-specific files (categories.json, yieldfi_knowledge.json, InstructionsFor*.md, docs.yield.fi.md) into a new data/protocols/yieldfi/ subdirectory, potentially renaming files for consistency (e.g., yieldfi_knowledge.json -> knowledge.json, docs.yield.fi.md -> docs.md, placing instructions in data/protocols/yieldfi/instructions/). Update all modules that load these files (src/models/category.py, src/knowledge/yieldfi.py, src/ai/prompt_engineering.py) to use the new get_protocol_data_path() helper function from Step 24, ensuring they dynamically load data for the ACTIVE_PROTOCOL.
-   **Files**:

-   src/models/category.py
-   src/knowledge/yieldfi.py (Consider renaming YieldFiDocsKnowledgeSource to generic MarkdownDocsKnowledgeSource)
-   src/ai/prompt_engineering.py
-   (Move existing data files from data/input and data/docs to data/protocols/yieldfi/)
-   tests/ (Relevant test files might need mock path updates)

-   **Step Dependencies**: Step 24
-   **User Instructions**: Verify the directory structure changes. Run the application with ACTIVE_PROTOCOL=yieldfi and confirm it loads and functions correctly using the data from the new location.

## **Section: Interaction Modes**

-   [ ] **Step 26: Define Mode Model and Data Structure**

-   **Task**: Introduce the concept of interaction "Modes". Create a Mode dataclass in src/models/mode.py (with fields like name, description, system_prompt, additional_instructions). Create a modes.json file within each protocol's data directory (start with data/protocols/yieldfi/modes.json) defining modes like "Default", "Professional", "Degen", each with appropriate system prompts and descriptions. Implement a utility function (e.g., in src/models/mode.py) to load the available modes for the currently active protocol.
-   **Files**:

-   src/models/mode.py (new)
-   src/models/__init__.py (updated)
-   data/protocols/yieldfi/modes.json (new)
-   src/utils/mode_loader.py (optional, or add loader to mode.py)

-   **Step Dependencies**: Step 25
-   **User Instructions**: Populate data/protocols/yieldfi/modes.json with distinct and effective system prompts for each mode, paying particular attention to crafting a suitable prompt for the "Degen" mode.

-   [ ] **Step 27: Integrate Modes into Prompt Engineering**

-   **Task**: Modify the prompt generation functions in src/ai/prompt_engineering.py (generate_interaction_prompt, generate_new_tweet_prompt) to accept an optional mode: Mode object. When a mode is provided, its system_prompt should be prepended to the overall prompt structure, and any additional_instructions from the mode should be merged with or prioritized over other contextual instructions (e.g., from categories).
-   **Files**:

-   src/ai/prompt_engineering.py
-   tests/ai/test_prompt_engineering.py

-   **Step Dependencies**: Step 7, Step 18, Step 26
-   **User Instructions**: Review how the mode's system prompt and instructions are integrated into the final LLM prompts for different scenarios. Verify the logic for merging/prioritizing instructions.

-   [ ] **Step 28: Add Mode Selection to UI**

-   **Task**: Enhance the Streamlit UI to allow users to select an interaction mode. Add a dropdown (st.selectbox) in the sidebar (app.py) or relevant UI sections (tweet_input.py, category_select.py) populated with the modes loaded for the ACTIVE_PROTOCOL. Pass the selected Mode object from the UI down to the response_generator functions (generate_tweet_reply, generate_new_tweet). Update the response generator function signatures to accept the mode parameter.
-   **Files**:

-   app.py
-   src/ui/tweet_input.py
-   src/ui/category_select.py
-   src/ai/response_generator.py

-   **Step Dependencies**: Step 14, Step 15, Step 19, Step 26, Step 27
-   **User Instructions**: Run the Streamlit app. Verify the mode selection dropdown appears and is populated correctly based on the active protocol's modes.json. Test generating responses with different modes selected and observe if the output style changes as expected based on the mode's system prompt.

## **Section: Image Generation**

-   [ ] **Step 29: Implement Image Generation Backend (Mock)**

-   **Task**: Set up the backend infrastructure for optional image generation. Create an abstract ImageGenerator class (src/ai/image_generator.py) with a generate_image(prompt) method, and implement a MockImageGenerator that returns placeholder image data (e.g., bytes of a small, default image). Create an abstract StorageUploader class (src/utils/storage.py) with an upload(image_bytes, filename) method, and implement a MockStorageUploader that returns a fake URL (e.g., https://placehold.co/600x400/EEE/31343C?text=Mock+Image). Add image_url: Optional[str] to the AIResponse model (src/models/response.py). Modify src/ai/response_generator.py functions to accept a generate_image: bool flag. If true, construct an image prompt, call the (mock) generator and uploader, and populate response.image_url. Define necessary config keys/env vars for real API keys/storage, but use mocks for now.
-   **Files**:

-   src/ai/image_generator.py (new)
-   src/utils/storage.py (new)
-   src/models/response.py (updated)
-   src/ai/response_generator.py (updated)
-   .env.example (updated with placeholder keys for image/storage)
-   config.yaml (updated with placeholder keys/config sections)
-   tests/ai/test_response_generator.py (updated)

-   **Step Dependencies**: Step 5, Step 9
-   **User Instructions**: Review the structure for image generation and storage. The mock implementations should allow testing the flow without real API keys. *Actual implementation of non-mock ImageGenerator and StorageUploader requires separate effort based on chosen services.*

-   [ ] **Step 30: Integrate Image Generation into UI**

-   **Task**: Add UI elements to control and display image generation. Include an st.checkbox("Generate Poster Image?") in the relevant UI sections (src/ui/tweet_input.py, src/ui/category_select.py). Pass the state of this checkbox to the backend response_generator functions. When displaying the AIResponse, check if response.image_url exists. If it does, display the image using st.image(response.image_url) and provide a button to copy the URL.
-   **Files**:

-   src/ui/tweet_input.py (updated)
-   src/ui/category_select.py (updated)

-   **Step Dependencies**: Step 16, Step 29
-   **User Instructions**: Test the UI checkbox. Verify that when checked, the (mock) image URL is generated and the image (placeholder) is displayed in the response area along with its URL and copy button.

## **Section: Relevancy Fact Generation**

-   [ ] **Step 31: Implement Relevancy Fact Generation**

-   **Task**: Enhance the AI's output to include a concise "Relevancy Fact". Modify the prompt structures in src/ai/prompt_engineering.py to instruct the LLM to provide a one-sentence summary or key fact related to the main response, marked with a specific prefix (e.g., "Fact:"). Update the parsing logic in src/ai/response_generator.py to detect this marker, extract the fact, and store it separately from the main content. Add a relevancy_fact: Optional[str] field to the AIResponse model (src/models/response.py). Update the UI (src/ui/tweet_input.py, src/ui/category_select.py) to display this extracted relevancy_fact distinctly below the main generated content (e.g., using st.caption or st.info).
-   **Files**:

-   src/ai/prompt_engineering.py (updated)
-   src/ai/response_generator.py (updated)
-   src/models/response.py (updated)
-   src/ui/tweet_input.py (updated)
-   src/ui/category_select.py (updated)
-   tests/ai/test_response_generator.py (updated)

-   **Step Dependencies**: Step 9, Step 16, Step 27 (prompts modified)
-   **User Instructions**: Test generating responses for various inputs. Check if a relevancy fact is consistently generated, extracted correctly, and displayed separately in the UI. Refine the prompt instructions if the LLM struggles with this task.

## **Section: Exana Example & Documentation**

-   [ ] **Step 32: Create Exana Protocol Example**

-   **Task**: Demonstrate the protocol templatization by creating an example setup for a hypothetical "Exana" protocol. Create the directory data/protocols/exana/. Inside this directory, create placeholder files mirroring the YieldFi structure: categories.json, knowledge.json, modes.json, docs.md, and an instructions/ subdirectory with at least one example instruction file (e.g., InstructionsForOfficialToPartner.md). Populate these files with simple, distinct content relevant to the imaginary Exana protocol.
-   **Files**:

-   data/protocols/exana/categories.json (new)
-   data/protocols/exana/knowledge.json (new)
-   data/protocols/exana/modes.json (new)
-   data/protocols/exana/instructions/InstructionsForOfficialToPartner.md (new)
-   data/protocols/exana/docs.md (new)

-   **Step Dependencies**: Step 25 (Templatization structure)
-   **User Instructions**: Populate the new Exana files with basic but representative content. Test the application by setting ACTIVE_PROTOCOL=exana in .env, restarting the app, and verifying that it loads Exana's categories, modes, and uses its specific knowledge/instructions during generation.

-   [ ] **Step 33: Update Documentation**

-   **Task**: Update all user-facing and developer documentation (README.md, docs/usage.md, docs/api.md, docs/deployment.md) to comprehensively cover the newly added features and architectural changes. Include sections on: how to select the active protocol, how to configure and use interaction modes, the image generation option (including backend setup requirements), the display of relevancy facts, and a guide on how to onboard a new protocol by creating its data directory and configuration files.
-   **Files**:

-   README.md
-   docs/usage.md
-   docs/api.md
-   docs/deployment.md

-   **Step Dependencies**: Steps 24-32
-   **User Instructions**: Review all updated documentation sections for clarity, accuracy, and completeness, ensuring they accurately reflect the new features and how to use/configure them.