import config
import pymongo
from store.store import DataStore
class MongoFactory(object):
    __instance: pymongo.MongoClient = None

    @staticmethod
    def getConnection():
        if MongoFactory.__instance:
            return MongoFactory.__instance
        MongoFactory.__instance = pymongo.MongoClient(config.MONGO_STRING)
        return MongoFactory.__instance

class MongoStore(DataStore):
    __instance = None
    @staticmethod
    def getInstance():
        if MongoStore.__instance:
            return MongoStore.__instance
        return MongoStore()

    def __init__(self):
        client = MongoFactory.getConnection()
        self.db = client[config.DB_NAME]

    def addMass(self, mass):
        self.db[config.MASS_COL].insert_one(mass)
    
    def addState(self, state):
        self.db[config.STATE_COL].insert_one(state)
        
    
    def addVolume(self, volume):
        self.db[config.VOLUME_COL].insert_one(volume)
    
    def addTime(self, time):
        self.db[config.TIME_COL].insert_one(time)

    def addFloFlow(self, flow):
        self.db[config.FLO_FLOW_COL].insert_one(flow)
    
    def addVelocity(self, velocity):
        self.db[config.VELOCITY_COL].insert_one(velocity)
    
    def addWeight(self, weight):
        self.db[config.WEIGHT_COL].insert_one(weight)
    
    def addFlow(self, flow):
        self.db[config.FLOW_COL].insert_one(flow)
    
    def addTotal(self, total):
        self.db[config.TOTAL_COL].insert_one(total)
    
    def addCommand(self, command):
        self.db[config.COMMAND_COL].insert_one(command)
    
    def _getItem(self, startTime, endTime, skip, limit, collection):
        query = {}
        if startTime:
            query['time'] = {'$gte': startTime}
        if endTime:
            if not query['time']:
                query['time'] = {}
            query['time'].update({'$lte': endTime})
        def f(x):
            x['_id'] = str(x['_id'])
            return x
        return list(map(f, self.db[collection].find(query).limit(limit).skip(skip)))

    def getLastFromCollection(self, collection, limit=1):
        def f(x):
            x['_id'] = str(x['_id'])
            return x
        return list(map(f, self.db[collection].find().limit(limit).sort('time', -1)))
    
    def getLastNonMaxFillState(self):
        def f(x):
            x['_id'] = str(x['_id'])
            return x
        return list(map(f, self.db[config.STATE_COL].find({'state': {'$ne': 'Max reached'}}).limit(1).sort('time', -1)))


    def getMass(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.MASS_COL)

    def getVolume(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.VOLUME_COL)

    def getTime(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.TIME_COL)

    def getState(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.STATE_COL)
    
    def getFloFlow(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.FLO_FLOW_COL)
    
    def getVelocity(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.VELOCITY_COL)
    
    def getWeight(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.WEIGHT_COL)
    
    def getFlow(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.FLOW_COL)
    
    def getTotal(self, startTime, endTime, skip, limit):
        return self._getItem(startTime, endTime, skip, limit, config.TOTAL_COL)