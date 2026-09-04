# ClassEye

> AI-Powered Learning Management, Attendance & Classroom Monitoring System

ClassEye is a full-stack education management system that combines a modern React dashboard, a Node.js/Express REST API, MongoDB, and a dedicated FastAPI computer-vision service.

The system is designed to help educational institutions manage students, teachers, classes, users, attendance, and student face-embedding enrollment from a single platform. It also supports image-based attendance by detecting faces in classroom images, generating face embeddings, matching them against enrolled students, and creating attendance records.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Modules](#application-modules)
- [AI Attendance Pipeline](#ai-attendance-pipeline)
- [Face Embedding Enrollment](#face-embedding-enrollment)
- [Authentication and Authorization](#authentication-and-authorization)
- [Database](#database)
- [REST API](#rest-api)
- [Frontend](#frontend)
- [Prerequisites](#prerequisites)
- [Environment Variables](#environment-variables)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [AI Service Setup](#ai-service-setup)
- [Attendance Workflow](#attendance-workflow)
- [Development](#development)
- [Build and Lint](#build-and-lint)
- [Important Notes](#important-notes)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

ClassEye provides a web-based platform for managing academic and attendance workflows.

The application consists of three main services:

1. **React/Vite frontend** — provides dashboards and management interfaces.
2. **Node.js/Express backend** — handles authentication, users, students, teachers, classes, attendance, uploads, and MongoDB persistence.
3. **FastAPI computer-vision service** — handles face detection, face-embedding generation, and classroom-image recognition.

The backend and AI service communicate through HTTP APIs.

### Main workflow

```text
React Frontend
      |
      | REST API
      v
Node.js + Express
      |
      +---------------------> MongoDB
      |
      | HTTP request
      v
FastAPI AI Service
      |
      +--> YOLO face detection
      |
      +--> InsightFace embeddings
      |
      +--> Cosine similarity matching
      |
      v
Recognized Students
      |
      v
Attendance Records
```

---

## Key Features

### User Management

- User creation and management
- User lookup by ID
- User lookup by role
- User update and deletion
- Login support
- Role-based application flows

### Authentication

- JWT-based authentication
- Password hashing with `bcryptjs`
- Authentication cookies
- Protected frontend routes
- Logout support

### Student Management

- Add students
- View student list
- Search students
- View student profiles
- Edit student profiles
- Delete students
- Filter students by department
- Update student profile photos
- Enroll students in classes
- Store face-embedding information for recognition

### Teacher Management

- Add teachers
- View teacher list
- View teacher details
- Update teacher information
- Delete teachers
- Teacher dashboard
- Teacher/class relationships

### Class Management

- Create classes
- View classes
- View class details
- Update classes
- Delete classes
- Enroll students into classes
- Associate teachers with classes
- Manage course/class information

### Attendance Management

- Manual attendance
- Image-based automatic attendance
- Attendance by class and date
- Update individual student attendance status
- Finalize attendance
- Class attendance history
- Student attendance summaries
- Attendance confidence information
- Attendance statistics

### AI-Powered Attendance

- Upload classroom images
- Detect faces in classroom images
- Generate face embeddings
- Compare detected faces with enrolled students
- Calculate cosine similarity
- Identify recognized students
- Return recognition confidence/similarity information
- Integrate recognized students into attendance records

### Dashboards

The frontend contains separate dashboard experiences/components for different application roles, including:

- Admin dashboard
- Teacher dashboard
- Student dashboard
- Parent dashboard
- General dashboard views

Dashboard components include attendance, student, teacher, course-completion, assignment, and at-risk-student information.

---

## System Architecture

ClassEye follows a service-oriented full-stack architecture.

```text
                    ┌───────────────────────────┐
                    │       React Frontend      │
                    │                           │
                    │ React + Vite              │
                    │ Redux Toolkit             │
                    │ RTK Query                 │
                    │ React Router               │
                    │ Tailwind CSS              │
                    └─────────────┬─────────────┘
                                  │
                                  │ REST / JSON
                                  v
                    ┌───────────────────────────┐
                    │     Express Backend       │
                    │                           │
                    │ Node.js + Express         │
                    │ JWT Authentication        │
                    │ Mongoose                  │
                    │ Multer                    │
                    └──────────┬───────┬────────┘
                               │       │
                         MongoDB       │ HTTP
                               │       │
                               │       v
                               │  ┌───────────────────────┐
                               │  │   FastAPI AI Service  │
                               │  │                       │
                               │  │ YOLO                  │
                               │  │ OpenCV                │
                               │  │ InsightFace           │
                               │  │ scikit-learn          │
                               │  └───────────┬───────────┘
                               │              │
                               │         Face embeddings
                               │         + similarity
                               │              │
                               └──────────────┘
```

---

## Technology Stack

### Frontend

| Technology | Purpose |
|---|---|
| React 18 | User interface |
| Vite 5 | Frontend build/dev server |
| React Router 6 | Client-side routing |
| Redux Toolkit | Application state |
| RTK Query | API data fetching/caching |
| Axios | HTTP communication |
| Tailwind CSS 3 | Styling |
| Recharts | Charts and visualization |
| Lucide React | UI icons |
| React Icons | Additional icons |

### Backend

| Technology | Purpose |
|---|---|
| Node.js | Backend runtime |
| Express 5 | REST API |
| MongoDB | Database |
| Mongoose 8 | MongoDB ODM |
| JWT | Authentication |
| bcryptjs | Password hashing |
| Multer | Multipart/image upload handling |
| Axios/Fetch-compatible HTTP tooling | Service communication |
| CORS | Cross-origin requests |
| Cookie Parser | Authentication cookies |
| dotenv | Environment configuration |
| Nodemon | Development server |

### AI / Computer Vision

| Technology | Purpose |
|---|---|
| Python | AI service runtime |
| FastAPI | AI REST API |
| Uvicorn | ASGI server |
| Ultralytics YOLO | Face detection |
| OpenCV | Image decoding and processing |
| InsightFace | Face embeddings |
| scikit-learn | Cosine similarity |
| NumPy | Numerical processing |
| ONNX Runtime | Model inference runtime |

---

## Project Structure

```text
ClassEye/
│
├── README.md
├── package-lock.json
│
├── client/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── eslint.config.js
│   ├── index.html
│   │
│   ├── public/
│   │
│   └── src/
│       ├── App.jsx
│       ├── main.jsx
│       ├── App.css
│       ├── index.css
│       │
│       ├── assets/
│       │
│       ├── layout/
│       │   └── MainLayout.jsx
│       │
│       ├── redux/
│       │   ├── api/
│       │   └── features/
│       │
│       └── pages/
│           ├── dashboards
│           ├── student management
│           ├── teacher management
│           ├── class management
│           ├── attendance
│           ├── reports
│           ├── user management
│           └── reusable components
│
├── server/
│   ├── index.js
│   │
│   ├── config/
│   │   └── db.js
│   │
│   ├── controllers/
│   │
│   ├── middleware/
│   │
│   ├── migration/
│   │
│   ├── models/
│   │   ├── user.model.js
│   │   ├── student.model.js
│   │   ├── teacher.model.js
│   │   ├── class.model.js
│   │   ├── attendance.model.js
│   │   └── counter.model.js
│   │
│   ├── routes/
│   │   ├── auth.route.js
│   │   ├── user.route.js
│   │   ├── student.route.js
│   │   ├── teacher.route.js
│   │   ├── class.route.js
│   │   ├── attendance.routes.js
│   │   ├── dashboard.routes.js
│   │   └── upload.routes.js
│   │
│   └── utils/
│
└── faceEmbeddings/
    ├── app.py
    ├── requirements.txt
    └── notebooks/
```

---

## Application Modules

### 1. Authentication

Authentication is implemented through the Express backend and JWT-based sessions.

The frontend uses authentication state and protected routes to control access to application pages.

Core areas include:

```text
server/controllers/auth.controller.js
server/utils/generateToken.js
server/routes/auth.route.js
client/src/redux/features/auth/
client/src/pages/Login.jsx
client/src/pages/components/ProtectedRoute.jsx
```

---

### 2. Students

Student management is implemented through the student controller, model, routes, and frontend pages.

Relevant frontend pages include:

```text
AddStudent.jsx
StudentList.jsx
StudentProfile.jsx
EditStudentProfile.jsx
SearchStudents.jsx
```

Student-related API state is handled through the Redux/RTK Query student API.

---

### 3. Teachers

Teacher management provides CRUD operations and teacher-facing dashboard functionality.

Relevant pages include:

```text
AddTeacher.jsx
TeacherList.jsx
TeacherDashboard.jsx
```

---

### 4. Classes

Classes connect teachers and students.

The class management module supports:

- class creation
- class retrieval
- class editing
- class deletion
- student enrollment

Relevant pages include:

```text
AddClass.jsx
ClassManagement.jsx
AddStudentsToClass.jsx
```

---

### 5. Attendance

Attendance supports both manual and AI-assisted workflows.

The backend exposes separate operations for:

- retrieving attendance
- creating manual attendance
- automatic image-based attendance
- updating individual student status
- finalizing attendance
- class attendance history
- student attendance summaries

---

## AI Attendance Pipeline

The AI attendance service is implemented in:

```text
faceEmbeddings/app.py
```

The recognition pipeline works approximately as follows:

```text
Classroom Image
      |
      v
Image decoding with OpenCV
      |
      v
YOLO face detection
      |
      v
Individual face crops
      |
      v
InsightFace
      |
      v
Face embedding
      |
      v
Compare with enrolled student embeddings
      |
      v
Cosine similarity
      |
      v
Recognized student
      |
      v
Express attendance controller
      |
      v
MongoDB Attendance document
```

### Recognition threshold

The current AI service defines:

```text
SIMILARITY_THRESHOLD = 0.5
```

The threshold is used when comparing detected face embeddings with stored student embeddings.

---

## Face Embedding Enrollment

ClassEye can generate a student's face embedding from multiple images.

The FastAPI service exposes:

```text
POST /generate-embeddings
```

The service:

1. Receives multiple face images.
2. Decodes the images.
3. Detects/encodes the face using InsightFace.
4. Collects valid embeddings.
5. Requires at least three valid face images.
6. Calculates an average embedding.
7. Returns the resulting embedding information.

The backend can then associate the generated embedding with the student.

---

## Authentication and Authorization

The backend uses:

- JSON Web Tokens
- `bcryptjs`
- HTTP cookies
- Express middleware

Environment variables used by the server include:

```text
MONGO_URI
JWT_SECRET
NODE_ENV
PORT
```

The frontend uses protected routes and authentication state to determine access to protected pages.

> The exact role permissions should be reviewed against the current route/controller implementation before treating them as a formal authorization policy.

---

## Database

ClassEye uses **MongoDB with Mongoose**.

### Models

The project contains the following main Mongoose models:

```text
User
Student
Teacher
Class
Attendance
Counter
```

### Relationships

A simplified relationship structure is:

```text
User
 │
 └── authentication / user information


Teacher
 │
 └── assigned classes


Class
 ├── teacher
 └── enrolled students


Student
 ├── enrolled classes
 └── face embedding


Attendance
 ├── class
 ├── teacher
 └── student attendance records
```

The attendance model also supports a class/date-based attendance structure and individual student attendance information.

---

# REST API

The backend API is mounted under:

```text
/api
```

## Authentication

```text
POST /api/auth/login
POST /api/auth/logout
```

---

## Users

```text
POST   /api/users
GET    /api/users
GET    /api/users/:id
PUT    /api/users/:id
DELETE /api/users/:id
POST   /api/users/login
GET    /api/users/role/:role
```

---

## Teachers

```text
POST   /api/teachers
GET    /api/teachers
GET    /api/teachers/:id
PUT    /api/teachers/:id
DELETE /api/teachers/:id
```

---

## Students

```text
POST   /api/students
GET    /api/students
GET    /api/students/:id
PUT    /api/students/:id
DELETE /api/students/:id
GET    /api/students/department/:department
PATCH  /api/students/photo/:id
```

---

## Classes

```text
POST   /api/classes
GET    /api/classes
GET    /api/classes/:id
PUT    /api/classes/:id
DELETE /api/classes/:id
```

---

## Attendance

```text
GET   /api/attendance/class/:classId/:date
POST  /api/attendance/manual/:classId
POST  /api/attendance/auto/:classId
PATCH /api/attendance/:attendanceId/student/:studentId
POST  /api/attendance/:attendanceId/finalize
GET   /api/attendance/history/class/:classId
GET   /api/attendance/history/student/:studentId/class/:classId
```

---

## Upload / Face Embeddings

```text
POST /api/upload/imgbb
POST /api/upload/generate-embeddings
GET  /api/upload/embeddings-status/:studentId
```

---

## Dashboard

```text
GET /api/dashboard/...
```

The dashboard route provides backend data used by the application's dashboard views.

---

# AI Service API

The FastAPI service runs separately from the Express application.

### Health check

```text
GET /health
```

### Generate embeddings

```text
POST /generate-embeddings
```

### Recognize faces

```text
POST /recognize
```

The recognition request contains classroom image data and enrolled student embedding information.

---

# Frontend

The frontend is a React application built with Vite.

### State management

ClassEye uses:

```text
Redux Toolkit
React Redux
RTK Query
```

Feature API modules include areas such as:

```text
auth
students
teachers
classes
attendance
dashboard
users
image upload
```

### Routing

React Router is used for application navigation and protected pages.

### UI

The application uses:

- Tailwind CSS
- reusable React components
- responsive layouts
- modal-based workflows
- loading indicators
- error messages
- dashboard cards
- charts

---

# Prerequisites

Install the following before running ClassEye:

### Required

- Node.js
- npm
- MongoDB
- Python 3.x
- pip

### Recommended for AI inference

- NVIDIA GPU with compatible CUDA environment, if GPU acceleration is desired
- Compatible ONNX Runtime / InsightFace environment

The exact Python package versions are listed in:

```text
faceEmbeddings/requirements.txt
```

---

# Environment Variables

## Backend

Create a `.env` file inside:

```text
server/.env
```

Example:

```env
MONGO_URI=mongodb://localhost:27017/classeye
JWT_SECRET=your_secure_jwt_secret
NODE_ENV=development
PORT=3000
```

Use a strong secret for `JWT_SECRET`.

---

## Frontend

Create:

```text
client/.env
```

Example:

```env
VITE_API_BASE_URL=http://localhost:3000
```

The current project uses `VITE_API_BASE_URL` for the frontend API base URL.

---

## AI Service

The current FastAPI implementation does not use a dedicated `.env` configuration for its main model path.

The YOLO model is currently loaded from:

```text
classeye.pt
```

Make sure the model is available at the location expected by `faceEmbeddings/app.py` before starting the recognition service.

---

# Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd ClassEye
```

---

## 1. Install Frontend Dependencies

```bash
cd client
npm install
```

---

## 2. Install Backend Dependencies

Open another terminal:

```bash
cd server
npm install
```

---

## 3. Install AI Dependencies

Create and activate a Python virtual environment:

### Windows

```bash
cd faceEmbeddings
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/macOS

```bash
cd faceEmbeddings
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

# Running the Application

ClassEye requires the frontend, backend, and AI service to be available.

## Terminal 1 — Backend

```bash
cd server
npm run dev
```

The Express server uses:

```text
PORT=3000
```

unless another port is supplied through the environment.

---

## Terminal 2 — AI Service

Activate the Python virtual environment and run:

```bash
cd faceEmbeddings
uvicorn app:app --reload
```

The exact host/port configuration should match the AI-service URL used by the Express attendance integration.

---

## Terminal 3 — Frontend

```bash
cd client
npm run dev
```

Vite will display the local development URL in the terminal.

---

# Attendance Workflow

## Manual Attendance

The manual workflow is:

```text
Teacher/Class
      |
      v
Select class
      |
      v
Load students
      |
      v
Mark Present / Absent
      |
      v
Submit attendance
      |
      v
MongoDB
```

---

## Automatic Image Attendance

The automatic workflow is:

```text
Teacher
   |
   v
Select class
   |
   v
Upload classroom image(s)
   |
   v
Express receives image
   |
   v
FastAPI /recognize
   |
   +--> YOLO detects faces
   |
   +--> InsightFace creates embeddings
   |
   +--> Cosine similarity matches students
   |
   v
Recognized students
   |
   v
Attendance generated
   |
   v
Teacher reviews/corrects
   |
   v
Finalize attendance
   |
   v
MongoDB
```

---

# Development

## Frontend Development

```bash
cd client
npm run dev
```

## Backend Development

```bash
cd server
npm run dev
```

## AI Development

```bash
cd faceEmbeddings
uvicorn app:app --reload
```

---

# Build and Lint

## Frontend Build

```bash
cd client
npm run build
```

## Frontend Lint

```bash
cd client
npm run lint
```

## Frontend Preview

```bash
cd client
npm run preview
```

The server package currently does not contain a real automated test suite; its `test` script is only a placeholder.

---

# Important Notes

## Model File

The AI service expects:

```text
classeye.pt
```

This is a binary model artifact used by the YOLO inference pipeline.

Model weights should generally **not be committed to Git**. For production repositories, store large model artifacts separately and configure the application to load them from an appropriate model-storage location.

---

## Credentials

Never commit real:

```text
.env
API keys
JWT secrets
database credentials
private keys
```

Use environment variables and provide safe placeholder examples instead.

---

## Image Uploads

The project includes image-upload functionality and an ImgBB integration route.

Before deploying publicly, review the upload configuration and ensure API credentials are stored securely in environment variables rather than source code.

---

# Limitations

The current source code has several areas that should be considered when deploying ClassEye to production:

- The project does not include a complete automated test suite.
- The AI training pipeline is not included in this repository; the current Python service is focused on inference and embedding/recognition.
- The YOLO model is loaded as an external binary artifact.
- Some configuration values are currently development-oriented.
- Production deployment should move all secrets/API keys into environment variables.
- AI recognition accuracy depends on image quality, face visibility, enrollment quality, lighting, camera angle, and similarity threshold.
- The current recognition threshold is configured as `0.5` and should be validated against real institutional data before production use.
- The system should be evaluated for privacy, consent, retention, and access-control requirements before using biometric data in a real educational environment.

---

# Future Improvements

Potential improvements based on the current architecture include:

### AI / Computer Vision

- Improve face-detection accuracy for crowded classrooms
- Add better handling of occluded faces
- Add confidence calibration
- Add configurable recognition thresholds
- Add automated evaluation metrics
- Separate model storage from application source
- Add a reproducible model-training repository/pipeline

### Backend

- Add comprehensive API tests
- Add request validation schemas
- Improve centralized configuration
- Add structured logging
- Add API documentation
- Add rate limiting
- Improve error handling
- Add production-grade service configuration

### Frontend

- Add more granular role/permission controls
- Improve loading and error states
- Add automated component tests
- Improve responsive behavior
- Add accessibility improvements
- Add richer attendance analytics

### Infrastructure

- Add Docker support
- Add CI/CD
- Add production environment configuration
- Add centralized logging and monitoring
- Add secure object storage for images/models
- Add database backup and recovery procedures

---

# Security and Privacy

ClassEye processes student information and biometric-related face embeddings.

For real-world deployment:

- obtain appropriate consent where required
- restrict access to student biometric information
- encrypt sensitive data in transit and at rest
- avoid storing unnecessary raw classroom images
- establish retention and deletion policies
- protect API credentials
- use HTTPS
- apply least-privilege access controls
- audit access to attendance and biometric data

This README describes the technical implementation present in the project; legal/privacy compliance requirements depend on the deployment jurisdiction and institution.

---

# License

No explicit open-source license is currently defined in the project.

If this project is intended for public distribution, add an appropriate `LICENSE` file and update this section accordingly.

---

# Project Status

**ClassEye is a full-stack AI-assisted education and attendance management project built with React, Node.js/Express, MongoDB, and FastAPI-based computer vision.**

The current implementation includes student, teacher, class, user, dashboard, attendance, face-embedding, and image-recognition functionality, with the AI service integrated into the attendance workflow.

---

## Author

**Usman**

GitHub: `https://github.com/usman0794`

---

## Acknowledgements

ClassEye uses several open-source technologies and libraries, including React, Vite, Redux Toolkit, Express, MongoDB/Mongoose, FastAPI, OpenCV, Ultralytics, InsightFace, scikit-learn, and related Python/JavaScript packages.

---

> **Note:** This README is written from the actual ClassEye source structure and configuration present in the project archive. Where the repository does not contain evidence for a capability—such as a model-training pipeline, Docker configuration, CI/CD, or automated tests—it is not presented as an existing feature.
