# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column,UniqueConstraint
from sqlalchemy.types import Integer, String, TIMESTAMP, SMALLINT, DECIMAL
from application import db
import datetime

class PoolLoadRatio(db.Model):
    __tablename__ = "pool_load_ratio"

    id              = Column(Integer, primary_key=True)
    pool_id         = Column(Integer, nullable=False)
    ratio           = Column(DECIMAL(5,2), nullable=False)
    created         = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    __table_args__ = (UniqueConstraint('pool_id', 'created', name='idx_pool_created'),)

    def __init__(self, pool_id, ratio, created):
        self.pool_id = pool_id
        self.ratio = ratio
        self.created = created
        self.updated = created

