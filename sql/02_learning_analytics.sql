-- Execute in SQLite after audit-cleaning student_attempts with Python.
-- 'correct' is correctness of the first response, before help is requested.
-- bottom_hint=1 means the student reached the final hint; not necessarily an explicit answer.
CREATE VIEW ordered AS
SELECT *,
 ROW_NUMBER() OVER(PARTITION BY user_id,skill_id ORDER BY opportunity,order_id) AS rn,
 LAG(correct,1) OVER(PARTITION BY user_id,skill_id ORDER BY opportunity,order_id) AS prev1,
 LAG(correct,2) OVER(PARTITION BY user_id,skill_id ORDER BY opportunity,order_id) AS prev2,
 LEAD(correct,1) OVER(PARTITION BY user_id,skill_id ORDER BY opportunity,order_id) AS next_correct,
 LEAD(opportunity,1) OVER(PARTITION BY user_id,skill_id ORDER BY opportunity,order_id) AS next_opportunity,
 CASE WHEN bottom_hint = 1 THEN 'Bottom Hint'
      WHEN hint_count = 0 THEN 'No Hints'
      WHEN hint_count > 0 AND bottom_hint = 0 THEN 'Guided Hints'
      ELSE 'Unknown' END AS help_group
FROM student_attempts;

CREATE VIEW help_groups AS
SELECT help_group, COUNT(*) AS interactions, COUNT(DISTINCT user_id) AS students
FROM ordered WHERE help_group != 'Unknown' GROUP BY help_group;

CREATE VIEW next_opportunity_accuracy AS
SELECT help_group,
 COUNT(*) AS eligible_transitions,
 ROUND(100.0 * AVG(next_correct),2) AS next_accuracy_pct
FROM ordered
WHERE help_group != 'Unknown'
AND next_correct IN (0,1) AND next_opportunity > opportunity
GROUP BY help_group;

-- 'Mastery' = earliest observed third consecutive correct initial responses.
-- The denominator includes student-skill pairs that never reach this proxy threshold.
-- Group assignment = help category on first observed eligible opportunity of pair.
CREATE VIEW mastery_comparison AS
WITH first_group AS (
 SELECT user_id,skill_id,help_group
 FROM ordered WHERE rn=1 AND help_group!='Unknown'
), first_observed AS (
 SELECT user_id,skill_id,MIN(opportunity) AS first_opportunity
 FROM ordered GROUP BY user_id,skill_id
), milestones AS (
 SELECT user_id,skill_id,MIN(opportunity) AS mastery_opportunity
 FROM ordered
 WHERE correct=1 AND prev1=1 AND prev2=1
 GROUP BY user_id,skill_id
)
SELECT f.help_group,
 COUNT(*) AS student_skill_pairs,
 COUNT(m.mastery_opportunity) AS mastered_pairs,
 ROUND(100.0*COUNT(m.mastery_opportunity)/COUNT(*),2) AS mastery_rate_pct,
 ROUND(AVG(m.mastery_opportunity - o.first_opportunity + 1),2) AS avg_observed_opportunities_to_mastery_among_mastered,
 ROUND(AVG(m.mastery_opportunity),2) AS avg_absolute_mastery_opportunity
FROM first_group f
JOIN first_observed o ON f.user_id=o.user_id AND f.skill_id=o.skill_id
LEFT JOIN milestones m ON f.user_id=m.user_id AND f.skill_id=m.skill_id
GROUP BY f.help_group;
