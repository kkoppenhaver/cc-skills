#!/usr/bin/env python3
"""
YouTube Title Generator
Generates viral title options based on topic and style
"""

import random
import re
from typing import List, Dict

class TitleGenerator:
    def __init__(self):
        self.templates = {
            'curiosity': [
                "Why {topic} Is Actually {unexpected_result}",
                "The Real Reason {phenomenon}",
                "What Nobody Tells You About {topic}",
                "The Hidden {secret} of {subject}",
                "The Truth About {controversial_topic}",
                "{authority} Doesn't Want You to Know This About {topic}"
            ],
            'challenge': [
                "Can You {task}? (99% Fail)",
                "I {action} for {time_period} and {result}",
                "{number} Levels of {topic} (Level {max_level} Is Impossible)",
                "Try Not to {action} Challenge (Impossible)",
                "${amount} If You Can {challenge}"
            ],
            'educational': [
                "How to {desired_outcome} (Step-by-Step)",
                "{number} Ways to {achieve_goal}",
                "{topic} Explained in {number} Minutes",
                "Master {skill} in {time_period}",
                "The Only {topic} Guide You'll Ever Need",
                "Stop {mistake} - Do This Instead"
            ],
            'transformation': [
                "From {bad_state} to {good_state} in {time_period}",
                "This {method} Changed My {aspect}",
                "I Went From {start} to {end} in {time}",
                "How I {achievement} in Just {time_period}",
                "My ${amount} {type} Transformation"
            ],
            'comparison': [
                "${price1} vs ${price2} {item}",
                "{option1} vs {option2}: The Winner Shocked Me",
                "I Tested {number} {items} - Here's the Best",
                "Is {expensive_option} Worth It?",
                "{old_way} vs {new_way}: Mind-Blowing Results"
            ],
            'story': [
                "The Day That Changed Everything",
                "I {extreme_action} So You Don't Have To",
                "They Said {limitation}, So I {proved_wrong}",
                "My ${amount} Mistake",
                "Why I Quit {thing} After {achievement}"
            ]
        }
    
    def generate_titles(self, topic: str, style: str = None, count: int = 5) -> List[str]:
        """Generate title options for a given topic and style"""
        
        if style and style in self.templates:
            templates = self.templates[style]
        else:
            # Use all templates if no style specified
            templates = []
            for template_list in self.templates.values():
                templates.extend(template_list)
        
        titles = []
        used_templates = []
        
        for _ in range(count):
            available_templates = [t for t in templates if t not in used_templates]
            if not available_templates:
                available_templates = templates
                used_templates = []
            
            template = random.choice(available_templates)
            used_templates.append(template)
            
            title = self._fill_template(template, topic)
            titles.append(title)
        
        return titles
    
    def _fill_template(self, template: str, topic: str) -> str:
        """Fill in template variables with contextual content"""
        
        replacements = {
            'topic': topic,
            'number': str(random.choice([3, 5, 7, 10, 15, 21, 30])),
            'time_period': random.choice(['24 Hours', '7 Days', '30 Days', '1 Year']),
            'amount': str(random.choice([100, 500, 1000, 5000, 10000, 50000, 100000])),
            'price1': str(random.choice([1, 10, 100])),
            'price2': str(random.choice([1000, 10000, 100000, 1000000])),
            'max_level': str(random.choice([5, 10, 100])),
            
            # Context-aware replacements
            'unexpected_result': f"the Best {topic} Strategy",
            'phenomenon': f"Everyone's Obsessed with {topic}",
            'secret': f"Secret",
            'subject': topic,
            'controversial_topic': topic,
            'authority': random.choice(['Experts', 'Big Tech', 'The Industry']),
            'task': f"Master {topic} in 1 Day",
            'action': f"Studied {topic}",
            'result': "These Were the Results",
            'desired_outcome': f"Master {topic}",
            'achieve_goal': f"Improve Your {topic} Skills",
            'skill': topic,
            'mistake': f"Making These {topic} Mistakes",
            'bad_state': "Complete Beginner",
            'good_state': "Expert Level",
            'method': f"{topic} Technique",
            'aspect': "Life",
            'start': "Zero",
            'end': "Hero",
            'achievement': "10,000 Hours",
            'type': topic,
            'item': topic,
            'items': f"{topic} Tools",
            'option1': f"Traditional {topic}",
            'option2': f"Modern {topic}",
            'expensive_option': f"Premium {topic}",
            'old_way': "The Old Method",
            'new_way': "This New Technique",
            'extreme_action': f"Lived Like a {topic} Expert",
            'limitation': f"You Can't Learn {topic} Fast",
            'proved_wrong': "Proved Them Wrong",
            'thing': topic,
            'challenge': f"Beat My {topic} Score"
        }
        
        # Replace all placeholders
        for key, value in replacements.items():
            pattern = r'\{' + key + r'\}'
            if re.search(pattern, template):
                template = re.sub(pattern, value, template)
        
        return template
    
    def generate_with_metrics(self, topic: str, style: str = None) -> List[Dict]:
        """Generate titles with predicted performance metrics"""
        
        titles = self.generate_titles(topic, style, count=10)
        results = []
        
        for title in titles:
            # Simple heuristic scoring
            score = 0
            
            # Length scoring (optimal 40-60 chars)
            length = len(title)
            if 40 <= length <= 60:
                score += 20
            elif 30 <= length <= 70:
                score += 10
            
            # Power word scoring
            power_words = ['secret', 'shocking', 'truth', 'actually', 'nobody', 
                          'impossible', 'changed', 'mistake', 'quit', 'master']
            for word in power_words:
                if word.lower() in title.lower():
                    score += 10
            
            # Number inclusion
            if any(char.isdigit() for char in title):
                score += 15
            
            # Question format
            if '?' in title:
                score += 10
            
            # Dollar amount
            if '$' in title:
                score += 15
            
            results.append({
                'title': title,
                'length': length,
                'score': min(score, 100),
                'style': style or 'mixed'
            })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results

def main():
    """Example usage"""
    generator = TitleGenerator()
    
    # Get topic from user
    topic = input("Enter your video topic: ")
    
    print("\nSelect style:")
    print("1. Curiosity Gap")
    print("2. Challenge")
    print("3. Educational")
    print("4. Transformation")
    print("5. Comparison")
    print("6. Story")
    print("7. Mixed (All styles)")
    
    choice = input("\nEnter choice (1-7): ")
    
    style_map = {
        '1': 'curiosity',
        '2': 'challenge',
        '3': 'educational',
        '4': 'transformation',
        '5': 'comparison',
        '6': 'story',
        '7': None
    }
    
    style = style_map.get(choice, None)
    
    print(f"\n🎬 Generated Titles for '{topic}':\n")
    print("=" * 60)
    
    results = generator.generate_with_metrics(topic, style)
    
    for i, result in enumerate(results[:5], 1):
        print(f"\n{i}. {result['title']}")
        print(f"   📊 Score: {result['score']}/100")
        print(f"   📏 Length: {result['length']} chars")
        print(f"   🎯 Style: {result['style']}")

if __name__ == "__main__":
    main()
