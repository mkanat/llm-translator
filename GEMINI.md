## Gemini Added Memories
- This project uses uv for its dependencies and its venv.
- All python commands, including pytest, must be run via uv run.
- To install dependencies, use uv add.
- When parsing XLIFF, our target is to support Trados Studio 2017, which means we support XLIFF 1.2 and SDLXLIFF.
- We use pytest for tests.
- Test data always goes into a subdirectory of the directory where the test is. That subdirectory is named "testdata".