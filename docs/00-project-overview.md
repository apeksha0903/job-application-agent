# AI Job Application Agent — Project Overview

## 1. Project Overview

The AI Job Application Agent is an agentic AI system designed to reduce the manual effort involved in processing job opportunities and preparing job applications.

The eventual system will accept a job opportunity, extract and analyze its job description, compare it against a structured candidate profile, determine whether the role aligns with the candidate's career goals, select and tailor appropriate application materials, assist with application form completion, and track the application.

## 2. Problem Statement

Job searching involves many repetitive tasks:

* Reading job descriptions
* Checking required skills
* Determining whether a role fits long-term career goals
* Comparing the role against existing skills and experience
* Selecting an appropriate resume
* Tailoring the resume
* Preparing cover letters
* Filling repetitive application fields
* Answering application questions
* Tracking submitted applications

The purpose of this project is to automate as much of this repetitive work as safely possible.

## 3. Primary Goal

Build a personal AI agent that assists with the job application lifecycle while keeping the candidate in control of important decisions.

## 4. Core Workflow

Job Link
→ Job Description Extraction
→ Structured Job Analysis
→ Career Fit Analysis
→ Resume Selection
→ Resume Tailoring
→ Application Preparation
→ Browser Automation
→ Human Review
→ Submission
→ Application Tracking

## 5. Initial MVP

The first milestone is intentionally small:

Input:
A single public job URL.

Output:
A structured analysis containing:

* Company
* Job title
* Location
* Experience requirements
* Required skills
* Preferred skills
* Responsibilities
* Role category
* Career-fit analysis
* Matching skills
* Missing skills
* Career-switch relevance
* Whether the role should proceed to application preparation

## 6. Future Scope

Future versions may include:

* Multiple job sources
* Instagram job-link inbox
* Automated job discovery
* Resume variants
* Resume tailoring
* Cover-letter generation
* Application form automation
* Human-in-the-loop approval
* Application tracking dashboard
* Interview tracking
* Analytics
* PostgreSQL
* Deployment

## 7. Important Design Principles

### No Fabrication

The system must never invent:

* Skills
* Experience
* Qualifications
* Projects
* Certifications
* Employment history
* Achievements

All candidate claims must originate from verified candidate data.

### Human Control

The system should pause when important information is unknown or ambiguous.

Final application submission should require explicit human approval.

### Deterministic Rules + LLM Reasoning

Simple decisions should use deterministic code where possible.

The LLM should be used for tasks that require interpretation, reasoning, extraction, or natural-language generation.

## 8. Technology Direction

* Python
* OpenAI Agents SDK
* Pydantic
* Playwright
* SQLite
* Streamlit
* Git/GitHub

## 9. Development Approach

The system will be developed incrementally.

Each phase will be implemented, tested, and documented before moving to the next phase.

## 10. Current Phase

Phase 0 — Environment and Project Setup
