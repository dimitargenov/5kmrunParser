use fivekmrun;
SELECT -- avg(Results.TimeInSeconds) AS AvgTime,
COUNT(Results.TimeInSeconds) AS Count 
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True
-- AND Race.Date LIKE "%2014-%"
AND Results.Position = 2
-- AND Race.DomParkId = 8
AND Results.RunnerId = 14;