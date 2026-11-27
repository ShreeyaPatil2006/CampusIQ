# CampusIQ – AI-Powered College Information Assistant

CampusIQ is a college information platform designed to make academic and campus-related information easier to access. It combines a modern college website with an AI-powered FAQ assistant that answers student queries using a college knowledge base.

The project explores practical applications of Artificial Intelligence, including Retrieval-Augmented Generation (RAG), semantic search, vector embeddings, and knowledge representation.

## Features

### College Website
- Modern, responsive college website interface.
- Sections for Home, About, Academics, Admissions, Student Resources, Notices, and Contact.
- College information displayed through a centralized backend API.

### AI-Powered FAQ Assistant
- Answers questions about college-related topics.
- Uses a structured FAQ knowledge base.
- Supports semantic retrieval using text embeddings.
- Integrates Google's Gemini API.
- Includes a TF-IDF fallback retrieval mechanism.
- Provides a fallback response when relevant information cannot be found.

### Knowledge Base
- Sample college FAQs.
- Department and course information.
- Announcements.
- Semantic entities and relationships.

### Admin Functionality
- Admin authentication.
- FAQ management.
- Announcement management.
- Knowledge entity and relationship management.
- Unanswered query tracking.

## AI Concepts Used

| Concept | Application |
|---|---|
| Knowledge Base | Stores college FAQs and information |
| Semantic Search | Retrieves information based on meaning |
| Vector Embeddings | Represents text as numerical vectors |
| Cosine Similarity | Measures similarity between query and FAQ embeddings |
| Retrieval-Augmented Generation (RAG) | Retrieves relevant information before generating an answer |
| TF-IDF | Lightweight fallback retrieval method |
| Knowledge Representation | Organizes entities and relationships |

## Technology Stack

**Frontend**
- React
- JavaScript
- CSS

**Backend**
- Python
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- SQLite

**Artificial Intelligence**
- Google Gemini API
- Gemini Embeddings (`gemini-embedding-001`)
- Scikit-learn
- NumPy
- TF-IDF

**Authentication and Configuration**
- PyJWT
- Python-dotenv

## Project Structure

```text
CampusIQ/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   │   ├── retrieval.py
│   │   │   └── rag.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── seed.py
│   │   ├── extensions.py
│   │   └── __init__.py
│   │
│   ├── instance/
│   ├── .env
│   ├── requirements.txt
│   └── run.py
│
└── frontend/
    ├── src/
    ├── public/
    └── package.json
```

*Note: This is a simplified representation of the project structure.*

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CampusIQ.git
cd CampusIQ
```

### 2. Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file inside the `backend` directory:

```env
GEMINI_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///campusiq.db
FRONTEND_ORIGIN=http://localhost:5173
```

Replace the placeholder values with your own credentials.

**Important:** Never upload your `.env` file or expose API keys and secret credentials in your repository.

### 4. Start the Backend

From the `backend` directory:

```bash
python run.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

Health check:

```text
http://127.0.0.1:5000/api/health
```

### 5. Frontend Setup

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local frontend URL:

```text
http://localhost:5173
```

Keep both the backend and frontend terminals running while using the application.

## API Endpoints

The backend exposes REST API endpoints under `/api`.

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/health` | GET | Backend health check |
| `/api/content` | GET | Retrieve website content |
| `/api/faqs` | GET | Retrieve FAQs |
| `/api/departments` | GET | Retrieve departments |
| `/api/courses` | GET | Retrieve courses |
| `/api/announcements` | GET | Retrieve announcements |
| `/api/chat` | POST | Process assistant queries |
| `/api/auth/login` | POST | Admin authentication |

Additional admin endpoints support managing FAQs, announcements, entities, relationships, and unanswered queries.

## Current Project Status

**Development version – Work in Progress**

Implemented:
- College website frontend.
- Flask backend and REST API.
- SQLite database initialization and sample data seeding.
- FAQ retrieval system.
- Gemini embedding integration.
- TF-IDF fallback retrieval.
- AI assistant interface.
- Admin-related backend endpoints.

Planned improvements:
- Expand and verify the college knowledge base.
- Improve semantic retrieval accuracy.
- Test and refine RAG response generation.
- Improve admin dashboard functionality.
- Add more robust error handling and testing.
- Deploy the application.

## Important Note

The current knowledge base contains sample/demo college information. Responses should not be treated as verified official college policies or academic information.

## Learning Outcomes

This project provides practical experience with:
- Full-stack web development.
- REST API development using Flask.
- Database integration.
- AI-powered information retrieval.
- Semantic search and embeddings.
- Retrieval-Augmented Generation.
- Integration of external AI APIs.

## Author

Developed as an academic and learning project exploring AI-powered college information systems.

---

**CampusIQ – Making College Information Accessible.**