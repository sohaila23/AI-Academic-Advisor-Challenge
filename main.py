import networkx as nx
import random

curriculum_graph = nx.DiGraph()
curriculum_graph.add_node("CS101", name="Introduction to Programming", credits=3,
                          interests=["Programming", "Problem Solving"])
curriculum_graph.add_node("MA101", name="Calculus I", credits=3, interests=["Mathematics"])
curriculum_graph.add_node("PH101", name="Physics I", credits=3, interests=["Science"])
curriculum_graph.add_node("EN101", name="English Composition", credits=3, interests=["Writing"])

curriculum_graph.add_node("CS201", name="Data Structures", credits=3, interests=["Programming", "Algorithms"])
curriculum_graph.add_node("MA201", name="Linear Algebra", credits=3, interests=["Mathematics"])
curriculum_graph.add_node("CS202", name="Object-Oriented Programming", credits=3, interests=["Programming"])

curriculum_graph.add_node("CS301", name="Algorithms Design", credits=3, interests=["Algorithms", "Problem Solving"])
curriculum_graph.add_node("CS302", name="Database Systems", credits=3, interests=["Databases", "Data Science"])
curriculum_graph.add_node("AI401", name="Introduction to AI", credits=3, interests=["AI", "Machine Learning"])

curriculum_graph.add_edge("CS101", "CS201")  # Intro to Programming -> Data Structures
curriculum_graph.add_edge("CS101", "CS202")  # Intro to Programming -> OOP
curriculum_graph.add_edge("MA101", "MA201")  # Calculus I -> Linear Algebra
curriculum_graph.add_edge("CS201", "CS301")  # Data Structures -> Algorithms Design
curriculum_graph.add_edge("CS201", "CS302")  # Data Structures -> Database Systems
curriculum_graph.add_edge("CS202", "AI401")  # OOP -> Intro to AI
curriculum_graph.add_edge("MA201", "AI401")  # Linear Algebra -> Intro to AI

# print("Curriculum Graph created:")
# print(f"Number of nodes (courses): {curriculum_graph.number_of_nodes()}")
# print(f"Number of edges (prerequisites): {curriculum_graph.number_of_edges()}")

# print("\nDetails for CS201:")
# print(curriculum_graph.nodes["CS201"])

all_course_ids = list(curriculum_graph.nodes())
available_interests = ["AI", "Machine Learning", "Data Science", "Cybersecurity",
                       "Web Development", "Mobile Development", "Game Development",
                       "Cloud Computing", "Networking", "Databases"]

num_students = 100
students_data = []
for i in range(num_students):
    student_id = f"S{i + 1:03d}"
    gpa = round(random.uniform(2.0, 4.0), 2)
    num_student_interests = random.randint(1, 3)
    student_interests = random.sample(available_interests, num_student_interests)
    initial_completed_courses = []
    no_prereq_courses = [course_id for course_id in all_course_ids if
                         not list(curriculum_graph.predecessors(course_id))]
    num_to_complete = random.randint(3, 6)
    completed_course_ids = random.sample(no_prereq_courses, min(num_to_complete, len(no_prereq_courses)))
    grades = {}
    for course_id in completed_course_ids:
        grades[course_id] = random.choice(["A", "B", "C", "F"])  # ممكن الطالب يكون ساقط في كورس

    student_info = {
        "student_id": student_id,
        "gpa": gpa,
        "interests": student_interests,
        "completed_courses": completed_course_ids,
        "grades": grades
    }
    students_data.append(student_info)


# print(f"\nSimulated {num_students} students. Here are the first 5:")
# for i, student in enumerate(students_data[:5]):
#  print(f"\nStudent ID: {student['student_id']}")
#  print(f"  GPA: {student['gpa']}")
#  print(f"  Interests: {', '.join(student['interests'])}")
# print(f"  Completed Courses: {', '.join(student['completed_courses'])}")
# print(f"  Grades: {student['grades']}")
def get_eligible_courses(student, curriculum_graph):
    eligible_courses = []
    completed_course_ids = student["completed_courses"]
    student_grades = student["grades"]
    retake_required_courses = [
        course_id for course_id in completed_course_ids
        if course_id in student_grades and student_grades[course_id] == "F"
    ]
    courses_not_passed = []
    for course_id in curriculum_graph.nodes():
        if course_id not in completed_course_ids or \
                (course_id in completed_course_ids and course_id in student_grades and student_grades[
                    course_id] == "F"):
            courses_not_passed.append(course_id)
    for course_id in courses_not_passed:
        if course_id in retake_required_courses:
            eligible_courses.append(course_id)
            continue
        prerequisites = list(curriculum_graph.predecessors(course_id))
        if not prerequisites:
            eligible_courses.append(course_id)
        else:
            all_prereqs_met = True
            for prereq_id in prerequisites:
                if prereq_id not in completed_course_ids or \
                        (prereq_id in student_grades and student_grades[
                            prereq_id] == "F"):
                    all_prereqs_met = False
                break
            if all_prereqs_met:
                eligible_courses.append(course_id)
    return eligible_courses


