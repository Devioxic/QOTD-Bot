from redis import Redis
from os import getenv

class Data:
    def __init__(self):
        self.r = Redis(host=getenv("Host"), password=getenv("password"), port=30036, db=1)

    def add_question(self, question: str):
        self.r.sadd("questions", question)

    def get_random_question_and_remove(self):
        return self.r.spop("questions")
    
    def get_random_question(self):
        return self.r.srandmember("questions")
    
    def get_all_questions(self):
        questions = self.r.smembers("questions")
        return {i: question for i, question in enumerate(questions)}
    
    def get_allowed_roles(self):
        return self.r.smembers("allowed_roles")
    
    def get_channel(self):
        return self.r.get("channel")
    
    def add_allowed_role(self, id: int):
        self.r.sadd("allowed_roles", id)

    def set_channel(self, id: int):
        self.r.set("channel", id)

    def set_next_question_time(self, time: int):
        self.r.set("next_question_time", time)

    def get_next_question_time(self):
        return self.r.get("next_question_time")
    
    def remove_question(self, id: int):
        questions = self.r.smembers("questions")
        question = list(questions)[id]
        self.r.srem("questions", question)

    def is_a_question(self, question: str):
        return self.r.sismember("questions", question)

    def remove_allowed_role(self, id: int):
        self.r.srem("allowed_roles", id)

    def check_existing_question(self, question: str):
        return self.r.sismember("questions", question)
    
    def check_allowed_role(self, id: int):
        return self.r.sismember("allowed_roles", id)