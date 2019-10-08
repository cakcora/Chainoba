from easydict import EasyDict as edict

# initialization
__C = edict()
cfg = __C

# postgresql
__C.POSTGRES_PORT = 5432
__C.POSTGRES_URL = "127.0.0.1:{}".format(__C.POSTGRES_PORT)
__C.POSTGRES_USER = "postgres"
__C.POSTGRES_PW = ""
__C.POSTGRES_DB = "bitcoin"

# api
__C.API_PORT = None
