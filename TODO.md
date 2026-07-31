# Project TODO List

This file tracks future tasks, incomplete implementations, and refactoring opportunities for the Transport Booking Agent project.

## High Priority - Security

- **Implement Backend Token Validation**:
  - The FastAPI backend must be updated to validate the Google ID `id_token` sent in the `Authorization` header.
  - This is a critical security measure to protect the `/chat` endpoint and ensure requests are from authenticated users.
  - A library like `google-auth` can be used to verify the token against Google's public keys.

## Medium Priority - Core Functionality

- **Complete `BookingService` Implementation**:
  - The current `BookingService` uses a dummy implementation that returns a hardcoded booking ID (`GEN12345`).
  - This should be replaced with logic that interacts with actual transport provider APIs or a database.

- **Configure Google Client ID**:
  - The `index.html` file has a placeholder `YOUR_CLIENT_ID.apps.googleusercontent.com`. This needs to be replaced with a real OAuth 2.0 Client ID from the Google Cloud Console for the login functionality to work.

## Low Priority - Code Quality & Refactoring

- **Consolidate Duplicate Code**:
  - The project contains multiple identical files (e.g., `app.py`, `services/booking.py`) in different directories (`src`, `agents`, `docs`).
  - These should be consolidated into a single source of truth within the `src` directory to improve maintainability and reduce bugs.

- **Improve Test Structure**:
  - Consider separating API tests (for FastAPI endpoints) from unit tests for services (like `BookingService`).
  - For example, create `tests/api/` and `tests/services/` directories to better organize the test suite.