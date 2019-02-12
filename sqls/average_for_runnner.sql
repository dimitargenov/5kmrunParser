use fivekmrun;
SELECT sec_to_time(avg(Results.TimeInSeconds))
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True
AND Results.RunnerId = 14
-- AND (Race.Date LIKE "2015-01%" OR Race.Date LIKE "2015-02%")
-- AND Race.RaceDate LIKE "%-12-%"
ORDER BY Results.Time ASC;