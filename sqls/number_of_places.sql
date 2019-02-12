use fivekmrun;
SELECT Runner.Name, rr.secPlaces
FROM (
SELECT Runner.Id, COUNT(*) As secPlaces 
FROM Runner
Inner JOIN Results ON Results.RunnerId = Runner.RunnerId
INNER JOIN Race ON Race.Id = Results.RaceId
WHERE true
-- AND Race.DomParkId = 1
-- AND Race.RaceDate > "2013"
-- AND Race.RaceDate < "2014"
And Results.Position IN (2)
GROUP BY Runner.Id
) as rr
INNER JOIN Runner ON Runner.Id = rr.Id
ORDER BY rr.secPlaces DESC;