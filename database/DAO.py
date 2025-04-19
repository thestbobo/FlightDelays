from database.DB_connect import DBConnect
from model.airport import Airport
from model.connessione import Connessione


class DAO():

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  tmp.ID, tmp.IATA_CODE, count(*) as n
                    from(
                    SELECT a.ID, a.IATA_CODE , f.AIRLINE_ID, count(*) 
                    FROM airports a, flights f
                    WHERE a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID 
                    GROUP BY  a.ID , a.IATA_CODE , f.AIRLINE_ID 
                    ) as tmp
                    group by tmp.ID, tmp.IATA_CODE
                    having n >= %s"""

        cursor.execute(query, (nMin,))

        for row in cursor:
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
            from flights f 
            group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
            order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                            idMap[row["DESTINATION_AIRPORT_ID"]],
                                            row["n"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, COALESCE(t1.n, 0) + coalesce(t2.n ,0) as peso
        from
        (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
        FROM flights f 
        group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
        order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t1
        left join
        (SELECT f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as n
        FROM flights f 
        group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
        order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID ) t2
        on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID
        where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or t2.ORIGIN_AIRPORT_ID is null
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                            idMap[row["DESTINATION_AIRPORT_ID"]],
                                            row["peso"]))

        cursor.close()
        conn.close()
        return result
