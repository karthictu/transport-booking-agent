# Transport Booking Agent - Implementation Details

This document provides detailed implementation specifics for the AI-powered Transport Booking Agent. For a high-level overview of the architecture, please see [`SPEC.md`](./SPEC.md).

## 1. Service Specifications

### 1.1. GraphOrchestrator
*   **Purpose**: The central coordinator. It uses a Langgraph graph to manage the flow of control between specialist agents.
*   **Input**: User's natural language message (string).
*   **Output**: A user-facing response message (string).
*   **Structure**: The graph's structure is defined in `graph_orchestrator.py`, while the logic for each node in the graph resides in `graph_nodes.py`.
*   **Logic**:
    1.  Initialize the agent graph.
    2.  The graph starts by getting the user profile and then checking the request against guardrails.
    3.  If guardrails pass, it recognizes the transport mode and provider.
    4.  It then routes to the appropriate search agent based on the recognized mode.
    5.  The rest of the flow for filtering, ranking, presenting results, and booking remains the same.

### 1.2. Guardrail Service
*   **Purpose**: To enforce safety and security policies.

### 1.3. Recognition Service
*   **Purpose**: To identify the transport mode and provider from the user's message.

### 1.4. Parsing Service
*   **Purpose**: To extract structured information from unstructured user text.

### 1.5. Search Services
*   **Purpose**: To find available transport options for a specific mode by interfacing with external APIs.
*   **Services**:
    *   `FlightSearchService`
    *   `TrainSearchService`
    *   `BusSearchService`

### 1.6. Filtering Service
*   **Purpose**: To refine and sort search results based on user preferences.

### 1.7. Booking Service
*   **Purpose**: To execute the final booking transaction.
*   **Persistence**: Persists the `BookingConfirmation` to the PostgreSQL database.

### 1.8. User Profile Service
*   **Purpose**: To manage user data for personalization and history.
*   **Persistence**: Retrieves user data from a PostgreSQL database, utilizing a Redis cache to accelerate access to frequently requested profiles.

## 2. Data Models

### StructuredQuery (dict)
```json
{
  "origin": "string",
  "destination": "string",
  "date": "string",
  "passengers": "int",
  "mode": "string (flight, train, bus)",
  "preferences": "list[string] (e.g., 'cheapest', 'business class')"
}
```

### TransportOption (dict)
```json
{
  "type": "string (flight, train, bus)",
  "provider": "string (e.g., 'United Airlines')",
  "departure_time": "datetime",
  "arrival_time": "datetime",
  "price": "float",
  "booking_id": "string"
}
```