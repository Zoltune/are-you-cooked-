# im so bored rn
from dataclasses import dataclass
from enum import Enum
import random
import json
from pathlib import Path
from statistics import mean
import time
import sys

DATA_FILE = Path("cooked_history.json")

class CookedLevel(Enum):
    RAW = "Not Cooked"
    WARM = "Slightly Toasted"
    COOKED = "Cooked"
    BURNT = "DEEP FRIED"

@dataclass
class LifeStats:
    sleep_hours: float        # average per night
    assignments_missing: int
    money: float              # dollars
    stress: int               # 1–10
    motivation: int           # 1–10
    social_life: int          # 1–10

@dataclass
class Result:
    score: float
    level: CookedLevel
    chaos_factor: float
    sleep_category: str

class CookedCalculator:
    def __init__(self):
        self.history = self._load_history()

    def _load_history(self):
        if DATA_FILE.exists():
            return json.loads(DATA_FILE.read_text())
        return []

    def _save_result(self, result: Result):
        self.history.append({
            "score": result.score,
            "level": result.level.value,
            "chaos": result.chaos_factor,
            "sleep_category": result.sleep_category
        })
        DATA_FILE.write_text(json.dumps(self.history, indent=2))

    def _sleep_category(self, hours: float) -> str:
        if hours < 5:
            return "Short"
        elif hours <= 8:
            return "Medium"
        else:
            return "Long"

    def calculate(self, stats: LifeStats) -> Result:
        print("\nAnalyzing life stats...")
        time.sleep(7.5)  

        score = 0
        sleep_cat = self._sleep_category(stats.sleep_hours)

        # weighted scoring based on sleep category
        if sleep_cat == "Short":
            score += max(0, 8 - stats.sleep_hours) * 8
        elif sleep_cat == "Medium":
            score += max(0, 8 - stats.sleep_hours) * 5
        else:  # long (from line 59)
            score += max(0, 8 - stats.sleep_hours) * 3

        time.sleep(0.3)  
        score += stats.assignments_missing * 7
        score += max(0, 500 - stats.money) / 25
        score += stats.stress * 4
        score -= stats.motivation * 3
        score -= stats.social_life * 2

        chaos = random.uniform(-10, 15)
        score += chaos

        level = self._get_level(score)
        result = Result(score=round(score, 2), level=level, chaos_factor=round(chaos, 2), sleep_category=sleep_cat)
        self._save_result(result)
        return result

    def _get_level(self, score: float) -> CookedLevel:
        if score < 15:
            return CookedLevel.RAW
        elif score < 30:
            return CookedLevel.WARM
        elif score < 50:
            return CookedLevel.COOKED
        else:
            return CookedLevel.BURNT

    def stats_summary(self):
        if not self.history:
            return "No past data. First run detected."
        avg = mean(r["score"] for r in self.history)
        worst = max(self.history, key=lambda r: r["score"])
        return {
            "runs": len(self.history),
            "average_cooked_score": round(avg, 2),
            "worst_run": worst
        } # i dont really think this is neccesary but im keeping it just in case

def main():
    print("🔥 AM I COOKED? 🔥\n")
    stats = LifeStats(
        sleep_hours=float(input("Avg sleep hours: ")),
        assignments_missing=int(input("Missing assignments: ")),
        money=float(input("Money ($): ")),
        stress=int(input("Stress (1–10): ")),
        motivation=int(input("Motivation (1–10): ")),
        social_life=int(input("Social life (1–10): "))
    )

    calc = CookedCalculator()
    result = calc.calculate(stats)

    print("\n===== RESULTS =====")
    # print("Generating summary...") # commented out bc i dont really need it rn
    time.sleep(2.5)
    print(f"\nCooked Score: {result.score}") 
    time.sleep(2.5)
    print(f"Chaos Factor: {result.chaos_factor}")
    time.sleep(2.5)
    print(f"Sleep Category: {result.sleep_category}")
    time.sleep(2.5)
    print(f"Status: {result.level.value}")
    time.sleep(2.5)
    if result.level == CookedLevel.RAW:
        print("\nyou're chill lil bro")
        time.sleep(900)
    if stats.sleep_hours < 5:
        print("\nfix your sleep schedule bro 💔🥀")
        time.sleep(2.5)
    if stats.assignments_missing >= 10:
        print(f"\n{stats.assignments_missing} MISSING ASSINGMENTS??? DO YOU HAVE SENIORITIS??? 😭")
        time.sleep(2.5)
    if result.level == CookedLevel.WARM:
        print("\nyou're alright, just fix a thing or two and then you're chill")
        time.sleep(900)
    if result.level == CookedLevel.COOKED:
        print("\nok real talk you gotta get your life together")
        time.sleep(900)
    if result.level == CookedLevel.BURNT:
        print("\nyour soul is being eaten...")
        time.sleep(900) # i just don't want "the ps c username stuff" to be RIGHT UNDER the finally print when the script is being ran ok shut up

if __name__ == "__main__":
    main()

# ewaeaseasgdasjkhghjajhsghjgajhdgsahjgdshjagdshjagsjahgsjhagaslkglksahgjksah

# i just scrolling through this file and i discovered that you can compare coding langauges to guitar riffs in rock/metal songs lmao