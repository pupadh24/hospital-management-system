# **Hospital Management System**
[Live Demo](https://hospital-management-system-0r2y.onrender.com) *_(Note: Since I'm using a free hosting and DB service, it might take some time to load)_*

Initial Build: 2023 | Currently updating for cloud hosting and new features.

This is a Flask web app I've built to help manage how a hospital handles patients and doctors. It uses a TiDB database to keep track of everything and has three different login types so users only see what they are supposed to.

## **What it does**
**For Patients:** You can sign up, log in, and see which doctors are available. I wrote the logic to make sure you can't book a time slot that is already taken. You can also view or cancel your appointments from your dashboard.

**For Doctors:** Once logged in, doctors get a list of their daily appointments. It shows the patient's name and blood group so they can be ready for the visit.

**For Admins:** This is the main control area. Admins can add or remove doctor and patient accounts, check doctor salaries, and manage the full appointment list for the hospital.

## **How it’s built**
**Language:** Python 3

**Framework:** Flask

**Database:** TiDB

## **How to run it locally**
**1. Clone the repo**
```bash
git clone https://github.com/pupadh24/hospital-management-system.git
cd hospital-management-system
```

**2. Set up Python**
```bash
python -m venv venv
pip install -r requirements.txt
```

**3. Set up the Database**
Import the schema.sql file into your MySQL.

Create a .env file in the main folder and add your MySQL username and password there.

**4. Run it**
```bash
python app.py
```

## **What I'm working on next**
1. Building out the Pharmacy section so doctors can manage medicine stock (and users can buy it too)

2. Cleaning up the UI to make it look a little better.
