from backend.scripts.llm.tactical_insight_engine import TacticalInsightEngine

engine=TacticalInsightEngine()

context=f"""
Store 3 experienced increasing sales over the past 4 weeks.
Temperature increased and unemployment decreased.
Holiday season approaching.
"""

response=engine.generate_insight(context)

print("\nTactical Insigth:\n")
print(response)