# print("\n--- Testing get_eligible_courses ---")
# sample_student = students_data[0]

# print(f"\nSample Student ID: {sample_student['student_id']}")
# print(f"  Completed Courses: {', '.join(sample_student['completed_courses'])}")
# print(f"  Grades: {sample_student['grades']}")

# eligible_for_sample_student = get_eligible_courses(sample_student, curriculum_graph)
# print(f"  Eligible Courses: {', '.join(eligible_for_sample_student)}")

# if len(students_data) >= 3:
#   sample_student_with_fails = students_data[2]
#  print(f"\nSample Student ID (with fails): {sample_student_with_fails['student_id']}")
# print(f"  Completed Courses: {', '.join(sample_student_with_fails['completed_courses'])}")
# print(f"  Grades: {sample_student_with_fails['grades']}")
# eligible_for_fail_student = get_eligible_courses(sample_student_with_fails, curriculum_graph)
# print(f"  Eligible Courses: {', '.join(eligible_for_fail_student)}")

def recommend_courses(student, eligible_courses, curriculum_graph, max_courses_per_term=5):
    recommendations = []
    student_interests = set(student["interests"])
    if not eligible_courses:
        return []
    course_scores = {}
    for course_id in eligible_courses:
        course_interests = set(curriculum_graph.nodes[course_id].get("interests", []))
        common_interests = len(student_interests.intersection(course_interests))
        course_scores[course_id] = common_interests
    sorted_eligible_courses = sorted(course_scores.items(), key=lambda item: (-item[1], item[0]))
    courses_to_retake = [
        course_id for course_id in eligible_courses
        if course_id in student["grades"] and student["grades"][course_id] == "F"
    ]
    for course_id in courses_to_retake:
        if len(recommendations) < max_courses_per_term:
            recommendations.append(course_id)
        else:
            break
    for course_id, score in sorted_eligible_courses:
        if len(recommendations) < max_courses_per_term:
            if course_id not in recommendations:
                recommendations.append(course_id)
        else:
            break
    return recommendations


sample_student_1 = students_data[0]
eligible_for_student_1 = get_eligible_courses(sample_student_1, curriculum_graph)
recommendations_1 = recommend_courses(sample_student_1, eligible_for_student_1, curriculum_graph)
print(f"\nStudent ID: {sample_student_1['student_id']}")
print(f"  Interests: {', '.join(sample_student_1['interests'])}")
print(f"  Completed Courses: {', '.join(sample_student_1['completed_courses'])}")
print(f"  Grades: {sample_student_1['grades']}")
print(f"  Eligible Courses: {', '.join(eligible_for_student_1)}")
print(f"  Recommended Courses: {', '.join(recommendations_1)}")

if len(students_data) >= 3:
    sample_student_3 = students_data[2]
    eligible_for_student_3 = get_eligible_courses(sample_student_3, curriculum_graph)
    recommendations_3 = recommend_courses(sample_student_3, eligible_for_student_3, curriculum_graph)
    print(f"\nStudent ID: {sample_student_3['student_id']}")
    print(f"  Interests: {', '.join(sample_student_3['interests'])}")
    print(f"  Completed Courses: {', '.join(sample_student_3['completed_courses'])}")
    print(f"  Grades: {sample_student_3['grades']}")
    print(f"  Eligible Courses: {', '.join(eligible_for_student_3)}")
    print(f"  Recommended Courses: {', '.join(recommendations_3)}")


if len(students_data) >= 5:
    sample_student_5 = students_data[4]
    eligible_for_student_5 = get_eligible_courses(sample_student_5, curriculum_graph)
    recommendations_5 = recommend_courses(sample_student_5, eligible_for_student_5, curriculum_graph)
    print(f"\nStudent ID: {sample_student_5['student_id']}")
    print(f"  Interests: {', '.join(sample_student_5['interests'])}")
    print(f"  Completed Courses: {', '.join(sample_student_5['completed_courses'])}")
    print(f"  Grades: {sample_student_5['grades']}")
    print(f"  Eligible Courses: {', '.join(eligible_for_student_5)}")
    print(f"  Recommended Courses: {', '.join(recommendations_5)}")

# print("\n--- Recommendations for all 100 students ---")
# all_students_recommendations = []
# for student in students_data:
#     eligible_courses_for_student = get_eligible_courses(student, curriculum_graph)
#     recommended_courses = recommend_courses(student, eligible_courses_for_student, curriculum_graph)
#     all_students_recommendations.append({
#         "student_id": student["student_id"],
#         "recommended_courses": recommended_courses
#     })
#     # print(f"Student {student['student_id']}: {', '.join(recommended_courses)}")
#
# # print(f"\nTotal recommendations generated for {len(all_students_recommendations)} students.")
