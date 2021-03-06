import sys
import os
import pytest
sys.path.append('./ontologyutils')
import ontologyutils as onto

print("Path at terminal when executing this file")
print(os.getcwd() + "\n")

print("This file path, relative to os.getcwd()")
print(__file__ + "\n")

print("This file full path (following symlinks)")
full_path = os.path.realpath(__file__)
print(full_path + "\n")

print("This file directory and name")
path, file = os.path.split(full_path)
print(path + ' --> ' + file + "\n")

print("This file directory only")
print(os.path.dirname(full_path))

filename = '../samples/hp.obo'
hpo = onto.Ontology.fromOBOFile(filename)

def test_hpoterm_exists():
    # "http://purl.obolibrary.org/obo/HP_0001387"
    # comment;synonym;name;hasDbXref;id;is_a;alt_id;def
    assert "name" in hpo.terms['HP:0001387']['tags'].keys()
    assert hpo.terms['HP:0001387']['tags']['name'][0] == "Joint stiffness"
    ancestors = hpo.getAncestors('HP:0001387')
    # HP:0011842,HP:0000001,HP:0000118,HP:0000924,HP:0001367,HP:0001376,HP:0011729,HP:0001387
    assert not ancestors == None
    assert "HP:0011842" in ancestors
    assert "HP:0000001" in ancestors

def test_hpodbxref_exists():
    for xref in ["SNOMEDCT:299032009", 'MeSH:D014552']:
        terms = hpo.getTermsByDbXref(xref)
        assert not terms == None
        for termId in terms:
            print "{0}: {1}\n".format(xref, ';'.join(hpo.terms[termId]['tags']['name']))

