import sys
import subprocess
import re

def extract_numbers(text):
    """ดึงตัวเลขทั้งหมดออกจาก Output ของนักเรียน"""
    return [float(n) if '.' in n else int(n) for n in re.findall(r"[-+]?\d*\.\d+|\d+", text)]

def run_test(file_path, input_data):
    """สั่งรันไฟล์ Python ของนักเรียนพร้อมป้อนค่า Input"""
    try:
        proc = subprocess.run(
            [sys.executable, file_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3
        )
        return proc.stdout, proc.stderr
    except Exception as e:
        return "", str(e)

# ชุด Test Cases สำหรับข้อสอบ Examination_1.py ถึง Examination_5.py
TEST_CASES = {
    "Examination_1.py": [
        {"input": "100\n10\n", "expected": 800}, # 100 * 10 - ส่วนลด 20% = 800
        {"input": "100\n6\n", "expected": 540},  # 100 * 6 - ส่วนลด 10% = 540
        {"input": "100\n3\n", "expected": 300}   # 100 * 3 = 300 (ไม่มีส่วนลด)
    ],
    "Examination_2.py": [
        {"input": "85\n", "expected": 4},
        {"input": "65\n", "expected": 2},
        {"input": "45\n", "expected": 0}
    ],
    "Examination_3.py": [
        {"input": "15\n42\n8\n", "expected": 42},
        {"input": "100\n50\n75\n", "expected": 100},
        {"input": "-5\n-1\n-10\n", "expected": -1}
    ],
    "Examination_4.py": [
        {"input": "30\n", "expected": 90},  # 30 * 3 = 90
        {"input": "70\n", "expected": 250} # (50 * 3) + (20 * 5) = 250
    ],
    "Examination_5.py": [
        {"input": "5\n3\n", "expected": 1},   # Quadrant 1: (+, +)
        {"input": "-4\n2\n", "expected": 2},  # Quadrant 2: (-, +)
        {"input": "-3\n-7\n", "expected": 3}, # Quadrant 3: (-, -)
        {"input": "6\n-1\n", "expected": 4}   # Quadrant 4: (+, -)
    ]
}

def grade_problem(file_name, cases):
    total_score = 0.0
    max_score = 2.0
    score_per_case = max_score / len(cases)
    
    for case in cases:
        out, err = run_test(file_name, case["input"])
        nums = extract_numbers(out)
        expected = case["expected"]
        
        # ตรวจเช็กว่ามีตัวเลขคำตอบที่ถูกต้องอยู่ใน Output หรือไม่
        if expected in nums or any(abs(n - expected) < 0.01 for n in nums):
            total_score += score_per_case
            
    return round(total_score, 2)

if __name__ == "__main__":
    print("==========================================")
    print("        สรุปผลการตรวจคะแนนข้อสอบ          ")
    print("==========================================")
    
    total = 0.0
    for i in range(1, 6):
        file_name = f"Examination_{i}.py"
        score = grade_problem(file_name, TEST_CASES[file_name])
        print(f"ข้อที่ {i} ({file_name}): {score:.2f} / 2.00 คะแนน")
        total += score
        
    print("------------------------------------------")
    print(f"คะแนนรวมทั้งหมด: {total:.2f} / 10.00 คะแนน")
    print("==========================================")
