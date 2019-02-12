use fivekmrun;
SELECT Results.Time, Runner.Name, Results.Position, Results.Age, Race.Name, Race.Date
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
INNER JOIN Runner ON Runner.RunnerId = Results.RunnerId
WHERE True
-- AND Results.RunnerId = 14
AND Race.Date LIKE "%-04-%"
AND Race.DomParkId = 1
ORDER BY Results.TimeInSeconds ASC;