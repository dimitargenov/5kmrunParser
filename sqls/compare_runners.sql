use fivekmrun;
SELECT Race.Name AS RaceName, Res1.Position AS Pos1, Res1.Name AS Runner1, Res1.Time AS Time1,
Res2.Position AS Pos2, Res2.Name AS Runner2, Res2.Time AS Time2 
FROM Race 
INNER JOIN Results AS Res2 ON Race.Id = Res2.RaceId
INNER JOIN Results AS Res1 ON Race.Id = Res1.RaceId
WHERE Res1.RaceId = Res2.RaceId
AND Res1.Position > Res2.Position
AND Res1.RunnerId = 14
AND Res2.RunnerId = 5574
AND Race.Date LIKE "%2018-"
ORDER BY Race.Date DESC