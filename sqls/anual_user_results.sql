use fivekmrun;
SELECT Results.Time, Results.Position
-- sec_to_time(avg(Results.TimeInSeconds)) AS AvgTime
-- max(Results.Time) AS SlowTime, min(Results.Time) AS FastTime
-- count(*) AS NumberOfRaces
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True 
AND Results.RunnerId = 1611
-- AND Results.Position = 2 
AND Race.Date LIKE "2018-%"
AND Race.DomParkId = 1
AND Results.Time < "18"
-- AND Results.RunnerId = 5574;
ORDER BY Time ASC