"""populate courses"""
from django.core.management.base import BaseCommand
from lesson.models import Course, Module, Quiz, Question, AnswerOption, Assignment
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        # Seed Courses
        if Course.objects.exists():
            self.stdout.write(self.style.SUCCESS('Skipping Seeding because courses are available already...'))
            return
        self.stdout.write(self.style.SUCCESS('Seeding Courses...'))
        courses = [
            {
                'title': 'Introduction to AI',
                'thumbnail': 'https://www.aiperspectives.com/wp-content/uploads/2020/03/iStock-1148923626.jpg',
                'description': 'A basic introduction to AI concepts.',
                'is_premium': False,
                'level': 'beginner'
            },
            {
                'title': 'Intermediate AI Concepts',
                'thumbnail': 'https://cdn.prod.website-files.com/65ea23d5dcd20a7abc7f1eae/66206b0ee06bbf8398803f65_AI_Training_Data_Concept.jpeg',
                'description': 'Dive deeper into AI technologies and methodologies.',
                'is_premium': False,
                'level': 'intermediate'
            },
            {
                'title': 'AI and Machine Learning',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRyt6x8bUjK5YCXlp3Rjj4N1mtvCfeLAJY2tA&s',
                'description': 'Explore machine learning techniques in AI.',
                'is_premium': True,
                'level': 'expert'
            },
            {
                'title': 'Neural Networks and Deep Learning',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQTDBT4p6sM65_iLtmSW7gMWxCD66N7HEekaQ&s',
                'description': 'Understanding deep learning models and architectures.',
                'is_premium': True,
                'level': 'expert'
            },
            {
                'title': 'AI Ethics and Future',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ0SLfTetH14ro2GAJrX_9x9cKqMmKGZx2jOw&s',
                'description': 'Understanding the ethical issues in AI development.',
                'is_premium': False,
                'level': 'beginner'
            },
            {
                'title': 'Computer Vision with AI',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTh4ROWp38RhgQwGP3UAP3ydOWFy8SkH4whbA&s',
                'description': 'Learn how AI is used to process and understand images.',
                'is_premium': True,
                'level': 'intermediate'
            },
            {
                'title': 'Natural Language Processing',
                'thumbnail': 'https://miro.medium.com/v2/resize:fit:1200/0*fgUmB5Ou19X4-4tX.png',
                'description': 'Learn about processing and analyzing human language using AI.',
                'is_premium': False,
                'level': 'intermediate'
            },
            {
                'title': 'Reinforcement Learning',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ3OASlWnKOWMO9TmEoxgOxN1J-KQP0AyEzxA&s',
                'description': 'Study the basics of reinforcement learning algorithms.',
                'is_premium': True,
                'level': 'expert'
            },
            {
                'title': 'AI in Healthcare',
                'thumbnail': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQQ4DQ1R0TYvGCOyAx956reEWvfUEleioK75A&s',
                'description': 'Explore how AI is revolutionizing the healthcare industry.',
                'is_premium': False,
                'level': 'intermediate'
            },
            {
                'title': 'AI in Robotics',
                'thumbnail': 'https://onlinedegrees.sandiego.edu/wp-content/uploads/2023/04/Applications-of-AI-in-Robots_An-Introduction.jpg',
                'description': 'Learn how AI and robotics intersect to build intelligent machines.',
                'is_premium': True,
                'level': 'expert'
            }
        ]

        course_objects = []
        for course_data in courses:
            course = Course.objects.create(**course_data)
            course_objects.append(course)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(course_objects)} courses.'))

        # Seed Modules for each Course
        self.stdout.write(self.style.SUCCESS('Seeding Modules...'))
        modules = [
            {
                'course': course_objects[0],
                'title': 'AI Overview',
                'description': 'Introduction to AI and its applications.',
                'content': 'AI is the simulation of human intelligence processes...',
                'video_url': 'https://www.youtube.com/embed/Y46zXHvUB1s'
            },
            {
                'course': course_objects[0],
                'title': 'AI Algorithms',
                'description': 'Learn various algorithms used in AI.',
                'content': 'Algorithms in AI are critical for decision making...',
                'video_url': 'https://www.youtube.com/embed/olFxW7kdtP8'
            },
            {
                'course': course_objects[0],
                'title': 'Machine Learning Foundations',
                'description': 'Explore the foundational aspects of machine learning.',
                'content': 'Machine learning is a subset of AI that allows systems to learn from data...',
                'video_url': 'https://www.youtube.com/embed/Beh13Cd_QbY'
            },
            {
                'course': course_objects[1],
                'title': 'Deep Learning Techniques',
                'description': 'Deep dive into neural networks and learning techniques.',
                'content': 'Deep learning allows AI to simulate the neural networks of the human brain...',
                'video_url': 'https://www.youtube.com/embed/VyWAvY2CF9c'
            },
            {
                'course': course_objects[1],
                'title': 'Ethics in AI',
                'description': 'Understanding the impact of AI on society and ethics.',
                'content': 'Ethical considerations are vital in the development and deployment of AI systems...',
                'video_url': 'https://www.youtube.com/embed/qpp1G0iEL_c'
            },
            # for neural networks
            {
                'course':course_objects[3],
                'title': 'Introduction to Neural Networks',
                'description': 'An overview of artificial neural networks and how they mimic the human brain to solve complex problems.',
                'content': 'This module introduces the fundamentals of neural networks, including perceptrons, activation functions, and the concept of layers.',
                'video_url': 'https://www.youtube.com/embed/aircAruvnKk'
            },
            {
                'course': course_objects[3],
                'title': 'Understanding Feedforward Neural Networks',
                'description': 'Dive deeper into the architecture of feedforward neural networks and how they process input data to generate output.',
                'content': 'Explore the structure and function of feedforward neural networks, including forward propagation, weights, and biases.',
                'video_url': 'https://www.youtube.com/embed/aircAruvnKk'
            },
            # for neural networks
            {
                'course': course_objects[5],
                'title': 'Convolutional Neural Networks (CNNs) for Image Classification',
                'description': 'A deep dive into CNNs, which are crucial for image classification and recognition tasks.',
                'content': 'Understand how convolutional layers, pooling layers, and fully connected layers contribute to image classification models.',
                'video_url': 'https://www.youtube.com/embed/YRhxdVk_sIs'
            },
            {
                'course': course_objects[5],
                'title': 'Object Detection with Computer Vision',
                'description': 'Learn how object detection models are used to locate and classify objects within images and videos.',
                'content': 'This module covers the techniques of object detection, including YOLO (You Only Look Once), Faster R-CNN, and SSD.',
                'video_url': 'https://www.youtube.com/embed/ag3DLKsl2vk'
            },
            {
                'course': course_objects[9],
                'title': 'Robot Motion and Control',
                'description': 'An introduction to motion planning and control systems for autonomous robots.',
                'content': 'This module covers motion planning algorithms such as A* and RRT, as well as control systems used to move robots within their environments.',
                'video_url': 'https://www.youtube.com/embed/wm0f_V3l9z4'
            },
            {
                'course': course_objects[9],
                'title': 'Robotic Manipulation',
                'description': 'Understand the mechanics and control of robotic arms for tasks like grasping, picking, and assembly.',
                'content': 'This module covers robotic manipulation techniques, including inverse kinematics, grasp planning, and real-time control for performing complex tasks.',
                'video_url': 'https://www.youtube.com/embed/mCI-f71MAvY'
            },
            # for reinforcement learning
            {
                'course': course_objects[7],
                'title': 'Introduction to Reinforcement Learning',
                'description': 'An introduction to the core concepts of reinforcement learning (RL).',
                'content': 'This module covers the foundational concepts of RL, including agents, environments, actions, rewards, and policies.',
                'video_url': 'https://www.youtube.com/embed/RmOdTQYQqmQ'
            },
            {
                'course': course_objects[7],
                'title': 'Markov Decision Processes (MDPs)',
                'description': 'Learn about MDPs and their role in reinforcement learning.',
                'content': 'This module delves into Markov Decision Processes, the mathematical framework for RL, including states, actions, rewards, and transition probabilities.',
                'video_url': 'https://www.youtube.com/embed/2iF9PRriA7w'
            },
        ]
        for module_data in modules:
            Module.objects.create(**module_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(modules)} modules.'))

        # Seed Quizzes and Questions
        self.stdout.write(self.style.SUCCESS('Seeding Quizzes and Questions...'))
        quizzes = [
            {
                'module': Module.objects.get(title='AI Overview'),
                'title': 'Intro to AI Quiz'
            },
            {
                'module': Module.objects.get(title='AI Algorithms'),
                'title': 'Algorithms Quiz'
            },
        ]
        quiz_objects = []
        for quiz_data in quizzes:
            quiz = Quiz.objects.create(**quiz_data)
            quiz_objects.append(quiz)

        # Seed Questions for each Quiz
        questions_data = [
            {
                'quiz': quiz_objects[0],
                'text': 'What is Artificial Intelligence?'
            },
            {
                'quiz': quiz_objects[0],
                'text': 'Which algorithm is commonly used in AI?'
            },
            {
                'quiz': quiz_objects[0],
                'text': 'What is supervised learning in ML?'
            },
            {
                'quiz': quiz_objects[0],
                'text': 'What is a neural network?'
            },
            {
                'quiz': quiz_objects[0],
                'text': 'What are ethical concerns in AI development?'
            },
        ]
        question_objects = []
        for question_data in questions_data:
            question = Question.objects.create(**question_data)
            question_objects.append(question)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(question_objects)} questions.'))

        # Seed Answer Options for each Question
        answer_options_data = [
            # For Question: 'What is Artificial Intelligence?'
            {
                'question': question_objects[0],
                'text': 'A machine that mimics human behavior.',
                'is_correct': True
            },
            {
                'question': question_objects[0],
                'text': 'A device used for calculations.',
                'is_correct': False
            },
            {
                'question': question_objects[0],
                'text': 'A programming language for AI.',
                'is_correct': False
            },

            # For Question: 'Which algorithm is commonly used in AI?'
            {
                'question': question_objects[1],
                'text': 'Linear Regression',
                'is_correct': True
            },
            {
                'question': question_objects[1],
                'text': 'Dijkstra\'s Algorithm',
                'is_correct': False
            },
            {
                'question': question_objects[1],
                'text': 'Binary Search',
                'is_correct': False
            },

            # For Question: 'What is supervised learning in ML?'
            {
                'question': question_objects[2],
                'text': 'Learning with labeled data to predict outcomes.',
                'is_correct': True
            },
            {
                'question': question_objects[2],
                'text': 'Learning without any labeled data.',
                'is_correct': False
            },
            {
                'question': question_objects[2],
                'text': 'Learning from trial and error.',
                'is_correct': False
            },

            # For Question: 'What is a neural network?'
            {
                'question': question_objects[3],
                'text': 'A system that mimics the brain\'s neural architecture.',
                'is_correct': True
            },
            {
                'question': question_objects[3],
                'text': 'A machine that computes numbers.',
                'is_correct': False
            },
            {
                'question': question_objects[3],
                'text': 'A type of unsupervised learning algorithm.',
                'is_correct': False
            },

            # For Question: 'What are ethical concerns in AI development?'
            {
                'question': question_objects[4],
                'text': 'Bias in decision-making processes.',
                'is_correct': True
            },
            {
                'question': question_objects[4],
                'text': 'Increased job opportunities for workers.',
                'is_correct': False
            },
            {
                'question': question_objects[4],
                'text': 'Decreased human dependency on technology.',
                'is_correct': False
            },
        ]

        for answer_option_data in answer_options_data:
            AnswerOption.objects.create(**answer_option_data)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded answer options.'))

        # Seed Assignments
        self.stdout.write(self.style.SUCCESS('Seeding Assignments...'))
        assignments_data = [
            {
                'title': 'AI Fundamentals Assignment',
                'module': Module.objects.get(title='AI Overview'),
                'text': 'Explain the basics of AI and its applications.'
            },
            {
                'title': 'AI Algorithms Assignment',
                'module': Module.objects.get(title='AI Algorithms'),
                'text': 'List and explain the most commonly used AI algorithms.'
            },
            {
                'title': 'ML Foundations Assignment',
                'module': Module.objects.get(title='Machine Learning Foundations'),
                'text': 'Discuss the different types of machine learning models.'
            }
        ]
        for assignment_data in assignments_data:
            Assignment.objects.create(**assignment_data)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
