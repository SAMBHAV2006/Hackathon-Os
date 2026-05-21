# HackOS
To resolve these inefficiencies, this project proposes a comprehensive Hackathon Management Database System. This system serves as the digital backbone of the event, providing a unified, normalized, and relational framework to manage every logistical and participant-facing component.

Here is a comprehensive `README.md` file for the HackOS project based on the provided code and database.

```markdown
# HackOS — Hackathon Management System 🚀

HackOS is a lightweight, full-stack web application designed to manage hackathons, participants, staff, projects, and resources. It features a sleek, dark-themed user interface and a robust relational database back-end.

## ✨ Features

* **🏛️ Admin Dashboard:** Track total events, view upcoming/ongoing/completed hackathons, and monitor financial transactions.
* **👤 Participant Portal:** Allow users to register for events and browse a live directory of team projects and their statuses.
* **🔧 Staff Operations:** View staff rosters, assigned shifts, and manage the real-time availability status of physical and digital resources.
* **💾 Auto-Initializing Database:** The system automatically builds and seeds the SQLite database with mock data on the first run.
* **🎨 Cyberpunk Aesthetic:** Custom dark-mode UI with grid noise textures, glow effects, and responsive Tailwind CSS layouts.

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, Vanilla JavaScript, Tailwind CSS (via CDN), Google Fonts (Space Mono, Syne).
* **Backend:** Python, Flask (RESTful API).
* **Database:** SQLite3.

## 📂 Project Structure

Ensure your files are structured exactly like this before running the application:

```text
hackos/
│
├── main.py              # Flask server and API endpoints
├── hackathon.db         # SQLite database (Auto-generated if missing)
└── templates/
    └── index.html       # Frontend SPA (Single Page Application)
```

## 🚀 Getting Started

### Prerequisites
* Python 3.7+ installed on your machine.
* `pip` (Python package installer).

### Installation & Setup

1.  **Clone or download** the project files.
2.  **Organize the files** into the directory structure shown above (make sure `index.html` is inside a folder named `templates`).
3.  **Install dependencies**:
    Open your terminal/command prompt and install Flask:
    ```bash
    pip install Flask
    ```
4.  **Run the application**:
    Navigate to the project root directory and execute the main script:
    ```bash
    python main.py
    ```
5.  **Access the web app**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## 🔌 API Endpoints

The Flask backend provides several RESTful endpoints to interact with the SQLite database:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/hackathons` | Fetches a list of all hackathons and their venue details. |
| `GET` | `/api/transactions` | Fetches all financial transaction logs. |
| `POST` | `/api/participants` | Registers a new participant. Expects a JSON payload. |
| `GET` | `/api/projects` | Fetches all submitted projects, their tech stacks, and team names. |
| `GET` | `/api/staff` | Fetches the staff roster and shift timings. |
| `GET` | `/api/resources` | Fetches the inventory of resources (hardware/software/cloud). |
| `PUT` | `/api/resources/<id>/status` | Toggles a resource's status between "Available" and "In Use". |

## 🗄️ Database Schema Overview

The underlying SQLite database uses a highly relational schema to tie the ecosystem together. Key tables include:

* **Core Entities:** `HACKATHON`, `VENUE`, `PARTICIPANT`, `TEAM`, `PROJECT`, `STAFF`, `RESOURCE`
* **Supporting Entities:** `SPONSOR`, `JUDGE`, `MENTOR`, `TRANSACTION_LOG`
* **Bridge Tables (Many-to-Many):** `TEAM_PARTICIPANT`, `MENTOR_TEAM`, `SPONSOR_HACKATHON`, `RESOURCE_HACKATHON`, `JUDGE_PROJECT`


```
