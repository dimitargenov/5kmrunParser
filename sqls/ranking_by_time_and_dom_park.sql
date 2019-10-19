use fivekmrun;
SET @row_number = 0;
SELECT a.RunnerId, b.BestTime, a.Name -- , b.RaceName, b.Best 
FROM Results a
INNER JOIN 
(
	SELECT 
    MIN(TimeInSeconds) AS Best, MIN(Time) AS BestTime,
		Results.RunnerId, Time, Results.Position, Runner.Name, Race.Name AS RaceName
    FROM Results
    INNER JOIN Race ON Race.Id = Results.RaceId
    INNER JOIN Runner ON Runner.RunnerId = Results.RunnerId
    WHERE true
    AND Race.DomParkId = 11 -- by dom park
    -- AND Results.Sex = "Жена" -- by sex
    -- AND Race.Date LIKE "2019-%"
    -- AND Results.RunnerId = 1611
    -- AND TimeInSeconds < 1020
    -- ORDER BY TimeInSeconds 
    GROUP BY Results.RunnerId
) as b ON a.RunnerId = b.RunnerId
GROUP BY a.RunnerId
ORDER BY b.Best ASC
LIMIT 100
