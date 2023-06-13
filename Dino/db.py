import psycopg2

def create_table():
    try:
        conn = psycopg2.connect(
            host="rogue.db.elephantsql.com",
            port=5432,  
            database="wocsykfv", 
            user="wocsykfv",  
            password="rwPJlc2S6ceN1uDanxX3cS9f2w9NCDJQ"  
        )
    except Exception as e:
        print(f'Error: {e}')
        return 'ERROR'
    cur = conn.cursor()
    try:
        query = """
        CREATE TABLE game_results (
        game_id SERIAL PRIMARY KEY, 
        game_title VARCHAR(50) NOT NULL,
        points INTEGER,
        level INTEGER
    )
        """
        cur.execute(query)
    except:
        return None
    
    conn.commit()
    conn.close()
    cur.close()

create_table()

# from dino import score

def manage_connection(query):
    try:
        connection = psycopg2.connect(
            host="rogue.db.elephantsql.com",
            port=5432,  
            database="wocsykfv", 
            user="wocsykfv",  
            password="rwPJlc2S6ceN1uDanxX3cS9f2w9NCDJQ"  
        )
        with connection:
            with connection.cursor() as cursor:
                if "SELECT" in query:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
                else:
                    cursor.execute(query)
                    connection.commit()
    except Exception as e:
        print(e)
    finally:
        connection.close()

def get_result():
        query = f"""
        SELECT MAX(points) FROM game_results
        """
        if manage_connection(query) == []:
            return None
        else:
            result = manage_connection(query)
            return result


highest_score = int(get_result()[0][0])
# print(type(highest_score))
# print(highest_score)