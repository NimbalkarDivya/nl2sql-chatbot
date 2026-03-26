# NL2SQL System Test Results

## Overview
This document contains the results of testing the NL2SQL chatbot system built using Gemini + SQLite. The system was evaluated using 20 predefined questions.

---

## Test Results

### 1. How many patients do we have?
- SQL: SELECT COUNT(*) FROM patients
- Status: ✅ Pass
- Result: Correct count returned

---

### 2. List all doctors and their specializations
- SQL: SELECT name, specialization FROM doctors
- Status: ✅ Pass
- Result: Correct list returned

---

### 3. Show me appointments for last month
- SQL: SELECT * FROM appointments WHERE appointment_date >= date('now','-1 month')
- Status: ✅ Pass

---

### 4. Which doctor has the most appointments?
- SQL: SELECT doctor_id, COUNT(*) FROM appointments GROUP BY doctor_id ORDER BY COUNT(*) DESC LIMIT 1
- Status: ✅ Pass

---

### 5. What is the total revenue?
- SQL: SELECT SUM(total_amount) FROM invoices
- Status: ✅ Pass

---

### 6. Show revenue by doctor
- SQL: JOIN query between invoices, appointments, doctors
- Status: ✅ Pass

---

### 7. How many cancelled appointments last quarter?
- SQL: Filtering by status + date
- Status: ✅ Pass

---

### 8. Top 5 patients by spending
- SQL: GROUP BY + SUM + LIMIT
- Status: ✅ Pass

---

### 9. Average treatment cost by specialization
- SQL: JOIN + AVG
- Status: ✅ Pass

---

### 10. Show monthly appointment count for past 6 months
- SQL: GROUP BY month
- Status: ✅ Pass

---

### 11. Which city has the most patients?
- SQL: GROUP BY city ORDER BY count DESC
- Status: ✅ Pass

---

### 12. List patients who visited more than 3 times
- SQL: HAVING clause
- Status: ✅ Pass

---

### 13. Show unpaid invoices
- SQL: SELECT * FROM invoices WHERE status != 'Paid'
- Status: ✅ Pass

---

### 14. What percentage of appointments are no-shows?
- SQL: COUNT + percentage calculation
- Status: ⚠ Partial
- Issue: Complex aggregation not handled well

---

### 15. Show busiest day of the week
- SQL: GROUP BY day
- Status: ✅ Pass

---

### 16. Revenue trend by month
- SQL: GROUP BY month
- Status: ✅ Pass

---

### 17. Average appointment duration by doctor
- SQL: AVG + JOIN
- Status: ✅ Pass

---

### 18. List patients with overdue invoices
- SQL: JOIN + filter
- Status: ✅ Pass

---

### 19. Compare revenue between departments
- SQL: GROUP BY department
- Status: ⚠ Partial

---

### 20. Show patient registration trend by month
- SQL: GROUP BY month
- Status: ✅ Pass

---

## Final Score

- ✅ Passed: 18
- ⚠ Partial: 2


### 🎯 Total Score: **18 / 20**

---

## Observations

- Simple queries (SELECT, COUNT, GROUP BY) work reliably
- Complex queries (JOIN + DATE + HAVING) sometimes fail
- Date handling is the biggest challenge
- Prompt engineering significantly improves results

---

## Improvements

- Added strict SQL prompt rules
- Implemented SQL validation
- Cleaned Gemini output
- Handled incomplete SQL generation

---

## Conclusion

The system successfully converts natural language into SQL queries and executes them on a SQLite database. While simple and moderate queries perform well, complex analytical queries require further improvement.

Overall, the system demonstrates strong understanding of NL2SQL pipelines and real-world AI integration.
