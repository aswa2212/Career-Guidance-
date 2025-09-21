import re
import json
import random
from typing import List, Dict, Any
from .base_scraper import BaseScraper, logger

class AptitudeScraper(BaseScraper):
    """Enhanced scraper for aptitude questions with real-time generation"""
    
    def __init__(self):
        super().__init__(delay_range=(2, 4))
        self.questions = []
        self.question_templates = self._load_question_templates()
    
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
    
    def _load_question_templates(self) -> Dict[str, List[Dict]]:
        """Load question templates for dynamic generation"""
        return {
            'mathematics': [
                {
                    'template': 'If {a}x + {b} = {c}, what is the value of x?',
                    'answer_func': lambda a, b, c: (c - b) / a,
                    'difficulty': 'Easy'
                },
                {
                    'template': 'What is the area of a circle with radius {r} cm?',
                    'answer_func': lambda r: 3.14159 * r * r,
                    'difficulty': 'Medium'
                },
                {
                    'template': 'If a train travels {distance} km in {time} hours, what is its speed?',
                    'answer_func': lambda distance, time: distance / time,
                    'difficulty': 'Easy'
                }
            ],
            'logical_reasoning': [
                {
                    'template': 'What comes next in the series: {series}?',
                    'pattern_type': 'arithmetic',
                    'difficulty': 'Medium'
                },
                {
                    'template': 'If all {category1} are {category2} and some {category2} are {category3}, which conclusion is correct?',
                    'difficulty': 'Hard'
                }
            ]
        }
    
    def generate_dynamic_questions(self, count: int = 50) -> List[Dict]:
        """Generate dynamic aptitude questions"""
        questions = []
        
        # Generate math questions
        for i in range(count // 3):
            # Linear equation questions
            a = random.randint(2, 10)
            b = random.randint(1, 20)
            c = random.randint(10, 50)
            x = (c - b) / a
            
            options = [x, x + 1, x - 1, x + 2]
            random.shuffle(options)
            correct_idx = options.index(x)
            
            questions.append({
                'question': f'If {a}x + {b} = {c}, what is the value of x?',
                'options': [f'{chr(65+i)}) {opt}' for i, opt in enumerate(options)],
                'correct_answer': chr(65 + correct_idx),
                'subject': 'Mathematics',
                'difficulty': 'Easy',
                'topic': 'Algebra',
                'explanation': f'Solving: {a}x + {b} = {c}, {a}x = {c-b}, x = {x}',
                'id': len(questions) + 1,
                'source': 'Dynamic Generation',
                'career_relevance': 'Engineering, Data Science, Finance'
            })
        
        # Generate logical reasoning questions
        for i in range(count // 3):
            # Number series
            start = random.randint(1, 10)
            diff = random.randint(2, 5)
            series = [start + i * diff for i in range(4)]
            next_num = series[-1] + diff
            
            options = [next_num, next_num + diff, next_num - diff, next_num + 2*diff]
            random.shuffle(options)
            correct_idx = options.index(next_num)
            
            questions.append({
                'question': f'What comes next in the series: {", ".join(map(str, series))}, ?',
                'options': [f'{chr(65+i)}) {opt}' for i, opt in enumerate(options)],
                'correct_answer': chr(65 + correct_idx),
                'subject': 'Logical Reasoning',
                'difficulty': 'Medium',
                'topic': 'Number Series',
                'explanation': f'Each number increases by {diff}: {series[-1]} + {diff} = {next_num}',
                'id': len(questions) + 1,
                'source': 'Dynamic Generation',
                'career_relevance': 'Management, Analytics, Problem Solving'
            })
        
        # Generate general knowledge questions
        gk_questions = [
            {
                'question': 'What is the capital of India?',
                'options': ['A) Mumbai', 'B) New Delhi', 'C) Kolkata', 'D) Chennai'],
                'correct_answer': 'B',
                'subject': 'General Knowledge',
                'difficulty': 'Easy',
                'topic': 'Geography'
            },
            {
                'question': 'Who is known as the Father of the Nation in India?',
                'options': ['A) Jawaharlal Nehru', 'B) Mahatma Gandhi', 'C) Sardar Patel', 'D) Subhas Chandra Bose'],
                'correct_answer': 'B',
                'subject': 'General Knowledge',
                'difficulty': 'Easy',
                'topic': 'History'
            },
            {
                'question': 'Which planet is known as the Red Planet?',
                'options': ['A) Venus', 'B) Jupiter', 'C) Mars', 'D) Saturn'],
                'correct_answer': 'C',
                'subject': 'General Knowledge',
                'difficulty': 'Easy',
                'topic': 'Science'
            }
        ]
        
        for i, gk in enumerate(gk_questions[:count//3]):
            gk.update({
                'id': len(questions) + i + 1,
                'source': 'Curated Content',
                'explanation': f'This is a standard {gk["topic"].lower()} question.',
                'career_relevance': 'General Knowledge, Civil Services, Teaching'
            })
            questions.append(gk)
        
        return questions
    
    def scrape_online_aptitude_sources(self) -> List[Dict]:
        """Try to scrape aptitude questions from online sources"""
        questions = []
        
        try:
            # Try to get questions from aptitude websites
            aptitude_sites = [
                'https://www.indiabix.com/aptitude/questions-and-answers/',
                'https://www.geeksforgeeks.org/aptitude-questions-and-answers/'
            ]
            
            for site in aptitude_sites:
                try:
                    soup = self.get_page(site)
                    if soup:
                        # Look for question patterns
                        question_elements = soup.find_all(['div', 'p'], class_=re.compile(r'question|problem'))
                        
                        for elem in question_elements[:5]:  # Limit to avoid too many requests
                            question_text = self.clean_text(elem.get_text())
                            if len(question_text) > 20 and '?' in question_text:
                                questions.append({
                                    'question': question_text,
                                    'options': ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4'],
                                    'correct_answer': 'A',
                                    'subject': 'Aptitude',
                                    'difficulty': 'Medium',
                                    'topic': 'General',
                                    'source': 'Online Source',
                                    'explanation': 'Scraped from online aptitude source',
                                    'career_relevance': 'General Aptitude'
                                })
                except Exception as e:
                    logger.warning(f"Error scraping {site}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping online aptitude sources: {e}")
        
        return questions
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Main scraping method for aptitude questions with real-time generation"""
        all_questions = []
        
        try:
            # Try to get questions from online sources
            logger.info("Attempting to scrape online aptitude sources...")
            online_questions = self.scrape_online_aptitude_sources()
            all_questions.extend(online_questions)
            
            # Generate dynamic questions
            logger.info("Generating dynamic aptitude questions...")
            dynamic_questions = self.generate_dynamic_questions(60)
            all_questions.extend(dynamic_questions)
            
            # Get curated subject questions as fallback
            logger.info("Adding curated subject questions...")
            basic_questions = self.scrape_subject_based_questions()
            all_questions.extend(basic_questions)
            
            # Get advanced questions
            advanced_questions = self.create_advanced_questions()
            all_questions.extend(advanced_questions)
            
            # Shuffle questions for variety
            random.shuffle(all_questions)
            
            logger.info(f"Created {len(all_questions)} total aptitude questions")
            
            # Group by subject for ML model
            subject_distribution = {}
            for q in all_questions:
                subject = q.get('subject', 'Unknown')
                subject_distribution[subject] = subject_distribution.get(subject, 0) + 1
            
            logger.info(f"Question distribution by subject: {subject_distribution}")
            
        except Exception as e:
            logger.error(f"Error during aptitude question creation: {e}")
            # Return at least some questions even if there's an error
            if not all_questions:
                all_questions = self.scrape_subject_based_questions()[:20]
        
        return all_questions[:100]  # Limit to 100 questions
