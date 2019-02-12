use fivekmrun;
SELECT Results.RunnerId, Results.Name, SUM(Results.Points) as TotalPoints, Results.Sex
FROM Results 
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE True
AND Race.RaceDate > "2017-01"
AND Race.RaceDate < "2018-0"
AND Results.Sex = 'Мъж'
-- AND Runner
GROUP BY Results.RunnerId,Results.Name,Results.Sex
ORDER BY TotalPoints DESC
-- Name LIKE "%Методи Геор%" ;