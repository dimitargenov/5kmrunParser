use fivekmrun;
SELECT *
-- r.Age, r.RaceName, r.RaceDate, r.RunnerId
FROM (
SELECT MIN(Time) AS BestTime, Id
FROM Results
WHERE True
-- DomParkId	4 (Lauta) After 06.06.2015 -
-- AND RaceDate > "2015-06-06"
GROUP BY Id
) AS r
INNER JOIN Results ON Results.Id = r.Id
INNER JOIN Race ON Race.Id = Results.RaceId
AND Race.DomParkId = 1
AND Race.RaceDate > "2018-01"
ORDER BY TimeInSeconds ASC
LIMIT 150;