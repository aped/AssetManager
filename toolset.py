#!/usr/bin/env python2.7

""" 
Originally tools to make CSV crawling easier. I've since
decided to skip intermediate CSV files an instead am
interfacing directly with the database. So, tools to interface
with the db and help the parsing/moving of data around. 

by Andrew Pedelty 9/16/2012
"""

import csv, getpass, subprocess
import psycopg2 as pg
from psycopg2.extras import DictCursor
from collections import defaultdict
import pdb

def dne(): 
    """ Helper function for defaultdicts """
    return "dne"

# Global dict to map location_ids to their strings
loc_map = defaultdict(dne, 
                           {1: "test",
                            2: "ISB",
                            3: "NS2",
                            4: "Mt Hamilton",
                            5: "CfAO",
                            6: "Thimann", 
                            7: "Shops",
                            8: "Keck",
                            9: "Kerr",
                            10: "SETI Institute",
                            11: "Remote", 
                            12: "Non-UCO"})

num_map = defaultdict(lambda: None,  # CAN Codes
                                   {"ISB":  98,
                                    "NS2": 179,
                                    "CfAO": 693,
                                    })
                                   
custom_map = defaultdict(lambda: None, # From WHD custom entries to meaningful words again
                                      { 42: "Jack No.",
                                        43: "Hub No.", 
                                        44: "Port No."
                                      })


def tree(): 
    """ 
    Super basic tree data structure thingo. 
    """
    return defaultdict(tree)

def tree_to_dicts(mytree): 
    return {subtree: tree_to_dicts(mytree[subtree]) if type(mytree) != type(tuple()) else mytree for subtree in mytree }

def get_netlist_ip_list(): 
    pass

def get_asset_hostname_list():
    """
    Gets hostnames of ALL assets, not just the ones with populated custom fields.
    """
    conn = pg.connect(database="webhelpdesk", user="psmith", password="")
    dbCur = conn.cursor(cursor_factory=DictCursor)
    dbCur.execute("""select network_name from asset""")
    return [x[0] for x in dbCur.fetchall() if x is not None]

def get_asset_ip_list(): 
    """ 
    Gets ip addresses of ALL assets, not just the ones with populated custom fields.
    """
    conn = pg.connect(database="webhelpdesk", user="psmith", password="")
    dbCur = conn.cursor(cursor_factory=DictCursor)
    dbCur.execute("""select network_address from asset""")
    return [x[0] for x in dbCur.fetchall() if x is not None]

def intify(val): 
    try: 
        return int(val)
    except TypeError as e: 
        return 0
    except ValueError as e: 
        return None
    except Exception as e: 
        return 0

def pull_assets(fname=""):
    """
    Gets a dump of a pgsql table ('assets' by default) and returns it. 
    
    From shell: psql -c "COPY (SELECT * FROM ASSETS) TO $SOMEPATH WITH NULL AS ''"
    or "...TO $SOMEPATH AS CSV" if tabs are no good. 
    
    Do not specify param fname as of current version, not implemented. 
    """
    conn = pg.connect(database="webhelpdesk", user="psmith", password="") # or something. 
    dbCur = conn.cursor(cursor_factory=DictCursor)
    # Hand crafted artisan SQL query: 
    dbCur.execute("""
            select asset.asset_id, definition_id, number_value, network_name, 
            asset.location_id, network_address, room.room_name, mac_address, user_name 
            from asset_custom_field join asset on asset_custom_field.entity_id = 
            asset.asset_id join room on asset.room_id = room.room_id 
            join asset_client on asset.asset_id = asset_client.asset_id 
            join client on asset_client.client_id = client.client_id
            where definition_id in (42, 43, 44) order by asset.asset_id, definition_id
                  """)
    resp = dbCur.fetchall()
    if (fname): 
        raise NotImplementedError ("This space saved against future need!")
    return resp

def transfer(source, dest, user=getpass.getuser()): 
    """ 
    Distribute your newly minted netlist or whatever. In an ideal world, there'd
    be backup checking etc. 
    Slightly ghetto but we're not running this on a windows machine anytime 
    in the near future. 
    Params are: 
    source: Path to local file
    dest: host:/path/to/dest
    user: If you want to do this as someone else.
    """
    p = subprocess.Popen(["scp", source, "%s@%s" % (user, dest)],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE)
    p.wait()
    

# The following are tools used for interacting with c/tsv files; I've since
# decided to do everything in python without intermediate steps, so they're
# 'deprecated'. 

def formatify(astr): 
    """
    An oddity of the TSV output from WHD is that some fields (numerical?)
    seem to be in format ="XXX" instead of just XXX. This fixes that, ideally.
    """
    if astr.startswith('='): 
        return astr[2:-1]
    return astr

def CommentedReader(filename, reader=csv.DictReader, *args, **kwargs): 
    """ 
    My take on a decommenter. Could use a regexp to match
    sth like \w+# but they don't seem to comment at all, much
    less with leading whitespace. So this is quicker. 
    """
    with open(filename, 'rbU') as fh: 
        formatted = (line for line in fh if not line.startswith("#"))
    return reader(formatted, *args, **kwargs)

def get_comments(filename): 
    """
    Gets commented lines from a file. 
    """
    with open(filename, 'rbU') as fh: 
        commented = (line for line in fh if line.startswith('#'))
    return commented

def read_assets(fname='asset_export.txt'): 
    reader = toolset.CommentedReader(fname, delimiter='\t')
    if debugging:
        import pprint
        a = reader
        while 1: 
            try: 
                pprint.pprint(a.next())
            except StopIteration as e: 
                print "Done. ", 
                print e
                break
    return reader

def get_jacks_by_room(bldg, roomnum): 
    pass

class PrettyDefaultDict(defaultdict): 
    def __init__(self, *args, **kwargs): 
        defaultdict.__init__(self, *args, **kwargs)
    def __repr__(self): 
        return str(dict(self))

if __name__ == "__main__": 
    print "Not meant to be called as a standalone."

