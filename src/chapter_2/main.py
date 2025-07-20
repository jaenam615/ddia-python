from chapter_2.clients.mongo_client import MongoDBClient
from chapter_2.clients.mysql_client import MySQLClient
from chapter_2.services.mongo_service import MongoService
from chapter_2.services.mysql_service import MySQLService

import time

def benchmark(service, resume_id, runs=1000):
    total = 0
    for _ in range(runs):
        start = time.perf_counter()
        service.get_resume(resume_id)
        end = time.perf_counter()
        total += (end - start)
    print(f"Average time over {runs} runs: {total / runs:.6f} seconds")

if __name__ == '__main__':
    mysql_service = MySQLService(client=MySQLClient())
    mongo_service = MongoService(client=MongoDBClient())

    if mysql_service.get_resume(resume_id=0) is None:
        mysql_service.create_resume()
    if mongo_service.get_resume(resume_id=0) is None:
        mongo_service.create_resume()

    print("Benchmarking MySQL Service:")
    benchmark(mysql_service, resume_id=0)
    print("Benchmarking MongoDB Service:")
    benchmark(mongo_service, resume_id=0)