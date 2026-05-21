from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, template_folder='templates')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'hackathon.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db()
        c = conn.cursor()
        c.executescript("""
-- 1. VENUE TABLE
CREATE TABLE VENUE (
    Venue_ID INT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Address VARCHAR(255), City VARCHAR(100), Capacity INT, Facilities VARCHAR(255), Rental_Cost DECIMAL(10, 2)
);
INSERT INTO VENUE VALUES (201, 'Grand Tech Hall', '123 Innovation Dr', 'San Francisco', 500, 'WiFi, AV System', 5000.00),
(202, 'City Convention Center', '456 Market St', 'New York', 2000, 'Large Stage, Catering', 15000.00),
(203, 'Startup Hub', '789 Enterprise Blvd', 'Austin', 300, 'Whiteboards, 24/7 Access', 3000.00),
(204, 'University Auditorium', '101 College Ave', 'Boston', 800, 'Lecture Seating, Labs', 4500.00),
(205, 'The Foundry', '321 Industrial Way', 'Seattle', 400, '3D Printers, Makerspace', 6000.00),
(206, 'Cyber Space', '12 Silicon Alley', 'San Jose', 600, 'High-Speed LAN, Servers', 7000.00),
(207, 'Downtown Expo', '88 Center Sq', 'Chicago', 1500, 'Expo Booths, PA System', 12000.00),
(208, 'Tech Incubator', '42 Garage Ln', 'Palo Alto', 200, 'Podcasting Studio', 2000.00),
(209, 'Global Arena', '1 Arena Pkwy', 'Los Angeles', 3000, 'Stadium Seating, VIP', 25000.00),
(210, 'Virtual Server', 'Online', 'Remote', 5000, 'Discord, Cloud VMs', 1000.00);

-- 2. HACKATHON TABLE
CREATE TABLE HACKATHON (
    Hackathon_ID INT PRIMARY KEY, Title VARCHAR(255) NOT NULL, Start_Date DATE, End_Date DATE, Duration INT, Theme VARCHAR(255), Expected_Participants INT, Status VARCHAR(50), Venue_ID INT, FOREIGN KEY (Venue_ID) REFERENCES VENUE(Venue_ID)
);
INSERT INTO HACKATHON VALUES
(101, 'AI for Good', '2025-11-01', '2025-11-02', 36, 'Artificial Intelligence', 200, 'Upcoming', 201),
(102, 'Fintech Disrupt', '2025-11-15', '2025-11-17', 48, 'Financial Tech', 300, 'Upcoming', 202),
(103, 'CodeJam 2025', '2025-10-28', '2025-10-29', 24, 'Open Source', 150, 'Ongoing', 203),
(104, 'HealthTech Innovate', '2025-12-05', '2025-12-07', 48, 'Healthcare', 250, 'Upcoming', 204),
(105, 'EcoHack', '2025-11-20', '2025-11-21', 24, 'Sustainability', 100, 'Upcoming', 201),
(106, 'CyberSec Challenge', '2025-10-10', '2025-10-12', 48, 'Cybersecurity', 400, 'Completed', 206),
(107, 'Web3 Builders', '2025-12-10', '2025-12-12', 48, 'Blockchain', 500, 'Upcoming', 207),
(108, 'Hardware Hack', '2025-09-01', '2025-09-03', 48, 'IoT', 150, 'Completed', 205),
(109, 'GameDev Sprint', '2025-11-25', '2025-11-27', 48, 'Gaming', 350, 'Upcoming', 209),
(110, 'Cloud Native Clash', '2026-01-05', '2026-01-07', 48, 'Cloud Computing', 1000, 'Upcoming', 210);

-- 3. PARTICIPANT TABLE
CREATE TABLE PARTICIPANT (
    Participant_ID INT PRIMARY KEY, Name VARCHAR(255) NOT NULL, Age INT, Gender VARCHAR(50), Contact VARCHAR(255), Skill_Set VARCHAR(255), Education VARCHAR(255)
);
INSERT INTO PARTICIPANT VALUES
(301, 'Alice Johnson', 22, 'Female', 'alice@email.com', 'Python, Machine Learning', 'BS Computer Science'),
(302, 'Bob Smith', 25, 'Male', 'bob@email.com', 'JavaScript, React, Node.js', 'Web Dev Bootcamp'),
(303, 'Charlie Brown', 20, 'Male', 'charlie@email.com', 'Java, Spring, SQL', 'MS Information Systems'),
(304, 'Dana White', 28, 'Non-binary', 'dana@email.com', 'UI/UX Design, Figma', 'BA Graphic Design'),
(305, 'Eve Davis', 23, 'Female', 'eve@email.com', 'C++, Unreal Engine', 'BS Game Development'),
(306, 'Frank Miller', 21, 'Male', 'frank@email.com', 'Go, Docker, Kubernetes', 'BS Computer Engineering'),
(307, 'Grace Lee', 26, 'Female', 'grace@email.com', 'Python, Data Analytics', 'MS Data Science'),
(308, 'Henry Ford', 24, 'Male', 'henry@email.com', 'Solidity, Rust', 'BS Computer Science'),
(309, 'Ivy Chen', 22, 'Female', 'ivy@email.com', 'HTML, CSS, Vue.js', 'Associate in IT'),
(310, 'Jack Wilson', 27, 'Male', 'jack@email.com', 'AWS, Azure, Terraform', 'Self-Taught');

-- 4. TEAM TABLE
CREATE TABLE TEAM (
    Team_ID INT PRIMARY KEY, Team_Name VARCHAR(255) NOT NULL, Hackathon_ID INT, FOREIGN KEY (Hackathon_ID) REFERENCES HACKATHON(Hackathon_ID)
);
INSERT INTO TEAM VALUES
(401, 'The AI Avengers', 101),(402, 'Cash Coders', 102),(403, 'Commit Kings', 103),
(404, 'Byte Me', 101),(405, 'MediTech', 104),(406, 'Cyber Punks', 106),
(407, 'Blockheads', 107),(408, 'Circuit Breakers', 108),(409, 'Pixel Pushers', 109),(410, 'Cloud Nine', 110);

-- 5. PROJECT TABLE
CREATE TABLE PROJECT (
    Project_ID INT PRIMARY KEY, Title VARCHAR(255) NOT NULL, Description VARCHAR(255), Tech_Stack VARCHAR(255), Submission_Status VARCHAR(50), Team_ID INT, FOREIGN KEY (Team_ID) REFERENCES TEAM(Team_ID)
);
INSERT INTO PROJECT VALUES
(501, 'Predictive Wildfire Model', 'ML to predict wildfires', 'Python, TensorFlow', 'Submitted', 401),
(502, 'Micro-loan App', 'P2P lending platform', 'React Native, Node.js', 'In-Progress', 402),
(503, 'Bug Tracker', 'Decentralized bug tracking', 'Java, PostgreSQL', 'Submitted', 403),
(504, 'Triage Chatbot', 'AI for patient diagnosis', 'Python, Flask', 'In-Progress', 405),
(505, 'AlgoVisualizer', 'Visualizing algorithms', 'JavaScript, D3.js', 'Submitted', 404),
(506, 'Phishing Detector', 'Browser extension for security', 'Python, JS', 'Finalist', 406),
(507, 'NFT Ticketing', 'Event tickets on blockchain', 'Solidity, React', 'In-Progress', 407),
(508, 'Smart Planter', 'IoT plant monitor', 'C++, Arduino', 'Submitted', 408),
(509, 'Retro Racer', '8-bit racing game', 'C#, Unity', 'Finalist', 409),
(510, 'Serverless Scraper', 'Cloud data pipeline', 'AWS Lambda, Python', 'In-Progress', 410);

-- 6. TEAM_PARTICIPANT BRIDGE TABLE
CREATE TABLE TEAM_PARTICIPANT (
    Team_ID INT, Participant_ID INT, PRIMARY KEY (Team_ID, Participant_ID),
    FOREIGN KEY (Team_ID) REFERENCES TEAM(Team_ID), FOREIGN KEY (Participant_ID) REFERENCES PARTICIPANT(Participant_ID)
);
INSERT INTO TEAM_PARTICIPANT VALUES (401,301),(402,302),(403,303),(404,304),(405,305),(406,306),(407,308),(408,305),(409,309),(410,310);

-- 7. MENTOR TABLE
CREATE TABLE MENTOR (Mentor_ID INT PRIMARY KEY, Name VARCHAR(255), Expertise VARCHAR(255), Contact VARCHAR(255));
INSERT INTO MENTOR VALUES (601,'Dr. Alan Turing','AI/ML','alan@email.com'),(602,'Ada Lovelace','Algorithms','ada@email.com'),(603,'Linus Torvalds','OS','linus@email.com');

-- 8. JUDGE TABLE
CREATE TABLE JUDGE (Judge_ID INT PRIMARY KEY, Name VARCHAR(255), Expertise VARCHAR(255), Contact VARCHAR(255));
INSERT INTO JUDGE VALUES (701,'Elon Musk','Innovation','elon@email.com'),(702,'Sam Altman','AI Startups','sam@email.com'),(703,'Sheryl Sandberg','Business Model','sheryl@email.com');

-- 9. SPONSOR TABLE
CREATE TABLE SPONSOR (Sponsor_ID INT PRIMARY KEY, Company_Name VARCHAR(255), Industry_Type VARCHAR(100), Sponsorship_Amount DECIMAL(10,2), Benefits VARCHAR(255));
INSERT INTO SPONSOR VALUES (801,'Google','Tech',50000.00,'Logo on site, API Credits'),(802,'Microsoft','Tech',45000.00,'Azure Credits');

-- 10. STAFF TABLE
CREATE TABLE STAFF (Staff_ID INT PRIMARY KEY, Name VARCHAR(255), Role VARCHAR(100), Shift_Timing VARCHAR(100), Hackathon_ID INT, FOREIGN KEY (Hackathon_ID) REFERENCES HACKATHON(Hackathon_ID));
INSERT INTO STAFF VALUES (901,'Tom Clark','Security','Night',101),(902,'Sarah Jenkins','Coordinator','Day',102);

-- 11. RESOURCE TABLE
CREATE TABLE RESOURCE (Resource_ID INT PRIMARY KEY, Name VARCHAR(255), Type VARCHAR(100), Supplier VARCHAR(255), Cost DECIMAL(10,2), Availability_Status VARCHAR(50));
INSERT INTO RESOURCE VALUES (1001,'Server Rack A','Hardware','Dell',5000.00,'Available'),(1002,'AWS Credits','Cloud','Amazon',10000.00,'Available');

-- 12. TRANSACTION TABLE
CREATE TABLE TRANSACTION_LOG (Transaction_ID INT PRIMARY KEY, Type VARCHAR(50), Amount DECIMAL(10,2), Date DATE, Entity_Type VARCHAR(50), Entity_ID INT);
INSERT INTO TRANSACTION_LOG VALUES (2001,'Sponsorship',50000.00,'2025-01-10','Sponsor',801),(2002,'Venue Rental',-5000.00,'2025-01-15','Venue',201);

-- 13. MENTOR_TEAM (Bridge)
CREATE TABLE MENTOR_TEAM (Mentor_ID INT, Team_ID INT, PRIMARY KEY (Mentor_ID, Team_ID));
INSERT INTO MENTOR_TEAM VALUES (601,401),(602,402);

-- 14. SPONSOR_HACKATHON (Bridge)
CREATE TABLE SPONSOR_HACKATHON (Sponsor_ID INT, Hackathon_ID INT, PRIMARY KEY (Sponsor_ID, Hackathon_ID));
INSERT INTO SPONSOR_HACKATHON VALUES (801,101),(802,102);

-- 15. RESOURCE_HACKATHON (Bridge)
CREATE TABLE RESOURCE_HACKATHON (Resource_ID INT, Hackathon_ID INT, PRIMARY KEY (Resource_ID, Hackathon_ID));
INSERT INTO RESOURCE_HACKATHON VALUES (1001,101),(1002,102);

-- 16. JUDGE_PROJECT (Bridge with attributes)
CREATE TABLE JUDGE_PROJECT (Judge_ID INT, Project_ID INT, Score INT, Comments VARCHAR(255), PRIMARY KEY (Judge_ID, Project_ID));
INSERT INTO JUDGE_PROJECT VALUES (701,501,95,'Excellent AI model'),(702,502,88,'Good UI, needs better backend');
        """)
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

