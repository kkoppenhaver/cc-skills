#!/usr/bin/env python3
"""
YouTube Shorts Extractor
Identifies short-worthy moments from video outlines
"""

import re
from typing import List, Dict, Tuple
from dataclasses import dataclass
import json

@dataclass
class ShortConcept:
    """A potential YouTube Short concept"""
    type: str
    title: str
    description: str
    duration: str
    hook: str
    content: str
    source_section: str
    viral_potential: int

class ShortsExtractor:
    def __init__(self):
        self.short_types = {
            'hook': {
                'duration': '15-30 seconds',
                'description': 'Most impactful moment as standalone teaser',
                'viral_potential': 85
            },
            'tip': {
                'duration': '30-45 seconds',
                'description': 'Single actionable tip or trick',
                'viral_potential': 70
            },
            'reveal': {
                'duration': '15-30 seconds',
                'description': 'Big reveal or surprising result',
                'viral_potential': 90
            },
            'process': {
                'duration': '45-60 seconds',
                'description': 'Quick how-to or demonstration',
                'viral_potential': 65
            },
            'story': {
                'duration': '30-60 seconds',
                'description': 'Complete micro-story with payoff',
                'viral_potential': 75
            },
            'comparison': {
                'duration': '30-45 seconds',
                'description': 'Quick A vs B comparison',
                'viral_potential': 70
            },
            'myth': {
                'duration': '15-30 seconds',
                'description': 'Myth-busting or misconception correction',
                'viral_potential': 80
            },
            'behind_scenes': {
                'duration': '30-45 seconds',
                'description': 'Making-of or blooper moment',
                'viral_potential': 60
            }
        }
        
        self.trigger_phrases = {
            'hook': ['most people think', 'what if i told you', 'nobody talks about', 
                    'the truth is', 'biggest mistake'],
            'tip': ['pro tip', 'quick tip', 'here\'s how', 'secret trick', 
                   'simple hack'],
            'reveal': ['the result', 'it turns out', 'the answer', 'shocking discovery',
                      'plot twist'],
            'process': ['step by step', 'how to', 'tutorial', 'first you', 
                       'the process'],
            'story': ['one time', 'story time', 'this happened', 'let me tell you',
                     'real quick story'],
            'comparison': ['versus', 'vs', 'compared to', 'difference between',
                          'better than'],
            'myth': ['myth', 'misconception', 'people believe', 'actually false',
                    'common mistake'],
            'behind_scenes': ['blooper', 'behind the scenes', 'what went wrong',
                             'failed attempt']
        }
    
    def extract_shorts(self, video_outline: str) -> List[ShortConcept]:
        """Extract potential shorts from a video outline"""
        
        shorts = []
        sections = self._parse_outline(video_outline)
        
        for section_title, section_content in sections.items():
            # Check each section for short-worthy content
            potential_shorts = self._analyze_section(section_title, section_content)
            shorts.extend(potential_shorts)
        
        # Sort by viral potential
        shorts.sort(key=lambda x: x.viral_potential, reverse=True)
        
        # Limit to top 5 concepts
        return shorts[:5]
    
    def _parse_outline(self, outline: str) -> Dict[str, str]:
        """Parse outline into sections"""
        
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        lines = outline.split('\n')
        
        for line in lines:
            # Check if this is a section header
            if re.match(r'^(#{1,3}|Act \d|Part \d|\d+\.)', line):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('#').strip()
                current_content = []
            else:
                if line.strip():
                    current_content.append(line.strip())
        
        # Add the last section
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _analyze_section(self, title: str, content: str) -> List[ShortConcept]:
        """Analyze a section for short potential"""
        
        shorts = []
        lower_content = content.lower()
        
        # Check for trigger phrases
        for short_type, phrases in self.trigger_phrases.items():
            for phrase in phrases:
                if phrase in lower_content:
                    short = self._create_short_concept(
                        short_type, title, content, phrase
                    )
                    if short:
                        shorts.append(short)
                    break  # Only one short per type per section
        
        # Special checks for high-value content
        if re.search(r'\$\d+', content):  # Money mentioned
            short = self._create_short_concept('reveal', title, content, 'money')
            if short:
                shorts.append(short)
        
        if re.search(r'\d+%', content):  # Statistics mentioned
            short = self._create_short_concept('myth', title, content, 'statistic')
            if short:
                shorts.append(short)
        
        if '?' in content:  # Questions that could be hooks
            short = self._create_short_concept('hook', title, content, 'question')
            if short:
                shorts.append(short)
        
        return shorts
    
    def _create_short_concept(self, short_type: str, section: str, 
                            content: str, trigger: str) -> ShortConcept:
        """Create a short concept from section content"""
        
        if short_type not in self.short_types:
            return None
        
        type_info = self.short_types[short_type]
        
        # Generate title based on type
        title = self._generate_short_title(short_type, content, trigger)
        
        # Generate hook
        hook = self._generate_hook(short_type, content)
        
        # Extract relevant content (first 100 chars for brevity)
        relevant_content = content[:200] + "..." if len(content) > 200 else content
        
        return ShortConcept(
            type=short_type,
            title=title,
            description=type_info['description'],
            duration=type_info['duration'],
            hook=hook,
            content=relevant_content,
            source_section=section,
            viral_potential=type_info['viral_potential']
        )
    
    def _generate_short_title(self, short_type: str, content: str, 
                            trigger: str) -> str:
        """Generate a title for the short"""
        
        titles = {
            'hook': ["Wait, WHAT?! 🤯", "This Changes Everything", "You Won't Believe This"],
            'tip': ["60-Second Hack", "Try This Today", "Game-Changing Tip"],
            'reveal': ["The Answer Will Shock You", "Plot Twist!", "I Was Wrong..."],
            'process': ["How To in 60 Seconds", "Quick Tutorial", "Watch Me Do This"],
            'story': ["Storytime!", "This Actually Happened", "You Need To Hear This"],
            'comparison': ["Which Is Better?", "The Winner Is...", "Tested & Compared"],
            'myth': ["MYTH BUSTED", "Everyone Gets This Wrong", "The Truth About..."],
            'behind_scenes': ["What Really Happened", "Behind The Scenes", "Blooper Alert"]
        }
        
        # Get first few words of content for context
        first_words = ' '.join(content.split()[:5])
        
        base_title = titles.get(short_type, ["Must Watch"])[0]
        
        # Add emoji based on content
        if '$' in content:
            base_title += " 💰"
        elif '?' in content:
            base_title += " 🤔"
        elif 'fail' in content.lower():
            base_title += " 😅"
        
        return base_title
    
    def _generate_hook(self, short_type: str, content: str) -> str:
        """Generate a hook for the short"""
        
        hooks = {
            'hook': "POV: You just learned something that changes everything...",
            'tip': "Stop scrolling! This tip will save you hours...",
            'reveal': "The result? I couldn't believe it either...",
            'process': "Learn this in 60 seconds or less...",
            'story': "Let me tell you what happened...",
            'comparison': "I tested both so you don't have to...",
            'myth': "Everyone believes this, but here's the truth...",
            'behind_scenes': "Here's what you didn't see..."
        }
        
        return hooks.get(short_type, "Watch this...")
    
    def generate_short_scripts(self, short: ShortConcept) -> str:
        """Generate a brief script for a short"""
        
        script = []
        script.append(f"TITLE: {short.title}")
        script.append(f"DURATION: {short.duration}")
        script.append("")
        script.append("SCRIPT:")
        script.append(f"[0-3 seconds] HOOK: {short.hook}")
        
        if short.type == 'hook':
            script.append("[3-15 seconds] BUILD: Create tension with the question/problem")
            script.append("[15-25 seconds] REVEAL: Show the surprising answer/result")
            script.append("[25-30 seconds] CTA: 'Full video explains everything - link in bio'")
        
        elif short.type == 'tip':
            script.append("[3-10 seconds] PROBLEM: Show what people usually do wrong")
            script.append("[10-30 seconds] SOLUTION: Demonstrate the better way")
            script.append("[30-40 seconds] RESULT: Show the improvement")
            script.append("[40-45 seconds] CTA: 'Follow for more tips like this'")
        
        elif short.type == 'reveal':
            script.append("[3-10 seconds] SETUP: Context for the reveal")
            script.append("[10-20 seconds] BUILD: Increase anticipation")
            script.append("[20-28 seconds] REVEAL: The big moment")
            script.append("[28-30 seconds] REACTION: Your genuine response")
        
        elif short.type == 'process':
            script.append("[3-10 seconds] INTRO: What we're making/doing")
            script.append("[10-40 seconds] STEPS: Quick, clear demonstration")
            script.append("[40-55 seconds] RESULT: Show the finished product")
            script.append("[55-60 seconds] CTA: 'Save this for later!'")
        
        elif short.type == 'story':
            script.append("[3-10 seconds] SETUP: Quick context")
            script.append("[10-40 seconds] STORY: The main narrative")
            script.append("[40-55 seconds] TWIST/LESSON: The payoff")
            script.append("[55-60 seconds] CTA: 'What would you have done?'")
        
        else:
            script.append("[3-45 seconds] CONTENT: Main content")
            script.append("[45-60 seconds] CTA: Engagement prompt")
        
        script.append("")
        script.append("CAPTION:")
        script.append(f"{short.hook} {short.title}")
        script.append("#shorts #viral #fyp")
        
        return '\n'.join(script)

