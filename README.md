# Transport Booking Agent

This project implements an AI-powered Transport Booking Agent. For a detailed description of the project, its features, and architecture, please see the technical specification in `docs/SPEC.md`.

## Directory Contents

*   `requirements.txt`: Python dependencies for the project.
*   `src/`: Contains the main application source code.
    *   `transport_booking_agent/`: The main Python package.
        *   `app.py`: The main FastAPI application entry point.
        *   `models.py`: Pydantic and data models for the application state.
        *   `graph/`: Contains the core graph orchestration logic.
            *   `orchestrator.py`: Defines and compiles the LangGraph workflow.
            *   `nodes.py`: Implementation of each node in the graph.
        *   `services/`: Contains the implementation of various specialized services.
            *   `recognition.py`: Recognizes transport mode and provider.
            *   `parsing.py`: Extracts structured information from user text.
            *   `search/`: Specialized search services for flights, trains, and buses.
            *   `filtering.py`: Filters and ranks search results.
            *   `booking.py`: Executes the final booking.
            *   `user_profile.py`: Manages user data.
            *   `guardrail.py`: Enforces safety and security policies.
        *   `templates/`: HTML templates for the FastAPI application.
*   `kubernetes-manifests/`: Kubernetes YAML files for deployment.
*   `docs/SPEC.md`: Detailed technical specifications and architecture.

## Authentication

This application uses Google OAuth 2.0 for user authentication. All API requests must include a valid Google ID token in the `Authorization` header as a Bearer token.

The server validates the token with Google and uses it to identify the user.

## Getting Started (Local Development)

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd transport-booking-agent
    ```
2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv .venv
    ./.venv/Scripts/activate # On Windows
    source ./.venv/bin/activate # On macOS/Linux
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Environment Variables**:
    You must set your Google Client ID as an environment variable.
    ```bash
    # On Windows (Command Prompt)
    set GOOGLE_CLIENT_ID=<YOUR_GOOGLE_CLIENT_ID>

    # On Windows (PowerShell)
    $env:GOOGLE_CLIENT_ID="<YOUR_GOOGLE_CLIENT_ID>"

    # On macOS/Linux
    export GOOGLE_CLIENT_ID=<YOUR_GOOGLE_CLIENT_ID>
    ```
    _Replace `<YOUR_GOOGLE_CLIENT_ID>` with your actual Google Client ID._

5.  **Run the FastAPI application**:
    ```bash
    uvicorn src.transport_booking_agent.app:app --host 0.0.0.0 --port 8080
    ```
    The application will be accessible at `http://localhost:8080`.

## Deployment to Kubernetes (GKE)

1.  **Build Docker Image**:
    ```bash
    docker build -t transport-booking-agent:latest .
    # Tag and push to your container registry (e.g., Google Container Registry)
    # docker tag transport-booking-agent:latest gcr.io/<YOUR_PROJECT_ID>/transport-booking-agent:latest
    # docker push gcr.io/<YOUR_PROJECT_ID>/transport-booking-agent:latest
    ```
    _Remember to replace `<YOUR_PROJECT_ID>` with your Google Cloud Project ID._

2.  **Apply Kubernetes Manifests**:
    ```bash
    kubectl apply -f kubernetes-manifests/
    ```

3.  **Access the Application**:
    Once deployed, get the external IP of the LoadBalancer service:
    ```bash
    kubectl get services transport-booking-agent-external
    ```
    Access the application using the `EXTERNAL-IP` shown in the output.
