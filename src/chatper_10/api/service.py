class UserService:
    def get_users(self):
        return [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 25, "city": "New York", "role": "admin", "is_active": True, "signup_date": "2024-01-15", "last_login": "2025-09-01T12:34:56", "score": 85.5},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "age": 30, "city": "Los Angeles", "role": "user", "is_active": True, "signup_date": "2023-11-20", "last_login": "2025-08-30T09:15:20", "score": 72.3},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com", "age": 28, "city": "Chicago", "role": "moderator", "is_active": False, "signup_date": "2024-03-12", "last_login": "2025-08-28T18:50:10", "score": 91.0},
            {"id": 4, "name": "David", "email": "david@example.com", "age": 32, "city": "Houston", "role": "user", "is_active": True, "signup_date": "2023-09-05", "last_login": "2025-08-29T14:22:11", "score": 67.8},
            {"id": 5, "name": "Eve", "email": "eve@example.com", "age": 27, "city": "Phoenix", "role": "admin", "is_active": True, "signup_date": "2024-02-18", "last_login": "2025-09-02T08:10:45", "score": 88.1},
            {"id": 6, "name": "Frank", "email": "frank@example.com", "age": 35, "city": "Philadelphia", "role": "user", "is_active": False, "signup_date": "2023-08-22", "last_login": "2025-08-27T21:05:33", "score": 59.9},
            {"id": 7, "name": "Grace", "email": "grace@example.com", "age": 26, "city": "San Antonio", "role": "moderator", "is_active": True, "signup_date": "2024-04-10", "last_login": "2025-08-31T11:45:22", "score": 93.2},
            {"id": 8, "name": "Hannah", "email": "hannah@example.com", "age": 29, "city": "San Diego", "role": "user", "is_active": True, "signup_date": "2023-12-15", "last_login": "2025-08-30T17:30:50", "score": 77.4},
            {"id": 9, "name": "Ian", "email": "ian@example.com", "age": 31, "city": "Dallas", "role": "admin", "is_active": True, "signup_date": "2024-01-30", "last_login": "2025-09-01T09:12:14", "score": 82.0},
            {"id": 10, "name": "Jack", "email": "jack@example.com", "age": 24, "city": "San Jose", "role": "user", "is_active": False, "signup_date": "2024-03-05", "last_login": "2025-08-28T16:45:01", "score": 65.7},
            {"id": 11, "name": "Karen", "email": "karen@example.com", "age": 33, "city": "Austin", "role": "moderator", "is_active": True, "signup_date": "2023-10-12", "last_login": "2025-08-29T19:22:44", "score": 89.5},
            {"id": 12, "name": "Leo", "email": "leo@example.com", "age": 28, "city": "Jacksonville", "role": "user", "is_active": True, "signup_date": "2024-02-25", "last_login": "2025-09-02T10:05:18", "score": 74.8},
            {"id": 13, "name": "Mona", "email": "mona@example.com", "age": 27, "city": "Fort Worth", "role": "admin", "is_active": False, "signup_date": "2024-01-08", "last_login": "2025-08-27T20:15:39", "score": 91.6},
            {"id": 14, "name": "Nina", "email": "nina@example.com", "age": 30, "city": "Columbus", "role": "moderator", "is_active": True, "signup_date": "2023-11-18", "last_login": "2025-08-30T13:55:07", "score": 80.3},
            {"id": 15, "name": "Oscar", "email": "oscar@example.com", "age": 29, "city": "Charlotte", "role": "user", "is_active": True, "signup_date": "2024-03-22", "last_login": "2025-08-31T15:40:12", "score": 78.9},
        ]