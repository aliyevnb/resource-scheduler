import configparser
import os

pathToConfigFile=os.path.abspath("./config.properties")
cfg=configparser.ConfigParser()
cfg.read(pathToConfigFile)


def setAccount():
    return cfg.get("DEFAULTS", "account")

def setRegion():
    return cfg.get("DEFAULTS", "region")

def setVpc():
    return cfg.get("DEFAULTS", "vpc_name")

def setStart():
    return cfg.get("DEFAULTS", "start")

def setStop():
    return cfg.get("DEFAULTS", "stop")

def setSg():
    return cfg.get("DEFAULTS", "sg_name")

def setRole():
    return cfg.get("DEFAULTS", "role_name")