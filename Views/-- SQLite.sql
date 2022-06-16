-- SQLite
SELECT strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) ) as mes
FROM Datas_espetaculo

ALTER TABLE Datas_espetaculo ADD COLUMN datas TEXT

UPDATE Datas_espetaculo SET datas = CAST(data as text)

ALTER TABLE Datas_espetaculo DROP COLUMN data
ALTER TABLE Datas_espetaculo RENAME COLUMN datas to data


SELECT id FROM Datas_espetaculo WHERE strftime('%Y', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  = '2021' AND strftime('%m', (substr(data,7,4) || '-' || substr(data,4,2) || '-' || substr(data,1,2)) )  = '07'

DELETE FROM Reservas WHERE id = '18'

SELECT de.data, uel.lugar, uel.reserva 
FROM User_espetaculo_lugar uel 
INNER JOIN Datas_espetaculo de ON uel.data_espetaculo = de.id 
INNER JOIN Lugares l ON uel.lugar = l.id 
WHERE uel.user='q' AND espetaculo='Filme2' 
ORDER BY l.fila, l.coluna

SELECT data_espetaculo.data WHERE reserva ='{reserva}' AND 

SELECT * FROM User_espetaculo_lugar WHERE data_espetaculo = 8

DELETE FROM User_espetaculo_lugar

ALTER TABLE Users ADD COLUMN blocked TEXT
SELECT blocked FROM Users
UPDATE Users SET blocked = NULL WHERE username='t'
SELECT username FROM Users WHERE blocked is NULL
SELECT username FROM Users WHERE role='User' AND blocked is NULL