# Project10X: The Backend Builder Series

A structured, hands-on journey through 10 backend projects, designed to progressively build and deepen backend development skills using **Django**, **Django REST Framework**, and selected projects with **FastAPI** for asynchronous and microservice-based tasks.

---

## Overview

This repository documents a curated sequence of backend projects developed to explore modern web development concepts in a practical, incremental way.

Each project focuses on production-style backend architecture, and includes:

* Core CRUD and RESTful logic
* Backend tests (unit and API-level)
* A minimal frontend built with HTML, CSS, and vanilla JavaScript
* Optional stretch goals for deeper exploration or feature expansion

Projects are structured to reflect real-world systems rather than isolated examples, with an emphasis on clean code, modular design, and practical experience.

---

## Projects Included

| #  | Project Name                           | Key Features                                                 | Stack               |
| -- | -------------------------------------- | ------------------------------------------------------------ | ------------------- |
| 1  | Personal Blogging Platform API         | Markdown, slugs, tags, authentication, filtering             | Django + DRF        |
| 2  | Expense Tracker API                    | User data, date filtering, aggregation                       | Django + DRF        |
| 3  | URL Shortener API                      | Short link hashing, redirection, click tracking              | Django + DRF        |
| 4  | Fitness Workout Tracker                | Nested models (workouts > exercises), progress tracking      | Django + DRF        |
| 5  | API Aggregator Microservice            | Async external fetch, response merging, optional caching     | **FastAPI + httpx** |
| 6  | Movie Reservation System               | Time slots, seat logic, transactional integrity              | Django + DRF        |
| 7  | Job Board API                          | User roles, job applications, advanced filtering             | Django + DRF        |
| 8  | Real-Time Messaging & Polling Backend  | WebSockets, Django Channels, live chat/polling modules       | Django + Channels   |
| 9  | Restaurant Review Platform + Sentiment | Text analysis (TextBlob/VADER), moderation, review filtering | Django + DRF + NLP  |
| 10 | Simple E-commerce API                  | Product catalog, cart/checkout, payments, order tracking     | Django + DRF        |

Each project resides in its own folder with documentation for setup, features, and testing.

---

## Skills and Technologies

* Python 3.12
* Django & Django REST Framework
* FastAPI (async API microservices)
* JWT Authentication
* PostgreSQL
* HTML, CSS, and Vanilla JavaScript
* RESTful API Design
* Django Testing Framework & DRF APIClient
* Django Channels and WebSocket Communication
* FastAPI with `httpx` for external async API calls
* Redis Caching
* Role-Based Access Control
* Basic Sentiment Analysis (TextBlob, VADER)
* Git and Modular Code Structure

---

## Purpose

**Project10X: The Backend Builder Series** serves as a long-term learning track for mastering backend development through full-stack, feature-complete projects. It reflects a commitment to:

* Building real applications from the ground up
* Practicing testing, deployment readiness, and clean API design
* Exploring technologies beyond core CRUD, including async microservices, real-time communication, and basic ML integration

---

## Usage

Each project includes:

* Clear setup instructions and environment dependencies
* A list of core features and stretch goals
* Backend tests for endpoints and logic
* A minimal frontend for interacting with and verifying API behavior
* Sample data or seeding utilities (where applicable)

This repo is open for exploration, learning, and contribution. Forks, pull requests, and suggestions are welcome.

---

## License

This repository is open source under the MIT License.

---

*Created and maintained by RM Villa.*