use fivekmrun;
-- SET @row_number = 0;
SELECT b.BestTime, a.Name, b.RaceName, b.Best 
FROM Results a
INNER JOIN 
(
	SELECT MIN(TimeInSeconds) AS Best, MIN(Time) AS BestTime,
		RunnerId, Time, Results.Id, Race.Name AS RaceName
    FROM Results
    INNER JOIN Race ON Race.Id = Results.RaceId
    WHERE Race.DomParkId = 1 -- by dom park
    AND Results.Sex = "Жена" -- by sex
    GROUP BY RunnerId
    ) as b ON a.RunnerId = b.RunnerId
GROUP BY a.RunnerId
ORDER BY b.best ASC
LIMIT 100