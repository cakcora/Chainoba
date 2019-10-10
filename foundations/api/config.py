from easydict import EasyDict as edict

# initialization
__C = edict()
cfg = __C

# postgresql
__C.POSTGRES_USER = "postgres"
__C.POSTGRES_PW = "postgres"
__C.POSTGRES_DB = "bitcoin"
__C.POSTGRES_HOST = "localhost"
__C.POSTGRES_PORT = 5432

# api
__C.API_PORT = None
