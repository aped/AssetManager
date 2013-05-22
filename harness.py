#!/usr/bin/env python2.7


""" re-write of a test harness to work with code in the 'assets' module
    and basically automate testing. 

    now essentially a prototype for the next 'assetparse' module
""" 

import dict_tools
from toolset import PrettyDefaultDict, custom_map, pull_assets, intify, loc_map, tree
from collections import defaultdict
import pdb
import csv

local_netlist_path = "/u/psmith/netlist.data"
local_host_path    = "/u/psmith/host.ethers"


netlist_headers = ["Building", "Hostname", "Room No.", "Jack No.",
                   "Hub No.", "Port No.", "Comments"]
host_headers    = ["Hostname", "Ip", "MAC Address", "Additional Info"]

def create_assets_bigdict(): 
    records = pull_assets()
    assets_metadict = PrettyDefaultDict(lambda: PrettyDefaultDict(str))
    # Build a more reasonable (less flat) data structure here.
    for el in records: 
        aid                      = el[0]
        asset                    = assets_metadict[aid]
        asset[custom_map[el[1]]] = intify(el[2])
        asset['Hostname']        = el[3]
        asset['Building']        = loc_map[el[4]]
        asset['Ip']              = el[5] or "--.--"
        asset['Room No.']        = el[6]
        asset['MAC Address']     = el[7]
        asset['Username']        = el[8]
    return assets_metadict


# ---- DEPRECATED BAD UGLY CODE FOLLOWS ----
# Below are two simple functions for creating the flat files
#def create_netlist(bigdict, filename=""): 
#
#    def write_netlist(filename): 
#        with open(filename, "wb") as fh: 
#            netlist_writer = csv.DictWriter(fh, headers)
#            netlist_writer.writeheaders()
#            for row in netlist: 
#                netlist_writer.writerow(row)
#
#    netlist = []
#    for hostid, info in bigdict.items(): 
#        netlist.append(defaultdict(dne, {
#            'Building': info['building'],
#            'Hostname': info['hostname'],
#            'Room No.': info['roomnum'],
#            'Jack No.': info['Jack'],
#            'Hub No.' : info['Hub'],
#            'Port No.': info['Port'], 
#            'Comments': '' # comments would go here.
#        } ))
#    if filename: 
#        write_netlist(filename)
#        return True
#    else: 
#        return netlist
#
#def create_hosts(bigdict): 
#    host_ethers = []
#    for hostid, info in bigdict.items(): 
#        host_ethers.append(defaultdict(dne, {
#            'Hostname': info['Hostname'],
#            'Ip': info['ip'] or '--.--',
#            'MAC Address': info['mac'],
#            'Additional Info': ', '.join(
#                map(lambda a: str(info[a]), ['Hub', 'Port', 'Jack', 'username']))}))
#    return host_ethers

# Superior, pretty code follows: 
def create_flatfile(bigdict, headers): 
    """ An attempt to unify the host.ethers and netlist.data
        flatfile creation. """
    flat_file = []
    for hostid, info in bigdict.items(): 
        flat_file.append(dict_tools.filter_dict(info, headers))
    return flat_file

def create_moin(bigdict, sep='||'): 
    moinlines = ["""#acl SystemsGroup:admin,read,write,delete,revert All:"""]
    # Start to create a tree structure: 
    moin_tree = tree()
    for anum, asset in bigdict.items(): 
        moin_tree[asset['Building']][asset['Room No.']][asset['Jack No.']] = \
                             (asset['Hostname'], asset['Username']) or 'off'
    # Start to create the flat file structure, in proper format
    for bldg, rooms in moin_tree.items(): 
        moinlines.append("""=== %s ===""" % bldg)
        for room, jacks in rooms.items(): 
            moinlines.append("""=== %s %s ===""" % (bldg, room))
            jup = [(str(k), "%s (%s)" % v) for k,v in jacks.items()] # Linearize because dicts are unordered...
            jackrow = sep+sep.join([e[0] for e in jup])+sep if jup else ""
            userrow = sep+sep.join([e[1] for e in jup])+sep if jup else ""
            moinlines.append(jackrow)
            moinlines.append(userrow)
            moinlines.append("")
    return moinlines, moin_tree



def write_flatfile(flatfile, outfile, headers): 
    """ An attempt to unify host.ethers and netlist.data 
        flatfile writing. """
    with open(outfile, "wb") as fh: 
        writer = csv.DictWriter(fh, headers, delimiter="\t")
        writer.writeheader()
        for row in flatfile:
            writer.writerow(row) 


if __name__ == "__main__": 
    huge_dict = create_assets_bigdict()
    netlist = create_flatfile(huge_dict, netlist_headers)
    host = create_flatfile(huge_dict, host_headers)
    moin, tree = create_moin(huge_dict)
    write_flatfile(netlist, local_netlist_path+'.test', netlist_headers)
    write_flatfile(host, local_host_path+'.test', host_headers)
    with open('../mointest.dat', 'w') as fh: 
        for line in moin: 
            fh.write("""%s\n""" % line)
    print "done"
