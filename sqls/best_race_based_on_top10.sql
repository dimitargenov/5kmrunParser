use fivekmrun;
SELECT Race.EventId,Race.Name, Results.Position,
avg(Results.TimeInSeconds) AS AvgTopTen,
sec_to_time(avg(Results.TimeInSeconds)) AS AvgTime,
max(Results.Time) AS SlowTime, min(Results.Time) AS FastTime,
Results.RaceId
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE Results.Position < 11
GROUP BY Results.RaceId
ORDER BY AvgTopTen;