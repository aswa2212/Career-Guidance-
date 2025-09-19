import re
import json
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class AptitudeScraper(BaseScraper):
    """Scraper for aptitude questions from various educational sources"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))
        self.questions = []
    
    def scrape_subject_based_questions(self) -> List[Dict]:
        """Create comprehensive aptitude questions for different subjects"""
        questions = []
        
        # Mathematics Questions
        math_questions = [
            {
                'question': 'If 2x + 3 = 11, what is the value of x?',
                'options': ['A) 3', 'B) 4', 'C) 5', 'D) 6'],
                'correct_answer': 'B',
                'subject': 'Mathematics',
                'difficulty': 'Easy',
                'topic': 'Algebra',
                'explanation': 'Solving: 2x + 3 = 11, 2x = 8, x = 4'
            },
            {
                'question': 'What is the area of a circle with radius 7 cm?',
                'options': ['A) 154 cm²', 'B) 144 cm²', 'C) 164 cm²', 'D) 174 cm²'],
                'correct_answer': 'A',
                'subject': 'Mathematics',
                'difficulty': 'Medium',
                'topic': 'Geometry',
                'explanation': 'Area = πr² = (22/7) × 7² = 154 cm²'
            },
            {
                'question': 'If log₂(8) = x, what is the value of x?',
                'options': ['A) 2', 'B) 3', 'C) 4', 'D) 8'],
                'correct_answer': 'B',
                'subject': 'Mathematics',
                'difficulty': 'Hard',
                'topic': 'Logarithms',
                'explanation': '2³ = 8, so log₂(8) = 3'
            },
            {
                'question': 'What is the derivative of x³?',
                'options': ['A) 3x²', 'B) x²', 'C) 3x', 'D) x³'],
                'correct_answer': 'A',
                'subject': 'Mathematics',
                'difficulty': 'Medium',
                'topic': 'Calculus',
                'explanation': 'd/dx(x³) = 3x²'
            },
            {
                'question': 'In a right triangle, if one angle is 30°, what is the other acute angle?',
                'options': ['A) 45°', 'B) 60°', 'C) 90°', 'D) 120°'],
                'correct_answer': 'B',
                'subject': 'Mathematics',
                'difficulty': 'Easy',
                'topic': 'Trigonometry',
                'explanation': 'Sum of angles in triangle = 180°, so 90° + 30° + x = 180°, x = 60°'
            }
        ]
        
        # Physics Questions
        physics_questions = [
            {
                'question': 'What is the SI unit of force?',
                'options': ['A) Joule', 'B) Newton', 'C) Watt', 'D) Pascal'],
                'correct_answer': 'B',
                'subject': 'Physics',
                'difficulty': 'Easy',
                'topic': 'Mechanics',
                'explanation': 'Newton (N) is the SI unit of force'
            },
            {
                'question': 'If a car travels 100 km in 2 hours, what is its average speed?',
                'options': ['A) 40 km/h', 'B) 50 km/h', 'C) 60 km/h', 'D) 200 km/h'],
                'correct_answer': 'B',
                'subject': 'Physics',
                'difficulty': 'Easy',
                'topic': 'Kinematics',
                'explanation': 'Speed = Distance/Time = 100/2 = 50 km/h'
            },
            {
                'question': 'What is the acceleration due to gravity on Earth?',
                'options': ['A) 9.8 m/s²', 'B) 10 m/s²', 'C) 8.9 m/s²', 'D) 11 m/s²'],
                'correct_answer': 'A',
                'subject': 'Physics',
                'difficulty': 'Easy',
                'topic': 'Gravity',
                'explanation': 'Standard acceleration due to gravity is 9.8 m/s²'
            },
            {
                'question': 'Which law states that energy cannot be created or destroyed?',
                'options': ['A) Newton\'s First Law', 'B) Law of Conservation of Energy', 'C) Ohm\'s Law', 'D) Boyle\'s Law'],
                'correct_answer': 'B',
                'subject': 'Physics',
                'difficulty': 'Medium',
                'topic': 'Energy',
                'explanation': 'The Law of Conservation of Energy states energy cannot be created or destroyed'
            },
            {
                'question': 'What is the speed of light in vacuum?',
                'options': ['A) 3×10⁸ m/s', 'B) 3×10⁶ m/s', 'C) 3×10¹⁰ m/s', 'D) 3×10⁴ m/s'],
                'correct_answer': 'A',
                'subject': 'Physics',
                'difficulty': 'Medium',
                'topic': 'Optics',
                'explanation': 'Speed of light in vacuum is approximately 3×10⁸ m/s'
            }
        ]
        
        # Chemistry Questions
        chemistry_questions = [
            {
                'question': 'What is the chemical symbol for Gold?',
                'options': ['A) Go', 'B) Au', 'C) Ag', 'D) Gd'],
                'correct_answer': 'B',
                'subject': 'Chemistry',
                'difficulty': 'Easy',
                'topic': 'Periodic Table',
                'explanation': 'Au is the chemical symbol for Gold (from Latin: Aurum)'
            },
            {
                'question': 'What is the pH of pure water?',
                'options': ['A) 6', 'B) 7', 'C) 8', 'D) 9'],
                'correct_answer': 'B',
                'subject': 'Chemistry',
                'difficulty': 'Easy',
                'topic': 'Acids and Bases',
                'explanation': 'Pure water has a pH of 7, which is neutral'
            },
            {
                'question': 'How many electrons can the first shell of an atom hold?',
                'options': ['A) 1', 'B) 2', 'C) 8', 'D) 18'],
                'correct_answer': 'B',
                'subject': 'Chemistry',
                'difficulty': 'Medium',
                'topic': 'Atomic Structure',
                'explanation': 'The first shell (K shell) can hold maximum 2 electrons'
            },
            {
                'question': 'What is the molecular formula of methane?',
                'options': ['A) CH₃', 'B) CH₄', 'C) C₂H₆', 'D) C₂H₄'],
                'correct_answer': 'B',
                'subject': 'Chemistry',
                'difficulty': 'Easy',
                'topic': 'Organic Chemistry',
                'explanation': 'Methane has the molecular formula CH₄'
            },
            {
                'question': 'Which gas is produced when metals react with acids?',
                'options': ['A) Oxygen', 'B) Carbon dioxide', 'C) Hydrogen', 'D) Nitrogen'],
                'correct_answer': 'C',
                'subject': 'Chemistry',
                'difficulty': 'Medium',
                'topic': 'Chemical Reactions',
                'explanation': 'Metals react with acids to produce hydrogen gas'
            }
        ]
        
        # Biology Questions
        biology_questions = [
            {
                'question': 'What is the powerhouse of the cell?',
                'options': ['A) Nucleus', 'B) Mitochondria', 'C) Ribosome', 'D) Chloroplast'],
                'correct_answer': 'B',
                'subject': 'Biology',
                'difficulty': 'Easy',
                'topic': 'Cell Biology',
                'explanation': 'Mitochondria are called the powerhouse of the cell as they produce ATP'
            },
            {
                'question': 'Which blood group is known as the universal donor?',
                'options': ['A) A', 'B) B', 'C) AB', 'D) O'],
                'correct_answer': 'D',
                'subject': 'Biology',
                'difficulty': 'Medium',
                'topic': 'Human Physiology',
                'explanation': 'O negative blood type is the universal donor'
            },
            {
                'question': 'What is the process by which plants make their food?',
                'options': ['A) Respiration', 'B) Photosynthesis', 'C) Transpiration', 'D) Digestion'],
                'correct_answer': 'B',
                'subject': 'Biology',
                'difficulty': 'Easy',
                'topic': 'Plant Biology',
                'explanation': 'Photosynthesis is the process by which plants make food using sunlight'
            },
            {
                'question': 'How many chambers does a human heart have?',
                'options': ['A) 2', 'B) 3', 'C) 4', 'D) 5'],
                'correct_answer': 'C',
                'subject': 'Biology',
                'difficulty': 'Easy',
                'topic': 'Human Anatomy',
                'explanation': 'Human heart has 4 chambers: 2 atria and 2 ventricles'
            },
            {
                'question': 'What is the basic unit of heredity?',
                'options': ['A) Chromosome', 'B) Gene', 'C) DNA', 'D) RNA'],
                'correct_answer': 'B',
                'subject': 'Biology',
                'difficulty': 'Medium',
                'topic': 'Genetics',
                'explanation': 'Gene is the basic unit of heredity'
            }
        ]
        
        # Computer Science Questions
        cs_questions = [
            {
                'question': 'What does CPU stand for?',
                'options': ['A) Central Processing Unit', 'B) Computer Personal Unit', 'C) Central Program Unit', 'D) Computer Processing Unit'],
                'correct_answer': 'A',
                'subject': 'Computer Science',
                'difficulty': 'Easy',
                'topic': 'Computer Hardware',
                'explanation': 'CPU stands for Central Processing Unit'
            },
            {
                'question': 'Which programming language is known as the "mother of all languages"?',
                'options': ['A) Java', 'B) Python', 'C) C', 'D) Assembly'],
                'correct_answer': 'C',
                'subject': 'Computer Science',
                'difficulty': 'Medium',
                'topic': 'Programming Languages',
                'explanation': 'C is often called the mother of all programming languages'
            },
            {
                'question': 'What is the time complexity of binary search?',
                'options': ['A) O(n)', 'B) O(log n)', 'C) O(n²)', 'D) O(1)'],
                'correct_answer': 'B',
                'subject': 'Computer Science',
                'difficulty': 'Hard',
                'topic': 'Algorithms',
                'explanation': 'Binary search has O(log n) time complexity'
            },
            {
                'question': 'Which data structure follows LIFO principle?',
                'options': ['A) Queue', 'B) Stack', 'C) Array', 'D) Linked List'],
                'correct_answer': 'B',
                'subject': 'Computer Science',
                'difficulty': 'Medium',
                'topic': 'Data Structures',
                'explanation': 'Stack follows Last In First Out (LIFO) principle'
            },
            {
                'question': 'What does HTML stand for?',
                'options': ['A) Hyper Text Markup Language', 'B) High Tech Modern Language', 'C) Home Tool Markup Language', 'D) Hyperlink and Text Markup Language'],
                'correct_answer': 'A',
                'subject': 'Computer Science',
                'difficulty': 'Easy',
                'topic': 'Web Development',
                'explanation': 'HTML stands for Hyper Text Markup Language'
            }
        ]
        
        # English Questions
        english_questions = [
            {
                'question': 'What is the synonym of "Happy"?',
                'options': ['A) Sad', 'B) Joyful', 'C) Angry', 'D) Tired'],
                'correct_answer': 'B',
                'subject': 'English',
                'difficulty': 'Easy',
                'topic': 'Vocabulary',
                'explanation': 'Joyful is a synonym of Happy'
            },
            {
                'question': 'Identify the noun in the sentence: "The cat runs quickly."',
                'options': ['A) The', 'B) cat', 'C) runs', 'D) quickly'],
                'correct_answer': 'B',
                'subject': 'English',
                'difficulty': 'Easy',
                'topic': 'Grammar',
                'explanation': 'Cat is the noun in the sentence'
            },
            {
                'question': 'What is the past tense of "go"?',
                'options': ['A) goes', 'B) going', 'C) went', 'D) gone'],
                'correct_answer': 'C',
                'subject': 'English',
                'difficulty': 'Easy',
                'topic': 'Tenses',
                'explanation': 'Went is the past tense of go'
            },
            {
                'question': 'Which of these is a metaphor?',
                'options': ['A) He runs like the wind', 'B) Time is money', 'C) The car is red', 'D) She sings beautifully'],
                'correct_answer': 'B',
                'subject': 'English',
                'difficulty': 'Medium',
                'topic': 'Literature',
                'explanation': 'Time is money is a metaphor comparing time to money'
            },
            {
                'question': 'What is the antonym of "Ancient"?',
                'options': ['A) Old', 'B) Modern', 'C) Historic', 'D) Traditional'],
                'correct_answer': 'B',
                'subject': 'English',
                'difficulty': 'Easy',
                'topic': 'Vocabulary',
                'explanation': 'Modern is the antonym of Ancient'
            }
        ]
        
        # Logical Reasoning Questions
        reasoning_questions = [
            {
                'question': 'If all roses are flowers and some flowers are red, which conclusion is correct?',
                'options': ['A) All roses are red', 'B) Some roses may be red', 'C) No roses are red', 'D) All red things are roses'],
                'correct_answer': 'B',
                'subject': 'Logical Reasoning',
                'difficulty': 'Medium',
                'topic': 'Syllogism',
                'explanation': 'Some roses may be red, but we cannot conclude all roses are red'
            },
            {
                'question': 'What comes next in the series: 2, 4, 8, 16, ?',
                'options': ['A) 24', 'B) 32', 'C) 20', 'D) 18'],
                'correct_answer': 'B',
                'subject': 'Logical Reasoning',
                'difficulty': 'Easy',
                'topic': 'Number Series',
                'explanation': 'Each number is doubled: 2×2=4, 4×2=8, 8×2=16, 16×2=32'
            },
            {
                'question': 'If BOOK is coded as CPPL, how is WORD coded?',
                'options': ['A) XPSE', 'B) XQSE', 'C) WQSE', 'D) XPSD'],
                'correct_answer': 'A',
                'subject': 'Logical Reasoning',
                'difficulty': 'Medium',
                'topic': 'Coding-Decoding',
                'explanation': 'Each letter is shifted by +1: W→X, O→P, R→S, D→E'
            },
            {
                'question': 'Find the odd one out: Apple, Banana, Carrot, Mango',
                'options': ['A) Apple', 'B) Banana', 'C) Carrot', 'D) Mango'],
                'correct_answer': 'C',
                'subject': 'Logical Reasoning',
                'difficulty': 'Easy',
                'topic': 'Classification',
                'explanation': 'Carrot is a vegetable, others are fruits'
            },
            {
                'question': 'If today is Wednesday, what day will it be after 15 days?',
                'options': ['A) Monday', 'B) Tuesday', 'C) Wednesday', 'D) Thursday'],
                'correct_answer': 'D',
                'subject': 'Logical Reasoning',
                'difficulty': 'Medium',
                'topic': 'Calendar',
                'explanation': '15 days = 2 weeks + 1 day, so Wednesday + 1 = Thursday'
            }
        ]
        
        # Combine all questions
        all_questions = (math_questions + physics_questions + chemistry_questions + 
                        biology_questions + cs_questions + english_questions + reasoning_questions)
        
        # Add metadata to each question
        for i, question in enumerate(all_questions):
            question['id'] = i + 1
            question['source'] = 'Educational Content Database'
            question['created_for'] = 'ML Model Training'
            question['career_relevance'] = self.get_career_relevance(question['subject'])
        
        return all_questions
    
    def get_career_relevance(self, subject: str) -> str:
        """Map subjects to relevant career fields"""
        career_mapping = {
            'Mathematics': 'Engineering, Data Science, Finance, Research, Teaching',
            'Physics': 'Engineering, Research, Astronomy, Medical Physics, Teaching',
            'Chemistry': 'Chemical Engineering, Pharmaceuticals, Research, Medicine, Teaching',
            'Biology': 'Medicine, Biotechnology, Research, Environmental Science, Teaching',
            'Computer Science': 'Software Development, Data Science, Cybersecurity, AI/ML, IT',
            'English': 'Literature, Journalism, Content Writing, Teaching, Communications',
            'Logical Reasoning': 'Management, Law, Consulting, Problem Solving, Analytics'
        }
        return career_mapping.get(subject, 'General Problem Solving')
    
    def create_advanced_questions(self) -> List[Dict]:
        """Create more advanced aptitude questions for better ML training"""
        advanced_questions = [
            # Advanced Mathematics
            {
                'question': 'A train travels 240 km in 3 hours. If it increases its speed by 20 km/h, how long will it take to travel the same distance?',
                'options': ['A) 2 hours', 'B) 2.4 hours', 'C) 2.5 hours', 'D) 3 hours'],
                'correct_answer': 'B',
                'subject': 'Mathematics',
                'difficulty': 'Hard',
                'topic': 'Speed-Time-Distance',
                'explanation': 'Original speed = 80 km/h, New speed = 100 km/h, Time = 240/100 = 2.4 hours',
                'career_relevance': 'Engineering, Data Science, Finance'
            },
            # Advanced Physics
            {
                'question': 'A ball is thrown upward with initial velocity 20 m/s. What is its velocity after 1 second? (g = 10 m/s²)',
                'options': ['A) 10 m/s', 'B) 15 m/s', 'C) 20 m/s', 'D) 30 m/s'],
                'correct_answer': 'A',
                'subject': 'Physics',
                'difficulty': 'Hard',
                'topic': 'Kinematics',
                'explanation': 'v = u - gt = 20 - 10×1 = 10 m/s',
                'career_relevance': 'Engineering, Research, Aerospace'
            },
            # Advanced Programming Logic
            {
                'question': 'What will be the output of this pseudocode?\nfor i = 1 to 3\n  print i * 2\nend for',
                'options': ['A) 1 2 3', 'B) 2 4 6', 'C) 1 4 9', 'D) 2 3 4'],
                'correct_answer': 'B',
                'subject': 'Computer Science',
                'difficulty': 'Hard',
                'topic': 'Programming Logic',
                'explanation': 'Loop prints: 1×2=2, 2×2=4, 3×2=6',
                'career_relevance': 'Software Development, Programming'
            }
        ]
        
        return advanced_questions
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method for aptitude questions"""
        all_questions = []
        
        try:
            # Get basic subject questions
            basic_questions = self.scrape_subject_based_questions()
            all_questions.extend(basic_questions)
            
            # Get advanced questions
            advanced_questions = self.create_advanced_questions()
            all_questions.extend(advanced_questions)
            
            logger.info(f"Created {len(all_questions)} aptitude questions")
            
            # Group by subject for ML model
            subject_distribution = {}
            for q in all_questions:
                subject = q['subject']
                subject_distribution[subject] = subject_distribution.get(subject, 0) + 1
            
            logger.info(f"Question distribution by subject: {subject_distribution}")
            
        except Exception as e:
            logger.error(f"Error during aptitude question creation: {e}")
        
        return all_questions
