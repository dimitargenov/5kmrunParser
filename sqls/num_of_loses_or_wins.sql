use fivekmrun;
SELECT COUNT(Res2.Name) as winners, Res2.Name
-- Race.Name AS RaceName, Res1.Position AS Pos1, Res1.Name AS Runner1, Res1.Time AS Time1,
-- Res2.Position AS Pos2, Res2.Name AS Runner2, Res2.Time AS Time2 
FROM Race 
INNER JOIN Results AS Res2 ON Race.Id = Res2.RaceId
INNER JOIN Results AS Res1 ON Race.Id = Res1.RaceId
WHERE Res1.RaceId = Res2.RaceId
-- AND Res1.Position > Res2.Position
AND Res1.RunnerId = 14
-- AND Res1.Position IN (1)
AND Res2.Position = Res1.Position - 1 
-- AND Race.Date LIKE "%2018-"
-- ORDER BY Race.Date DESC
GROUP BY Res2.Name
ORDER BY winners DESC