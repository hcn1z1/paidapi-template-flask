"""
    this module functions used to control database in general and simple JSON responses
    TABLE = APIS {
        NAME text,
        APIKEY text,
        LogPATH text,
        RemainingREQUESTS integer,
        BALANCE float,
        unique (NAME,APIKEY,LogPATH)
    }

    todo:lock executions
"""