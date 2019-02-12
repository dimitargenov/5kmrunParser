use managementevents_alpha_local;
SELECT
COUNT(*) as statusClassCount, 
Prospect.StatusClass as statusClass, 
COUNT(CASE WHEN Prospect.Status = 0 THEN 1 else NULL end) as notParticipatingCount
FROM Prospect
INNER JOIN MasterContact ON(MasterContact.Id = Prospect.MasterContactId)
LEFT JOIN EventParticipant ON(EventParticipant.MasterContactId = Prospect.MasterContactId AND Prospect.EventId = EventParticipant.EventId)
WHERE Prospect.EventId = 2518 
AND MasterContact.Status != -3
-- AND Prospect.StatusClass IS NOT NULL 
-- AND Prospect.StatusClass != "" 
GROUP BY Prospect.StatusClass 
ORDER BY Prospect.StatusClass