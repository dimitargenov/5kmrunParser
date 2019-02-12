use fivekmrun;
SELECT Race.Name, Results.Time,
(SELECT COUNT(*) 
	FROM Results r 
    WHERE r.RunnerId = 14	
    GROUP BY r.RunnerId) AS TotalCount,
(SELECT COUNT(*)
	FROM Results r 
    WHERE r.RunnerId = 14
	AND r.Position = 1
    GROUP BY r.RunnerId) AS FirstCount,
(SELECT COUNT(*)
	FROM Results r 
    WHERE r.RunnerId = 14
	AND r.Position = 2
    GROUP BY r.RunnerId) AS SecondCount,
(SELECT COUNT(*)
	FROM Results r 
    WHERE r.RunnerId = 14
	AND r.Position = 3
    GROUP BY r.RunnerId) AS ThirdCount,
(SELECT COUNT(*)
	FROM Results r 
    WHERE r.RunnerId = 14
	AND r.Position IN (1,2,3,4,5)
    GROUP BY r.RunnerId) AS TopFiveCount    
FROM Results
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE RunnerId = 14
ORDER BY Time ASC;