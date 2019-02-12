use fivekmrun;
SELECT Runner.Sex, Runner.Name,
COUNT(Runner.Id) AS wins
-- Results.Name, Results.SexPosition, 
FROM Runner
INNER JOIN Results ON Runner.Id = Results.RunnerId
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE Results.SexPosition = 1
AND Runner.Sex = 2
GROUP BY Runner.Id
ORDER BY wins DESC
-- ORDER BY TimeInSeconds ASC
LIMIT 100;