# GUDLFT Registration

## Description

GUDLFT Registration is a lightweight proof of concept application for managing regional strength competitions.

The application allows club secretaries to:

- log in with their email address;
- view available competitions;
- book places for future competitions;
- use club points to reserve places;
- view their current points balance;
- view a public points board listing all clubs and their current points.

The application uses Flask and JSON files instead of a database in order to keep the prototype simple and lightweight.

---

## Technologies

This project uses:

- Python 3
- Flask
- Pytest
- Pytest-cov
- Locust
- Flake8
- Black

---

## Current setup

The application uses JSON files as data storage:

- `clubs.json`: contains club names, emails and points.
- `competitions.json`: contains competition names, dates and available places.

There is no database in this prototype.

---

## Main features

### Login

Club secretaries can log in with their email address.

If an unknown email is entered, an error message is displayed instead of crashing the application.

### Competition booking

A club secretary can book places for a valid future competition.

The booking system prevents:

- booking more places than the club has points;
- booking more than 12 places per competition;
- booking more places than the competition has available;
- booking places for past competitions;
- booking zero or negative places;
- submitting a non-numeric number of places;
- booking with an invalid club or competition.

After a valid booking:

- the competition's available places are deducted;
- the club's points are deducted.

### Public points board

A public points board is available without logging in.

It displays all clubs and their current points balance.

Route:

```text
/points
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Aurelien7777/Python_Testing.git
cd Python_Testing
```

Create a virtual environment:

```bash
python -m venv env
```

Activate the virtual environment.

On Windows PowerShell:

```bash
.\env\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---
## Environment variables

Create a `.env` file at the root of the project with the following content:

```env
FLASK_APP=server.py
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
```
Flask can automatically load this `.env` file if `python-dotenv` is installed.

The `.env` file is ignored by Git and should not be committed.

An example file is provided in `.env.example`.

---

## Run the application

If the `.env` file is configured, run:

```bash
flask run
```

Or run the application explicitly:

```bash
flask --app server run
```

Or:

```bash
python -m flask --app server run
```

The application should then be available at:

```text
http://127.0.0.1:5000
```

---

## Testing

The test suite is split into several categories:

- unit tests;
- integration tests;
- functional tests;
- performance tests.

### Run all tests

```bash
pytest
```

---

## Unit tests

Unit tests cover isolated business rules from `booking_rules.py`.

They test rules such as:

- valid or invalid place numbers;
- club points availability;
- competition places availability;
- maximum booking limit;
- remaining places calculation;
- remaining points calculation.

Run unit tests:

```bash
pytest test/unit
```

---

## Integration tests

Integration tests verify that Flask routes, templates, flash messages and in-memory JSON data work together correctly.

They test endpoints such as:

- `/showSummary`
- `/book/<competition>/<club>`
- `/purchasePlaces`
- `/points`

Run integration tests:

```bash
pytest test/integration/test_integration.py
```

---

## Functional tests

Functional tests simulate complete user workflows with Flask test client.

They cover scenarios such as:

- secretary login;
- opening a valid booking page;
- successful booking;
- failed booking;
- checking that points and competition places are updated or unchanged depending on the scenario.

Run functional tests:

```bash
pytest test/functional/test_functional.py
```

---

## Coverage report

Generate a coverage report in the terminal:

```bash
pytest --cov=server --cov=booking_rules --cov-report=term-missing
```

Generate an HTML coverage report:

```bash
pytest --cov=server --cov=booking_rules --cov-report=html
```

Then open:

```text
htmlcov/index.html
```

The generated coverage files are ignored by Git and should not be committed.

---

## Performance testing

Performance tests are handled with Locust.

The performance goals are:

- the competition list should load in less than 5 seconds;
- the points update after booking should take less than 2 seconds;
- the default number of users for the performance test is 6.

Start the Flask application first:

```bash
flask --app server run
```

Then start Locust:

```bash
cd test
cd performance_test
locust
```

Open the Locust interface:

```text
http://localhost:8089
```

Recommended settings:

```text
Number of users: 6
Spawn rate: 1
Host: http://127.0.0.1:5000
```

---

## Code quality

### Flake8

Run Flake8:

```bash
flake8
```

### Black

Check formatting:

```bash
black --check .
```

Apply formatting:

```bash
black .
```

---

## Git workflow

Each bug fix, feature or improvement is developed in a dedicated branch.

Examples:

```text
fix/1-unknown-email-crash
bug/282-prevent-booking-more-places-than-available
feature/public-points-board
refactor/add-unit-tests-booking-rules
test/add-functional-tests
chore/finalize-project-deliverables
```

The `master` branch contains the stable version of the project.

A final `qa` branch is created from `master` once all fixes, features, tests and documentation updates have been merged.

---

## Main fixes and improvements

The following bugs, features and improvements have been implemented:

- fixed crash when entering an unknown email;
- prevented clubs from booking more places than their available points;
- prevented clubs from booking more than 12 places per competition;
- prevented booking places for past competitions;
- deducted club points after a successful booking;
- deducted competition places after a successful booking;
- added a points display board;
- added a public points board accessible without login;
- prevented clubs from booking more places than available in a competition;
- prevented zero or negative booking values;
- handled invalid booking inputs;
- handled invalid club or competition names;
- refactored booking rules into isolated functions;
- added unit tests for booking rules;
- added integration tests for Flask routes;
- added functional tests for booking workflows;
- added performance testing with Locust;
- added coverage reporting;
- added code quality tools with Flake8 and Black.

---
