import csv
import time

def load_module_names(file_path="cs modules.csv"):
    """Load module codes, names, and credits from CSV file"""
    module_info = {}
    try:
        with open(file_path, 'r') as f:
            for row in csv.reader(f):
                if not row:
                    continue
                # Extract module code, name, and credits
                code = row[0].strip()
                name = row[1].strip() if len(row) > 1 else code
                credits = int(code.split('-')[1])
                module_info[code] = (name, credits)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
    return module_info

def calculate_weighted_average(data, max_credits=None, default_total_credits=None):
    """Calculate weighted average based on credits and marks"""
    # Filter modules with passing marks (>=40)
    modules = []
    for code, mark in data.items():
        if mark >= 40:
            credits = module_names[code][1]
            modules.append((credits, mark))

    weighted_sum = 0
    total_credits = 0

    # If max_credits specified, use best marks up to that limit
    if max_credits is not None:
        modules.sort(key=lambda x: x[1], reverse=True)
        for credits, mark in modules:
            take = min(credits, max_credits - total_credits)
            weighted_sum += take * mark
            total_credits += take
            if total_credits == max_credits:
                break
        divisor = total_credits

    # If default total specified, use all modules with that total
    elif default_total_credits is not None:
        for credits, mark in modules:
            weighted_sum += credits * mark
            total_credits += credits
        divisor = default_total_credits

    return weighted_sum / divisor if divisor else 0

def Y1_calculate_degrees(data):
    """Check Year 1 pass/fail status"""
    # Find all failed modules (mark < 40)
    failed = [module_names[code][0] for code, mark in data.items() if mark < 40]
    return ("fail" if failed else "pass", failed)

def Y2_calculate_degrees(data):
    """Calculate Year 2 average (best 100 credits)"""
    failed = [module_names[code][0] for code, mark in data.items() if mark < 40]
    return calculate_weighted_average(data, max_credits=100), failed

def Y3_calculate_degrees(data):
    """Calculate Year 3 average (all 120 credits)"""
    failed = [module_names[code][0] for code, mark in data.items() if mark < 40]
    return calculate_weighted_average(data, default_total_credits=120), failed

def final_grade(y2, y3):
    """Calculate final grade: 25% Year 2 + 75% Year 3"""
    return (y3 * 3 + y2) / 4

def Classification_lookup(overall):
    """Determine degree classification based on overall mark"""
    if overall >= 70:
        return "First Class"
    elif overall >= 60:
        return "Second Class (Upper Division) (2.1)"
    elif overall >= 50:
        return "Second Class (Lower Division) (2.2)"
    elif overall >= 40:
        return "Third Class"
    else:
        return "Fail"

def read_marks_csv(file_path):
    """Read student marks from CSV and generate reports"""
    reports = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue

            student_id = row[0]

            # Helper function to extract module code and mark pairs
            def get_dict(start, end):
                d = {}
                for i in range(start, end, 2):
                    if i+1 < len(row):
                        d[row[i]] = int(row[i+1])
                return d

            # --- Auto-detect year boundaries ---
            total_pairs = (len(row) - 1) // 2
            if total_pairs == 17:  
                y1_start, y1_end, y2_end, y3_end = 1, 11, 23, 35
            else:
                per_year = total_pairs // 3
                y1_start, y1_end = 1, 1 + per_year*2
                y2_end = 1 + per_year*4
                y3_end = 1 + per_year*6

            # Extract data for each year using detected boundaries
            y1_data = get_dict(y1_start, y1_end)
            y2_data = get_dict(y1_end, y2_end)
            y3_data = get_dict(y2_end, y3_end)

            # Calculate averages and check for failures
            y1_status, failed_y1 = Y1_calculate_degrees(y1_data)
            y2_avg, failed_y2 = Y2_calculate_degrees(y2_data)
            y3_avg, failed_y3 = Y3_calculate_degrees(y3_data)

            # Calculate final grade
            final = final_grade(y2_avg, y3_avg)

            # Determine classification (fail if any year has failures)
            if y1_status == "fail" or failed_y2 or failed_y3:
                class_result = "Fail"
            else:
                class_result = Classification_lookup(final)

            # Build formatted report string
            report = f"Student ID: {student_id}\nModules:\n"

            # Combine all modules for display
            all_module_data = {**y1_data, **y2_data, **y3_data}
            for code, mark in all_module_data.items():
                name = module_names.get(code, (code, 0))[0]
                report += f"  - {code} ({name}): {mark}%\n"

            # Add summary statistics
            report += f"\nLevel 5 Average: {y2_avg:.2f}%"
            report += f"\nLevel 6 Average: {y3_avg:.2f}%"
            report += f"\nFinal Aggregate: {final:.2f}%"
            report += f"\nClassification: {class_result}\n"
            report += "-" * 30

            reports.append([report])
    return reports


# --- MAIN EXECUTION ---
start = time.time()

# Load module information
module_names = load_module_names("cs modules.csv")

# Process student marks
formatted_reports = read_marks_csv("activity1_1_marks.csv")

# Write reports to output file
with open('students_mark.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(formatted_reports)

end = time.time()
print("Execution time:", end - start, "seconds")