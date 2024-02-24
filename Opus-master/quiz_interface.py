# The idea is to take the answers of the quiz and run the classifier on them.
# Used either in collaboration with first-hand data or replaces it.
# Splits the sentences in each question by '. ' sequence.
import init_db
import assign_tags
import assign_attribte_scores
import summariser
header_text = "Select the option that best describes you:"

choice_options = ["Strongly Agree", "Agree", "Somewhat Agree", "Neither Agree nor Disagree", "Somewhat Disagree", "Disagree", "Strongly Disagree"]

choice_questions = ["When faced with a complex problem in my studies, I take the time to break it down into smaller parts to understand it better.",
                    "I can usually understand why my peers feel the way they do in group projects or discussions.",
                    "When discussing academic material with classmates, I encourage others to contribute and make sure everyone is heard.",
                    "I maintain a calm and focused state of mind during exams or deadlines.",
                    "I often suggest new ways of approaching group assignments that differ from the traditional methods.",
                    "When there is an opportunity to lead a project or a study group, I step up without hesitation.",
                    "I consistently set specific goals for my academic progress and actively work towards achieving them.",
                    "In teamwork, I try to be considerate of others' schedules and commitments outside of our academic responsibilities.",
                    "I create a structured study schedule before the semester begins and generally stick to it.",
                    "If I witness academic dishonesty, I feel compelled to report it, even if it involves a friend or a group member.",
                    "I enjoy puzzles and games that challenge my quantitative and reasoning skills outside of academic work.",
                    "I find myself reflecting on my emotional responses to constructive criticism and using that experience to improve.",
                    "I often help mediate conflicts between my peers by providing clear communication and understanding both sides.",
                    "When I experience personal setbacks, I am able to recover and return to my studies without it affecting my performance.",
                    "I am not afraid to experiment with new artistic or creative hobbies, even if they are outside my comfort zone.",
                    "When a professor assigns additional work, I am proactive in organizing study sessions to tackle the material.",
                    "I seek out additional educational opportunities, such as workshops or seminars, even if they are not required for my course.",
                    "I can easily see things from my classmates' perspectives, especially when we have differing opinions on a topic.",
                    "Even when I have a lot of assignments, I manage my time so that I get adequate sleep and exercise.",
                    "I believe that maintaining academic integrity is important, even when others around me choose to ignore it."]

###########~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~########################

header_text = "Answer the following questions in great detail, giving what you would do in each of the situations: "

long_ans_questions = ["You've been given a challenging math problem set with complex equations. How would you approach solving it?",
                      "Your friend is upset about failing an exam. How would you comfort and support them?",
                      "You're tasked with leading a group discussion on a contentious academic topic. How would you ensure everyone's opinions are heard and encourage constructive dialogue?",
                      "During exam week, you face multiple deadlines and feel overwhelmed. How do you manage your stress and maintain focus?",
                      "You're given a project where you need to propose a novel solution to a societal issue. What innovative approach would you take, and how would you implement it?",
                      "A volunteer opportunity arises that aligns with your interests but requires a significant time commitment. How do you decide whether to pursue it?",
                      "You encounter a subject that you find challenging and less interesting. How do you motivate yourself to engage and excel in it?",
                      "You notice a classmate struggling with coursework and feeling isolated. How do you approach and offer support without being intrusive?",
                      "You have several personal projects alongside your studies. How do you manage your time effectively to ensure progress on all fronts?",
                      "You witness a case of academic dishonesty among your peers. How do you respond while upholding academic integrity and fairness?"]


person_name = "Louis"
choice_answers = [
    "Strongly Agree",
    "Strongly Agree",
    "Agree",
    "Agree",
    "Agree",
    "Somewhat Agree",
    "Strongly Agree",
    "Strongly Agree",
    "Agree",
    "Agree",
    "Somewhat Agree",
    "Agree",
    "Strongly Agree",
    "Agree",
    "Agree",
    "Agree",
    "Agree",
    "Strongly Agree",
    "Agree",
    "Strongly Agree"]

choice_answers = ["Agree",
                  "Somewhat Agree",
                  "	Neutral",
                  "	Strongly Agree",
                  "	Neutral",
                  "	Somewhat Disagree",
                  "	Strongly Agree",
                  "	Disagree",
                  "	Strongly Disagree",
                  "	Disagree	",
                  "Strongly Agree	",
                  "Neutral	",
                  "Somewhat Agree	",
                  "Strongly Agree	",
                  "Somewhat Disagree	",
                  "Strongly Disagree	",
                  "Agree	",
                  "Somewhat Agree	",
                  "Somewhat Disagree	",
                  "Strongly Disagree",	]

