# Transport Booking Agent - Specification

This document outlines the high-level architecture for the AI-powered Transport Booking Agent. For detailed implementation specifics, please refer to [`IMPLEMENTATION_DETAILS.md`](./IMPLEMENTATION_DETAILS.md).

## 1. High-Level Architecture

The system uses a multi-agent architecture orchestrated by **Langgraph**. A central **GraphOrchestrator** manages a graph of specialized agents to fulfill a user's request.

### Data Flow

```mermaid
graph TD
    User -- "Book a flight to Paris" --> A(Graph Orchestrator)
    A -- Invokes Graph --> B(Agent Graph)
    subgraph Agent Graph
        direction LR
        C(Get User Profile) --> D(Guardrail Check)
        D -- Passed --> E(Recognize Mode/Provider)
        D -- Failed --> Z(End)
        E --> F(Parse Query)
        F --> G{Route by Mode}
        G -- Flight --> H(Flight Search)
        G -- Train --> I(Train Search)
        G -- Bus --> J(Bus Search)
        G -- Unsupported --> Z
        H --> K(Filter & Rank)
        I --> K
        J --> K
        K --> L{Should Book?}
        L -- No --> M(Present Results)
        L -- Yes --> N(Book Transport)
        M --> Z
        N --> Z
    end
    B -- "Your flight is booked!" --> User
```

## 2. Agent Specifications

### 2.1. GraphOrchestrator
*   **Purpose**: The central coordinator. It uses a Langgraph graph to manage the flow of control between specialist agents.
*   **Input**: User's natural language message (string).
*   **Output**: A user-facing response message (string).
*   **Structure**: The graph's structure is defined in `src/transport_booking_agent/graph/orchestrator.py`, while the logic for each node in the graph resides in `src/transport_booking_agent/graph/nodes.py`.
*   **Logic**:
    1.  Initialize the agent graph.
    2.  The graph starts by getting the user profile and then checking the request against guardrails.
    3.  If guardrails pass, it recognizes the transport mode and provider.
    4.  It then routes to the appropriate search agent based on the recognized mode.
    5.  The rest of the flow for filtering, ranking, presenting results, and booking remains the same.

### 2.2. Guardrail Service
*   **Purpose**: To enforce safety and security policies.

### 2.3. Recognition Service
*   **Purpose**: To identify the transport mode and provider from the user's message.

### 2.4. Parsing Service
*   **Purpose**: To extract structured information from unstructured user text.

### 2.5. Search Services
*   **Purpose**: To find available transport options for a specific mode by interfacing with external APIs.

### 2.6. Filtering Service
*   **Purpose**: To refine and sort search results based on user preferences.

### 2.7. Booking Service
*   **Purpose**: To execute the final booking transaction.

### 2.8. User Profile Service
*   **Purpose**: To manage user data for personalization and history.

## 3. Data Models

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

## 4. Infrastructure Architecture

This diagram shows the Kubernetes infrastructure setup for deploying the application.

```mermaid
graph TD
    subgraph "User's Device"
        A[Web Browser]
    end

    subgraph "Google Kubernetes Engine Cluster"
        B["transport-booking-agent-external Service (Type: LoadBalancer)"]
        D["transport-booking-agent Deployment"]

        subgraph "Pod(s)"
          C["transport-booking-agent Container"]
        end

        subgraph "Container Details"
            E[FastAPI Web Server]
            G["/ (index.html)"]
            H["/chat (API)"]
        end
    end

    A -- "HTTPS Request" --> B
    D -- "Manages Pod Replicas" --> C
    B -- "Routes Port 80 to 8080" --> C
    C -- "Runs" --> E
    E -- "Serves" --> G
    E -- "Handles" --> H
```