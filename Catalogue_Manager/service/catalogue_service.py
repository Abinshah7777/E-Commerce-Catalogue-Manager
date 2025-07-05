from dto.catalogue_dto import Catalogue
from util.db_get_connection import get_connection
from exceptions.exceptions import CatalogueNotFoundError, CatalogueAlreadyExistsError
import mysql.connector

class CatalogueService:

    def create_catalogue(self, catalogue: Catalogue):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO catalogue (catalogue_id, catalogue_name, catalogue_version, 
                                       is_cat_active, catalogue_start, catalogue_end)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = (
                catalogue.catalogue_id,
                catalogue.catalogue_name,
                catalogue.catalogue_version,
                catalogue.is_cat_active,
                catalogue.catalogue_start,
                catalogue.catalogue_end
            )
            cursor.execute(query, data)
            conn.commit()
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:
                raise CatalogueAlreadyExistsError(f"Catalogue with ID {catalogue.catalogue_id} already exists.")
            else:
                raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def get_catalogue_by_id(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            raise CatalogueNotFoundError(f"Catalogue ID {catalogue_id} not found.")
        return Catalogue(*row)

    def update_catalogue_by_id(self, catalogue_id, updated_catalogue: Catalogue):
        conn = get_connection()
        cursor = conn.cursor()

        # Check existence first
        cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise CatalogueNotFoundError(f"Catalogue ID {catalogue_id} not found.")

        query = """
            UPDATE catalogue
            SET catalogue_name = %s, catalogue_version = %s,
                is_cat_active = %s, catalogue_start = %s, catalogue_end = %s
            WHERE catalogue_id = %s
        """
        data = (
            updated_catalogue.catalogue_name,
            updated_catalogue.catalogue_version,
            updated_catalogue.is_cat_active,
            updated_catalogue.catalogue_start,
            updated_catalogue.catalogue_end,
            catalogue_id
        )
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()

    def delete_catalogue_by_id(self, catalogue_id):
        conn = get_connection()
        cursor = conn.cursor()

        # Check if catalogue exists
        cursor.execute("SELECT * FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
        if cursor.fetchone() is None:
            cursor.close()
            conn.close()
            raise CatalogueNotFoundError(f"Catalogue ID {catalogue_id} not found.")

        cursor.execute("DELETE FROM catalogue WHERE catalogue_id = %s", (catalogue_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def get_all_catalogues(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM catalogue")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return [Catalogue(*row) for row in rows]
