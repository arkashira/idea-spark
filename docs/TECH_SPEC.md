# Technical Specification for Idea Tracker
==============================================

## Overview
------------

Idea Tracker is a software application designed to link validated ideas to the Axentx OS product pipeline, track 90-day conversion rates automatically, and generate NSM (New Service Metric) reports for performance analysis. This document outlines the technical specification for the Idea Tracker project.

## Architecture Overview
------------------------

The Idea Tracker application will be built using a microservices architecture, consisting of the following components:

### 1. Idea Service

* Responsible for storing and retrieving idea data
* Will be built using a relational database (PostgreSQL) for data persistence
* Will expose RESTful APIs for idea creation, retrieval, and deletion

### 2. Conversion Rate Service

* Responsible for tracking 90-day conversion rates for ideas
* Will use a message broker (RabbitMQ) to receive idea creation events from the Idea Service
* Will store conversion rate data in a time-series database (InfluxDB)

### 3. NSM Report Service

* Responsible for generating NSM reports for performance analysis
* Will use a reporting library (Pandas) to generate reports from data stored in the Conversion Rate Service
* Will expose a RESTful API for report generation and retrieval

### 4. Web Interface

* A simple web interface will be built using a frontend framework (React) to allow users to interact with the Idea Tracker application
* Will use the Idea Service RESTful API to retrieve and update idea data

## Data Model
-------------

The Idea Tracker application will use the following data models:

### Idea Entity

* `id` (primary key): unique identifier for the idea
* `title`: title of the idea
* `description`: description of the idea
* `validated`: boolean indicating whether the idea has been validated
* `created_at`: timestamp for when the idea was created
* `updated_at`: timestamp for when the idea was last updated

### Conversion Rate Entity

* `idea_id` (foreign key): reference to the Idea Entity
* `conversion_rate`: 90-day conversion rate for the idea
* `created_at`: timestamp for when the conversion rate was recorded
* `updated_at`: timestamp for when the conversion rate was last updated

## Key APIs/Interfaces
-----------------------

The Idea Tracker application will expose the following APIs/interfaces:

### Idea Service

* `POST /ideas`: create a new idea
* `GET /ideas`: retrieve a list of ideas
* `GET /ideas/{id}`: retrieve a single idea by ID
* `DELETE /ideas/{id}`: delete an idea by ID

### Conversion Rate Service

* `POST /conversion-rates`: record a new conversion rate event
* `GET /conversion-rates`: retrieve a list of conversion rates

### NSM Report Service

* `POST /reports`: generate a new NSM report
* `GET /reports`: retrieve a list of reports

## Tech Stack
--------------

The Idea Tracker application will be built using the following technologies:

* Programming language: Python 3.9
* Framework: Flask
* Database: PostgreSQL
* Message broker: RabbitMQ
* Time-series database: InfluxDB
* Reporting library: Pandas
* Frontend framework: React

## Dependencies
--------------

The Idea Tracker application will depend on the following libraries:

* `flask`: web framework
* `psycopg2`: PostgreSQL driver
* `pandas`: reporting library
* `influxdb`: InfluxDB driver
* `rabbitmq`: RabbitMQ driver
* `react`: frontend framework

## Deployment
-------------

The Idea Tracker application will be deployed to a cloud platform (AWS) using the following infrastructure:

* Containerization: Docker
* Orchestration: Kubernetes
* Load balancing: ELB
* Storage: EBS

## Conclusion
----------

The Idea Tracker application will provide a simple and effective way to link validated ideas to the Axentx OS product pipeline, track 90-day conversion rates automatically, and generate NSM reports for performance analysis. This technical specification outlines the architecture, components, data model, key APIs/interfaces, tech stack, dependencies, and deployment for the Idea Tracker project.
