# Guidance for Task

This project provides a foundational FastAPI application for a 'User Feedback' admin dashboard. Your task is to build out its core functionality and ensure the requirements are met.

## What You Need to Do
- Implement a FastAPI-powered API supporting user feedback submission and secure admin-only retrieval.
- Maintain all state in memory; feedback must have unique auto-incremented IDs.
- Implement:
  - **User endpoint** for submitting feedback (input validation, simulated confirmation email via `BackgroundTasks`).
  - **Admin endpoint** for listing feedbacks (requires a token query param; supports pagination and email-based filtering).
  - Use separate routers for user and admin, included in the app.
  - Provide robust error handling (including authentication, validation, and general errors).
  - Ensure all endpoints are documented with OpenAPI tags, summaries, and request/response examples.

## What is Already Provided
- Project scaffolding with Docker support.
- Required dependencies and base FastAPI app.

## What is Expected
- Write and document correct API endpoints.
- Implement the simulated background email mechanism without real emails.
- Use in-memory data structures for all storage and implement thread-safe auto-increment IDs.
- Secure the admin endpoint with token-based dependency checks passed as a query parameter.
- Provide OpenAPI examples for requests and responses.
- Ensure comprehensive error handling.

## Verifying Your Solution
- Confirm that a user can POST feedback on `/feedback/submit` and see a simulated confirmation action.
- Check that incorrect or incomplete feedback submissions result in validation errors.
- Verify that the `/admin/feedbacks` endpoint enforces authentication, supports filtering via `email`, and handles pagination.
- Interact with `/docs` to ensure API tags, summaries, and examples are complete and clear.
- Test that error responses are informative and standards-compliant.

*Note: Do not add any persistent database or actual email integration. Everything must stay in-memory and use simulated operations only.*
