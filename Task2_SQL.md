# SQL Task 2

## Given tables:
- tasks (id, name, status, project_id)
- projects (id, name)

# 1. get all statuses, not repeating, alphabetically ordered

SELECT DISTINCT status 
FROM tasks 
ORDER BY status ASC;


# 2. get the count of all tasks in each project, order by tasks count descending

SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY task_count DESC;


# 3. get the count of all tasks in each project, order by projects names

SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
GROUP BY p.id, p.name
ORDER BY p.name ASC;


# 4. get the tasks for all projects having the name beginning with "N" letter

SELECT t.*
FROM tasks t
JOIN projects p ON t.project_id = p.id
WHERE p.name LIKE 'N%';


# 5. get the list of all projects containing the 'a' letter in the middle of the name, and show the tasks count near each project. Mention that there can exist projects without tasks and tasks with project_id= NULL

SELECT p.name, COUNT(t.id) as task_count
FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id
WHERE p.name LIKE '_%a%_'
GROUP BY p.id, p.name
ORDER BY p.name ASC;


# 6. get the list of tasks with duplicate names. Order alphabetically

SELECT id, name, status, project_id
FROM tasks
WHERE name IN (
    SELECT name
    FROM tasks
    GROUP BY name
    HAVING COUNT(*) > 1
)
ORDER BY name ASC, id ASC;


# 7. get the list of tasks having several exact matches of both name and status, from the project 'Delivery'. Order by matches count

WITH TaskMatches AS (
    SELECT
        t.id,
        t.name,
        t.status,
        t.project_id,
        COUNT(*) OVER(PARTITION BY t.name, t.status) as matches_count
    FROM tasks t
    JOIN projects p ON t.project_id = p.id
    WHERE p.name = 'Delivery'
)
SELECT id, name, status, project_id, matches_count
FROM TaskMatches
WHERE matches_count > 1
ORDER BY matches_count DESC, name ASC, status ASC;


# 8. get the list of project names having more than 10 tasks in status 'completed'. Order by project_id

SELECT p.name
FROM projects p
JOIN tasks t ON p.id = t.project_id
WHERE t.status = 'completed'
GROUP BY p.id, p.name
HAVING COUNT(t.id) > 10
ORDER BY p.id ASC;
