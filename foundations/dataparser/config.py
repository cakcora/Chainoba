from easydict import EasyDict as edict

# initialization
__C = edict()
cfg = __C

# postgresql
__C.POSTGRES_DB = "blockchain"
__C.POSTGRES_PORT = 5432

#remote
#__C.POSTGRES_USER = "blockchain"
#__C.POSTGRES_PW = "uofm"
#__C.POSTGRES_HOST = "159.203.28.234"

#local
__C.POSTGRES_USER = "postgres"
__C.POSTGRES_PW = "postgres"
__C.POSTGRES_HOST = "127.0.0.1"

# api
__C.API_PORT = 8080