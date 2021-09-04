use fivekmrun;
SELECT Results.RunnerId,
COUNT(*) as total,
SEC_TO_TIME(AVG(TimeInSeconds)) AS avgTime,
MIN(Time) as bestTime
FROM Results
Inner Join Race On Race.Id = Results.RaceId 
WHERE Results.RunnerId = 1611
AND Race.DomParkId = 1
AND Race.Date LIKE "2018-%"
AND Results.Time < "18:00"
GROUP BY Results.RunnerId