# AI-Academic-Advisor-Challenge
# AI Curriculum Planner: Adaptive Academic Advising for 100 Simulated Students

## Introduction
This project implements an AI-powered academic advising system designed to recommend optimal course paths for a cohort of 100 simulated students. The system uses a graph-based model for the university curriculum and a heuristic-based planning algorithm for personalized course recommendations. 

## Project Structure and Files
*`academic_advisor.py` : Contains all the Python code for curriculum modeling, student simulation, and the personalization algorithm. 
* `2-Page Report.pdf`: A detailed report explaining the project's design, methodology, and results.

## How to Run the Project
To run this project, follow these steps:

1.  **Prerequisites:**
    * Ensure you have Python 3.x installed.
    * Install the required Python libraries using pip:
        ```bash
        pip install networkx matplotlib
        ```

2.  **Execution:**
    * Navigate to the directory where you saved the `academic_advisor.py` file .
    * Run the script from your terminal or command prompt:
        ```bash
        python academic_advisor.py
        ```
    * The script will output information about the generated curriculum graph, simulated students, and example course recommendations.

## PART 1 – Curriculum and Student Simulation (Graph Modeling)
This section focuses on modeling the university curriculum and simulating student data.

### Curriculum Model
* The university curriculum is modeled as a **directed graph** using the `networkx` library. 
* **Nodes** represent individual courses.Each course node has attributes such as `name`, `credits`, and `interests`.
* **Edges** represent prerequisite relations, indicating which courses must be completed before others (e.g., `CS101 -> CS201` means CS101 is a prerequisite for CS201). 

### Student Simulation
* **100 students** are simulated, each with unique characteristics.
* Each student's data includes:
    * `student_id`
    * `gpa` (randomly generated between 2.0 and 4.0) 
    * `interests` (randomly selected from a predefined list of academic interests) 
    * `completed_courses` (a collection of courses the student has passed, along with their `grades`).
    * **Note on `completed_courses` simulation:** For simplicity and due to time constraints, initial completed courses were randomly selected primarily from courses with no prerequisites.

### Modeled Constraints
The system takes into account the following academic constraints:
* **Course Load Limit:** A maximum of 3-5 courses per term is recommended.
* **Prerequisite Completion:** A student cannot take a course without successfully completing all its prerequisites. 
* **Retake Policy:** If a student fails a required course, it is prioritized for re-taking. 

## PART 2 – AI-Based Personalization Strategy
This section details the algorithm used for personalized course recommendations.

### Algorithm Design
* **Approach:** Due to time constraints, a **heuristic-based planning algorithm** was implemented instead of a full Reinforcement Learning model. This approach uses predefined rules to guide the recommendations.
* **Objective:** Recommend a set of next-term courses that: 
    ***Respect constraints:** Adhere to prerequisites, course load limits, and retake policies. 
    ***Align with interests:** Prioritize courses matching the student's declared interests.
    * **Maximize GPA/Graduation Likelihood:** While not explicitly optimized with a complex model, the heuristic aims for this by suggesting relevant courses and prioritizing retakes.

### Recommendation Process
The recommendation process for each student involves two main steps:
1.  **Identifying Eligible Courses:**
    * Checks all courses in the curriculum.
    * Determines if all prerequisites for a course are met (i.e., successfully completed).
    * Prioritizes courses where the student previously failed (`F` grade) and needs to retake.
2.  **Scoring and Selection:**
    * Assigns a "score" to each eligible course based on the number of overlapping interests between the course and the student.
    * Sorts eligible courses by this score (higher score first).
    * Selects the top 3-5 courses, prioritizing required retakes and then courses with the highest interest alignment, until the course load limit is reached.

## Deliverables
All project deliverables are included in this GitHub Repository: 
* **Code:** `academic_advisor.py`
* **Report:** `2-Page Report.pdf` 
