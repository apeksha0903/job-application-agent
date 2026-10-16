# AI Job Application Agent

## Project Overview

The AI Job Application Agent is an agentic AI system designed to reduce the manual effort involved in discovering, evaluating, preparing, and tracking job applications.

The system will accept job opportunities as input, analyze job descriptions against a structured candidate profile, determine career relevance, select and tailor application materials, assist with application form filling, request human input when necessary, and require human approval before final submission.

## Primary Goal

Automate repetitive job application tasks while keeping the candidate in control of important decisions and final submission.

## Core Workflow

Job Link
→ Job Description Extraction
→ Job Analysis
→ Career Fit Analysis
→ Resume Selection
→ Resume Tailoring
→ Application Preparation
→ Browser Automation
→ Human Review
→ Submission
→ Application Tracking

## Initial Scope

The first version will focus on processing a single job URL and producing a structured career-fit analysis.

Instagram integration and large-scale job discovery will be added later.

## Technology Direction

* Python
* OpenAI Agents SDK
* Pydantic
* Playwright
* SQLite
* Streamlit
* Git/GitHub

## Development Principle

The system should never fabricate candidate experience, skills, qualifications, or achievements.

Human approval will be required before submitting an application.

## Project Status

Phase 0 — Environment and Project Setup

## Documentation

Detailed implementation decisions and development steps are maintained in the docs/ directory.
