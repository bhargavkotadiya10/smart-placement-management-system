USE smart_placement_db;

INSERT INTO companies (name, location, website, description) VALUES
('Annex Infotechnologies', 'Ahmedabad', NULL, 'Software and technology company'),
('RyDOT Infotech', 'Ahmedabad', 'https://rydotinfotech.com/', 'Digital transformation and software solutions company'),
('TechNova Solutions', 'Ahmedabad', 'https://example.com/', 'Technology solutions and application development company')
ON DUPLICATE KEY UPDATE name = VALUES(name);

INSERT INTO jobs
(company_id, title, location, internship_duration, stipend, salary, description, skills, min_percentage, openings)
SELECT id, 'Associate Software Engineer', 'Ahmedabad', '3-6 months', '₹8,000/month', '₹3.5-6+ LPA',
       'Entry-level software engineering role focused on programming, SQL, APIs, problem solving and software development.',
       'Python, SQL, OOP, REST API, Git, DSA', 55.00, 5
FROM companies WHERE name = 'Annex Infotechnologies'
AND NOT EXISTS (SELECT 1 FROM jobs WHERE title = 'Associate Software Engineer' AND company_id = companies.id);

INSERT INTO jobs
(company_id, title, location, internship_duration, stipend, salary, description, skills, min_percentage, openings)
SELECT id, 'QA Automation Intern', 'Ahmedabad', '6 months', '₹8,000/month', '₹2.16-3 LPA',
       'QA automation internship focused on UI/API testing, Playwright, JavaScript or TypeScript, Git and quality practices.',
       'Playwright, JavaScript, TypeScript, API Testing, Git, Testing', 55.00, 3
FROM companies WHERE name = 'RyDOT Infotech'
AND NOT EXISTS (SELECT 1 FROM jobs WHERE title = 'QA Automation Intern' AND company_id = companies.id);

INSERT INTO jobs
(company_id, title, location, internship_duration, stipend, salary, description, skills, min_percentage, openings)
SELECT id, 'Backend Developer Intern', 'Ahmedabad', '6 months', '₹7,000/month', '₹3-4 LPA',
       'Backend development internship focused on Python, REST APIs, SQL and application development.',
       'Python, FastAPI, REST API, SQL, Git', 55.00, 2
FROM companies WHERE name = 'TechNova Solutions'
AND NOT EXISTS (SELECT 1 FROM jobs WHERE title = 'Backend Developer Intern' AND company_id = companies.id);
