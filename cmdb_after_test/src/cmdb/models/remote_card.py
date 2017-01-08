from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String
from application import db


class RemoteCard(db.Model):
    __tablename__ = "remote_card"

    id = Column(Integer, primary_key=True)
    ip_id = Column(Integer, nullable=False)
    user = Column(String(40), nullable=False)
    password = Column(String(40), nullable=False)
    
    def __init__(self,ip_id,user,password):
        self.ip_id = ip_id
        self.user=user
        self.password = password


