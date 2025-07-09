from database.DB_connect import DBConnect
from model.circuit import Circuit
from model.driverScore import DriverScore


class DAO():
    @staticmethod
    def getAllCircuits():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAnni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select `year` 
                    from races r 
                    group by `year` 
                    order by `year` desc """
        cursor.execute(query)
        for row in cursor:
            result.append(row["year"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllCircuits():
        '''I nodi sono costituiti da tutti i circuiti su cui è
        mai stato disputato un gran premio di F1
        indipendentemente dagli anni selezionati. Per
        ogni circuito, si salvi all’interno del nodo: i) le
        proprietà del circuito (colonne della tabella
        circuits); ii) i risultati dei gran premi tenuti in tale circuito negli anni selezionati (estremi inclusi).
        Per questa seconda richiesta, si suggerisce di utilizzare un ulteriore campo nella definizione della dataclass
        Circuito, che contiene un dizionario le cui chiavi sono gli anni in cui il circuito ha effettivamente ospitato la
        Formula1 (nel range selezionato) e come valori una lista contenente i piazzamenti dei vari piloti nella gara
        considerata (anno, circuito), ottenuti dalla tabella results (campi driverId e position). Tali piazzamenti
        possono essere comodamente rappresentati come una lista di tuple oppure (preferibilmente) come una lista
        di oggetti appositamente definiti per rappresentare l’id del pilota e la sua posizione nella gara. N.B. Si
        consiglia di approcciare questo punto con una soluzione in due step: una query per i circuiti, e
        successivamente una query (per nodo) per ottenere i dettagli dei piazzamenti.'''
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT circuitId, circuitRef, name, location, country, lat, lng 
                    from circuits"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Circuit(row['circuitId'],
                               row['circuitRef'],
                               row['name'],
                               row['location'],
                               row['country'],
                               row['lat'],
                               row['lng'], {}))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getResultsCircuitYear(circuitID, year):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select rID.raceId, rID.year, rID.circuitId, rID.name, rID.date, res.driverId, res.position, res.points 
                       from (select *
                       from races r 
                       where r.year= %s
                       and r.circuitId = %s) rID, results res
                       where rID.raceId = res.raceId """

        cursor.execute(query, (year, circuitID))

        res = []
        for row in cursor:
            res.append(DriverScore(row["driverId"], row["position"], row["points"]))

        cursor.close()
        cnx.close()
        return res