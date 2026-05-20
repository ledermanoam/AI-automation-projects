# Project Context - agent Test Runner

This is my AI agent workspace. i am using it for creating a test plan and writing automating tests.
We have application that running on Minikube. Use Python + playwright + Pytest to create frontend + backend testing framework to the app. 

# About me
i am QA engineer that have basic code skills in python, i want to build and run automation 
test framework to the web application that running on Minikube.

# Rules 

- Before writing ANY test, read `docs/TEST_PLAN.md`.
- Create basic and clear code in python with explanations in page object model + basic playwright framework.
- Create documentation about the code with explanations.
- Create MD file with description and documentation about the test framework in notion in this link:https://www.notion.so/AI-Agents-3320f6c540d280758cf0cc9166d7ad49?source=copy_link.





# Project Context : agent Test Runner + Notion Reporter

### Purpose
Run the Playwright test suite and publish a Pass/Fail summary to Notion.

### Stack
- pytest-playwright (Python)
- Notion API (already configured)

### Inputs
- Test files: `tests/` folder
- Notion API key: stored in `.env` as `NOTION_API_KEY`
- Notion page/database ID: stored in `.env` as `NOTION_DATABASE_ID`

### Expected Output
A new entry in the Notion database with:
- Date and time of the run
- Total tests: X
- Passed: X
- Failed: X
- List of failed test names (if any)

### File to create
`agents/runner_agent.py`

### Notes
- Use `pytest --json-report` to capture results as JSON
- Parse the JSON and push to Notion via their REST API
- No screenshots needed, summary only
```