def format_short_concept(short: ShortConcept) -> str:
    """Format a short concept for display"""
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"🎬 {short.title}")
    output.append(f"{'='*60}")
    output.append(f"Type: {short.type.upper()}")
    output.append(f"Duration: {short.duration}")
    output.append(f"Viral Potential: {short.viral_potential}/100 🔥")
    output.append(f"Source Section: {short.source_section}")
    output.append(f"\nDescription: {short.description}")
    output.append(f"\nHook: {short.hook}")
    output.append(f"\nContent Preview: {short.content}")
    
    return '\n'.join(output)

def main():
    """Example usage"""
    extractor = ShortsExtractor()
    
    print("🎬 YouTube Shorts Extractor")
    print("="*60)
    print("\nPaste your video outline (type 'END' on a new line when done):")
    
    outline_lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        outline_lines.append(line)
    
    outline = '\n'.join(outline_lines)
    
    if outline.strip():
        print("\n🔍 Analyzing outline for short opportunities...")
        shorts = extractor.extract_shorts(outline)
        
        if shorts:
            print(f"\n✨ Found {len(shorts)} potential shorts:")
            
            for i, short in enumerate(shorts, 1):
                print(f"\n{'🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f'{i}.'}")
                print(format_short_concept(short))
                
                # Optionally generate script for top short
                if i == 1:
                    print("\n📝 SUGGESTED SCRIPT:")
                    print("-"*40)
                    print(extractor.generate_short_scripts(short))
        else:
            print("\nNo clear short opportunities found. Consider adding:")
            print("- Strong hooks or surprising reveals")
            print("- Quick tips or hacks")
            print("- Compelling mini-stories")
            print("- Before/after comparisons")

if __name__ == "__main__":
    main()
