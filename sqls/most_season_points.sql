use fivekmrun;
SELECT t.RunnerId, Runner.Name, t.points
FROM (
SELECT Results.RunnerId as RunnerId, SUM(Points) as points
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True -- RunnerId = 14
AND Race.Date LIKE "2015-%"
GROUP BY Results.RunnerId
) as t
INNER JOIN Runner ON Runner.RunnerId = t.RunnerId
-- INNER JOIN DomPark ON DomPark.Id = Runner.DomParkId
ORDER BY t.points DESC