long_answers = ["Facing a challenging math problem set, my first inclination is to break down each problem into manageable parts. I would ensure that I have a solid understanding of the foundational concepts before tackling the complex equations. If needed, I'd review lecture notes, consult textbooks, and leverage online resources for further explanation. Then, working methodically through each problem, I would jot down my thoughts and possible solution paths for clarity. If I hit a snag, I’d reach out to classmates or tutors to discuss the issue. Collaborative study sessions can often provide new insights and ways of thinking about a problem. I'd take breaks to avoid frustration and maintain a fresh perspective.",
    "It's hard watching a friend upset over a failed exam, so my approach would be empathetic and supportive. I would listen to their concerns without judgment and reassure them that one exam doesn't define their ability or worth. I’d encourage reflection on what might have gone wrong and discuss study strategies that could help in the future, perhaps offering to study together or share resources. Importantly, I'd remind them that everyone encounters setbacks, and it's the recovery and perseverance that count. If they're open to it, we could create a study plan or identify support services provided by the university to help them improve.",
    "Leading a group discussion on a controversial topic requires careful facilitation. I’d start by setting ground rules for respectful and constructive dialogue, ensuring all group members agree to listen actively and speak in turn. By framing the discussion in a way that encourages critical thinking rather than confrontation, and by highlighting the importance of understanding diverse viewpoints, I aim to create an open and inclusive environment. During the discussion, I would actively direct questions to quieter group members to encourage broad participation, and if tensions arise, I’d remind the group of the common goal of learning and understanding, not winning an argument.",
    "Exam week can be particularly stressful with multiple deadlines. To manage this, I create a prioritized study schedule that allocates specific blocks of time for each subject and includes breaks for rest and relaxation. Regular exercise, healthy eating, and ensuring I get enough sleep are integral to maintaining my focus and energy levels. Additionally, I employ relaxation techniques like deep breathing or yoga to mitigate stress. By setting smaller daily goals, I can maintain a sense of progression and stay motivated without becoming overwhelmed by the larger picture.",
    "Proposing a novel solution to a societal issue demands creativity and an understanding of the current landscape. I would conduct thorough research to understand the scope of the problem, including existing solutions and their limitations. Drawing from my Psychology and Sociology knowledge, I would look for patterns or variables that have perhaps been overlooked. My proposal would likely have a strong human-centric approach, potentially utilizing technology or community-driven initiatives for implementation. For example, creating a peer-support app for mental health that leverages local resources and real user experiences could be one idea. Feasibility and sustainability would be essential considerations, and I’d seek feedback from knowledgeable peers and professors during the planning stage.",
    "When considering a volunteer role, it’s important to weigh my passion for the cause against my existing commitments. I would evaluate the time required for the opportunity and assess how it aligns with my long-term goals and current academic workload. If the volunteer work could provide valuable experience and further my understanding in a relevant area, it could justify rearranging my schedule, perhaps by cutting back on less critical activities. I’d also consider the potential academic benefits, like application of theory to practice, and the emotional gratification of contributing to a cause I believe in. To make a decision, a conversation with my advisor or mentor could provide further guidance.",
    "Not all subjects resonate equally, yet excelling in them may still be important. To motivate myself, I find aspects of the subject that tie into my personal interests or long-term goals. If the subject is challenging, I focus on understanding the purpose behind the material and how mastering it benefits my overarching educational journey. Establishing a study group or partnering with a classmate can help make the process more engaging, as can seeking additional resources or explanations that offer a different perspective. Celebrating small milestones along the way helps maintain motivation, and I always remind myself of the satisfaction that comes from overcoming challenges.",
    "When a classmate appears to be struggling, it’s important to offer support in a manner that respects their privacy and dignity. Reaching out casually, perhaps by starting a conversation about class content or university life, can open the door without being intrusive. I might share an experience of my own difficulty with coursework to create a level of empathy and extend an offer of help, such as studying together or sharing notes. If appropriate, I might also mention university resources like tutoring or counseling services, framing it as a common and positive option for many students.",
    "Balancing personal projects with academics requires diligent time management. I prioritize tasks based on urgency and importance, creating a flexible yet structured schedule that includes time blocks dedicated to each project and study sessions. Discipline is crucial, so I set clear boundaries for my work and leisure time, ensuring I don't neglect social activities and self-care, which are vital for maintaining overall well-being. Regular reflection on my progress helps me stay on track and make necessary adjustments to my approach, ensuring that I’m making the best use of my time.",
    "Encountering academic dishonesty is a serious matter. My response would be guided by a commitment to integrity and fairness. Initially, I would consider speaking directly to the individual involved, expressing my concerns about the behavior's implications and encouraging them to rectify the situation. If this approach did not lead to a resolution, or if the dishonesty was flagrant, I would feel compelled to report it to the appropriate university authorities. It is important to uphold the academic standards of the institution and ensure that all students are evaluated on an even playing field."]


long_answers = ["I split the problem into its constituent stages, identifying the methods to solve each stage.",
                "I would tell them to organise a schedule such that they are motivated to put the effort into succeeding next time.",
                "I would ask open-ended questions such that biases are reduced. Promote open discussion by ensuring the group that there are no wrong answers.",
                "Write down each of the deadlines and the actions I have to take in achieving a timely and successful outcome. I would also take walks to clear and focus my mind.",
                "I would focus on my areas of expertise (computer science) when designing a solution. Using innovative methodologies, such as spitballing and clustering ideas can help consolidate themes.",
                "I do not have the time to waste on such insignificant endeavours such as volunteering.",
                "I tell myself that it is necessary to succeed in this subject in order to fulfill my long-term goals.",
                "I do not care about other people or their feelings. I would tell them to struggle in private, as they are distracting me.",
                "I would dynamically allocate time in my brain according to how close deadlines are.",
                "I do not care about the matters of others."]
# take answers and parse them
##### Add sentences for person
# init_db.create_entries_interface()
#
def add_results(person_id, db, choice_answers, long_answers):

    for i in range(len(choice_answers)):
        db.add_sentence(choice_questions[i] + " Answer: " + choice_answers[i], person_id)
    for i in range(len(long_answers)):
        db.add_sentence(long_answers[i], person_id)
    #
    # # # ### Parse sentences
    # # #
    assign_tags.assign_sentences(person_id)
    # #
    # # #### Generate Scores
    # #
    assign_attribte_scores.parse_person(person_id)
    summariser.summarise_person_categories(person_id)
    #### Generate Summary
    summariser.summarise_person(person_id)

def main():
    db = init_db.Database()

    db.add_person_without_data("TEST_NAME")
        # person_id = 1
    person_id = db.get_recent_person_id()

    add_results(person_id, db, choice_answers, long_answers)

main()
