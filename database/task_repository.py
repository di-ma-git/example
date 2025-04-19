import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskRepository:

    def __init__(self, db_connection):
        self.conn = db_connection

    def delete_task_by_task_id(self, task_id: str) -> bool:
        query = ('DELETE FROM fed.tb_tasks WHERE id_ = %s;', (task_id,))
        try:

            with self.conn.cursor() as curs:
                logger.info(f"Deleting task {task_id}...")
                curs.execute(query[0], query[1])
                logger.info(f"Executed query: {query[0]} with params: {query[1]}")
                rows_deleted = curs.rowcount
                self.conn.commit()
                logger.info("Transaction committed")
                return rows_deleted > 0

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error deleting task {task_id}: {e}")
            raise RuntimeError(f"Error deleting task: {e}") from e

    def delete_task_by_task_id_from_all_tables(self, task_id: str) -> bool:

        queries = [
            ('DELETE FROM fed.tb_actions WHERE task_id_ = %s;', (task_id,)),
            ('DELETE FROM fed.tb_tasks_extension WHERE id_ = %s;', (task_id,)),
            ('DELETE FROM fed.tb_passes WHERE task_id_ = %s;', (task_id,)),
            ('DELETE FROM fed.tb_scc_message_id_suffixes WHERE task_id_ = %s;', (task_id,)),
            ('DELETE FROM fed.tb_files WHERE task_id_ = %s;', (task_id,)),
            ('DELETE FROM fed.tb_tasks WHERE id_ = %s;', (task_id,))
        ]

        try:

            with self.conn.cursor() as curs:
                logger.info(f"Deleting task {task_id} from all tables...")
                for query, param in queries:
                    curs.execute(query, param)
                    logger.info(f"Executed query: {query} with params: {param}")

                self.conn.commit()
                logger.info("Transaction committed")
                return True

        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error deleting task {task_id}: {e}")
            raise RuntimeError(f"Error deleting task: {e}") from e

    def get_task_by_task_id(self, task_id: str) -> str:
        query = ('SELECT data_ FROM fed.tb_tasks WHERE id_ = %s;', (task_id,))
        try:

            with self.conn.cursor() as curs:
                logger.info(f"Finding task by task_id {task_id}")
                curs.execute(query[0], query[1])
                logger.info(f"Executed query: {query[0]} with params: {query[1]}")
                data = curs.fetchone()
                if data is None:
                    raise ValueError(f"Task with task_id {task_id} not found")
                return data[0]

        except Exception as e:
            logger.error(f"Error getting task {task_id}: {e}")
            raise RuntimeError(f"Error retrieving task: {e}") from e

    def get_task_status(self, task_id: str) -> str:
        query = ('SELECT status_ FROM fed.tb_tasks WHERE id_ = %s', (task_id,))
        try:
            with self.conn.cursor() as curs:
                logger.info(f"Getting task status by task_id {task_id}")
                curs.execute(query[0], query[1])
                logger.info(f"Executed query: {query[0]} with params: {query[1]}")
                status = curs.fetchone()
                if status is None:
                    raise RuntimeError(f"Task status with taskId {task_id} not found")
                return status[0]
        except Exception as e:
            logger.error(f"Error getting task status, {task_id}: {e}")
            raise RuntimeError(f"Error retrieving task status: {e}") from e

    def get_confirm_email_code_by_task_id(self, task_id: str) -> str:
        query = ('SELECT code_ FROM fed.tb_passes WHERE task_id_ = %s', (task_id,))
        try:
            with self.conn.cursor() as curs:
                logger.info(f"Getting confirm email code by task_id {task_id}")
                curs.execute(query[0], query[1])
                logger.info(f"Executed query: {query[0]} with params: {query[1]}")
                code = curs.fetchone()
                if code is None:
                    raise RuntimeError(f"Email confirm code with task_id {task_id} not found")
                return code[0]
        except Exception as e:
            logger.error(f"Error getting email confirm code, {task_id}: {e}")
            raise RuntimeError(f"Error retrieving email confirm code: {e}") from e