# ── ADMIN ROUTES ──────────────────────────────────────────────────────────────

@app.route('/api/hackathons', methods=['GET'])
def get_hackathons():
    conn = get_db()
    rows = conn.execute("""
        SELECT H.Hackathon_ID, H.Title, H.Start_Date, H.End_Date, H.Duration,
               H.Theme, H.Expected_Participants, H.Status,
               V.Name AS Venue_Name, V.City, V.Capacity, V.Facilities
        FROM HACKATHON H
        JOIN VENUE V ON H.Venue_ID = V.Venue_ID
        ORDER BY H.Start_Date
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    conn = get_db()
    rows = conn.execute("SELECT * FROM TRANSACTION_LOG ORDER BY Date DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── PARTICIPANT ROUTES ────────────────────────────────────────────────────────

@app.route('/api/participants', methods=['POST'])
def add_participant():
    data = request.get_json()
    conn = get_db()
    try:
        max_id = conn.execute("SELECT MAX(Participant_ID) FROM PARTICIPANT").fetchone()[0] or 300
        new_id = max_id + 1
        conn.execute(
            "INSERT INTO PARTICIPANT (Participant_ID, Name, Age, Gender, Contact, Skill_Set, Education) VALUES (?,?,?,?,?,?,?)",
            (new_id, data['name'], data['age'], data['gender'], data['contact'], data['skill_set'], data['education'])
        )
        conn.commit()
        return jsonify({"success": True, "id": new_id, "message": f"Participant '{data['name']}' registered with ID {new_id}!"}), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

@app.route('/api/projects', methods=['GET'])
def get_projects():
    conn = get_db()
    rows = conn.execute("""
        SELECT P.Project_ID, P.Title, P.Description, P.Tech_Stack, P.Submission_Status,
               T.Team_Name, H.Title AS Hackathon_Title
        FROM PROJECT P
        JOIN TEAM T ON P.Team_ID = T.Team_ID
        JOIN HACKATHON H ON T.Hackathon_ID = H.Hackathon_ID
        ORDER BY P.Project_ID
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

# ── STAFF ROUTES ──────────────────────────────────────────────────────────────

@app.route('/api/staff', methods=['GET'])
def get_staff():
    conn = get_db()
    rows = conn.execute("""
        SELECT S.Staff_ID, S.Name, S.Role, S.Shift_Timing, H.Title AS Hackathon_Title
        FROM STAFF S
        JOIN HACKATHON H ON S.Hackathon_ID = H.Hackathon_ID
    """).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/resources', methods=['GET'])
def get_resources():
    conn = get_db()
    rows = conn.execute("SELECT * FROM RESOURCE").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/resources/<int:resource_id>/status', methods=['PUT'])
def update_resource_status(resource_id):
    data = request.get_json()
    new_status = data.get('status')
    conn = get_db()
    try:
        conn.execute(
            "UPDATE RESOURCE SET Availability_Status = ? WHERE Resource_ID = ?",
            (new_status, resource_id)
        )
        conn.commit()
        return jsonify({"success": True, "message": f"Resource {resource_id} status updated to '{new_status}'."}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400
    finally:
        conn.close()

# ── SERVE FRONTEND ────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
