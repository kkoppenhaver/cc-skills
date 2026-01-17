#!/usr/bin/env python3
"""
YouTube Hook Analyzer
Evaluates the effectiveness of video hooks
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class HookAnalysis:
    """Analysis results for a video hook"""
    text: str
    score: int
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    hook_type: str
    estimated_retention: str

class HookAnalyzer:
    def __init__(self):
        self.hook_patterns = {
            'question': r'^(what if|have you ever|did you know|can you|why do|is it)',
            'statement': r'^(this is|i just|most people|everyone thinks|nobody talks)',
            'challenge': r'(bet you|99%|impossible|try not to|challenge)',
            'story': r'(years ago|this is the day|i wasn\'t supposed|last week)',
            'shocking': r'(changes everything|completely wrong|biggest mistake|destroyed)',
            'promise': r'(i\'ll show you|you\'ll learn|by the end|in the next)'
        }
        
        self.power_words = [
            'secret', 'shocking', 'insane', 'crazy', 'unbelievable',
            'mind-blowing', 'revolutionary', 'game-changing', 'destroy',
            'exposed', 'truth', 'actually', 'real', 'hidden', 'nobody'
        ]
        
        self.weak_words = [
            'basically', 'sort of', 'kind of', 'maybe', 'possibly',
            'might', 'could', 'somewhat', 'fairly', 'quite'
        ]
    
    def analyze_hook(self, hook_text: str, target_length_seconds: int = 30) -> HookAnalysis:
        """Analyze a hook for effectiveness"""
        
        hook_text = hook_text.strip()
        score = 0
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Detect hook type
        hook_type = self._detect_hook_type(hook_text)
        
        # Length analysis (assuming ~2.5 words per second speaking rate)
        word_count = len(hook_text.split())
        expected_words = target_length_seconds * 2.5
        
        if word_count < expected_words * 0.7:
            weaknesses.append(f"Hook is too short ({word_count} words for {target_length_seconds}s)")
            suggestions.append("Expand with more specific details or examples")
        elif word_count > expected_words * 1.3:
            weaknesses.append(f"Hook is too long ({word_count} words for {target_length_seconds}s)")
            suggestions.append("Trim unnecessary words and get to the point faster")
        else:
            strengths.append(f"Good length ({word_count} words)")
            score += 10
        
        # Check for power words
        power_word_count = sum(1 for word in self.power_words 
                              if word.lower() in hook_text.lower())
        if power_word_count > 0:
            strengths.append(f"Uses {power_word_count} power word(s)")
            score += power_word_count * 5
        else:
            suggestions.append("Add power words for emotional impact")
        
        # Check for weak words
        weak_word_count = sum(1 for word in self.weak_words 
                            if word.lower() in hook_text.lower())
        if weak_word_count > 0:
            weaknesses.append(f"Contains {weak_word_count} weak qualifier(s)")
            suggestions.append("Remove weak qualifiers for stronger statements")
            score -= weak_word_count * 3
        
        # Pattern interrupt check
        if hook_text[0].islower() or hook_text.startswith('...'):
            strengths.append("Uses pattern interrupt opening")
            score += 10
        
        # Promise/value check
        if re.search(self.hook_patterns['promise'], hook_text.lower()):
            strengths.append("Makes clear promise to viewer")
            score += 15
        else:
            suggestions.append("Add a clear promise of what viewer will gain")
        
        # Question engagement
        if '?' in hook_text:
            strengths.append("Uses questions to engage viewer")
            score += 10
        
        # Specificity check
        if re.search(r'\d+', hook_text):
            strengths.append("Includes specific numbers")
            score += 10
        
        # Stakes/consequences check
        stakes_words = ['destroy', 'ruin', 'change everything', 'never be the same', 
                       'biggest mistake', 'costs you', 'loses']
        if any(word in hook_text.lower() for word in stakes_words):
            strengths.append("Establishes clear stakes")
            score += 15
        else:
            suggestions.append("Consider adding stakes or consequences")
        
        # Curiosity gap check
        curiosity_phrases = ['but', 'however', 'except', 'until', 'then something']
        if any(phrase in hook_text.lower() for phrase in curiosity_phrases):
            strengths.append("Creates curiosity gap")
            score += 15
        
        # Personal/relatable check
        if re.search(r'\b(i|my|me|you|your)\b', hook_text.lower()):
            strengths.append("Uses personal/direct language")
            score += 10
        
        # Calculate estimated retention
        if score >= 70:
            estimated_retention = "High (70-90%)"
        elif score >= 50:
            estimated_retention = "Good (60-70%)"
        elif score >= 30:
            estimated_retention = "Average (50-60%)"
        else:
            estimated_retention = "Low (Below 50%)"
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return HookAnalysis(
            text=hook_text,
            score=score,
            strengths=strengths,
            weaknesses=weaknesses,
            suggestions=suggestions,
            hook_type=hook_type,
            estimated_retention=estimated_retention
        )
    
    def _detect_hook_type(self, hook_text: str) -> str:
        """Detect the type of hook being used"""
        
        lower_text = hook_text.lower()
        
        for hook_type, pattern in self.hook_patterns.items():
            if re.search(pattern, lower_text):
                return hook_type.capitalize()
        
        return "General"
    
    def compare_hooks(self, hooks: List[str]) -> List[HookAnalysis]:
        """Compare multiple hook options"""
        
        analyses = []
        for hook in hooks:
            analyses.append(self.analyze_hook(hook))
        
        # Sort by score
        analyses.sort(key=lambda x: x.score, reverse=True)
        
        return analyses
    
    def suggest_improvements(self, hook_text: str) -> str:
        """Generate an improved version of the hook"""
        
        analysis = self.analyze_hook(hook_text)
        improved = hook_text
        
        # Add power word if missing
        if "power word" in " ".join(analysis.suggestions).lower():
            power_word = self.power_words[0]
            improved = f"This {power_word} discovery... {improved}"
        
        # Add promise if missing
        if "promise" in " ".join(analysis.suggestions).lower():
            improved += " ...and by the end, you'll know exactly how to use it."
        
        # Add stakes if missing
        if "stakes" in " ".join(analysis.suggestions).lower():
            improved = improved.replace(".", 
                ", and if you don't know this, it could cost you everything.")
        
        return improved

def format_analysis(analysis: HookAnalysis) -> str:
    """Format analysis results for display"""
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"HOOK: {analysis.text[:50]}...")
    output.append(f"{'='*60}")
    output.append(f"\n📊 Overall Score: {analysis.score}/100")
    output.append(f"🎯 Hook Type: {analysis.hook_type}")
    output.append(f"📈 Estimated Retention: {analysis.estimated_retention}")
    
    if analysis.strengths:
        output.append(f"\n✅ Strengths:")
        for strength in analysis.strengths:
            output.append(f"   • {strength}")
    
    if analysis.weaknesses:
        output.append(f"\n❌ Weaknesses:")
        for weakness in analysis.weaknesses:
            output.append(f"   • {weakness}")
    
    if analysis.suggestions:
        output.append(f"\n💡 Suggestions:")
        for suggestion in analysis.suggestions:
            output.append(f"   • {suggestion}")
    
    return "\n".join(output)

def main():
    """Example usage"""
    analyzer = HookAnalyzer()
    
    print("🎬 YouTube Hook Analyzer")
    print("="*60)
    print("\nEnter your hook (or 'compare' to compare multiple):")
    
    user_input = input("\n> ").strip()
    
    if user_input.lower() == 'compare':
        hooks = []
        print("\nEnter up to 5 hooks (empty line to finish):")
        for i in range(5):
            hook = input(f"Hook {i+1}: ").strip()
            if not hook:
                break
            hooks.append(hook)
        
        if hooks:
            print("\n🔍 Comparing Hooks...")
            analyses = analyzer.compare_hooks(hooks)
            
            for i, analysis in enumerate(analyses, 1):
                print(f"\n{'🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else '📊'} "
                      f"Rank {i}:")
                print(format_analysis(analysis))
    else:
        analysis = analyzer.analyze_hook(user_input)
        print(format_analysis(analysis))
        
        if analysis.score < 70:
            print("\n🔧 Suggested Improvement:")
            improved = analyzer.suggest_improvements(user_input)
            print(f"   {improved}")
            
            # Re-analyze improved version
            improved_analysis = analyzer.analyze_hook(improved)
            print(f"\n   New Score: {improved_analysis.score}/100 "
                  f"(+{improved_analysis.score - analysis.score} points)")

if __name__ == "__main__":
    main()
