use fivekmrun;
SELECT sec_to_time(MIN(Results.TimeInSeconds)) AS PB, 
Results.Name AS RunnerName, 
-- Results.Position, 
-- Results.Age, 
Results.RunnerId
-- ,Race.Name, Race.RaceDate
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True
-- by dom park --
-- AND Race.DomParkId = 8
-- by age --
-- AND Results.Age LIKE "%30-34%" 
-- by year
AND Race.Date LIKE "%2019%"
GROUP BY Results.RunnerId, RunnerName
ORDER BY MIN(Results.TimeInSeconds) ASC
LIMIT 100;