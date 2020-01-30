"""
pydoku is a Python documentation generator to dokuwiki format. As source 
currently supports a subset of reStructuredText syntax in docstrings.

:Author:
    Fernando Cosentino
    https://github.com/fbcosentino/
"""

import os
import sys
import imp
import inspect
import doc2doku
import doku_template as doku


def GetObjectType(object):
    """Inspects an object to find if it is a module, class, method, function or other.
    
    :param object: A python live object
    :returns: A string containing 'module', 'class', 'method', 'function' or 'other'
"""    
    if (inspect.ismodule(object)):
        return 'module'
    elif (inspect.isclass(object)):
        return 'class'
    elif (inspect.ismethod(object)):
        return 'method'
    elif (inspect.isfunction(object)):
        return 'function'
    else:
        return 'other'
        
def path_leaf(path):
    """Function by `Lauritz V. Thaulow <https://stackoverflow.com/users/566644/lauritz-v-thaulow>`_"""
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)
    
def ExtractFileCoreName(filename):
    """Extracts the file name no including directories or extensions"""
    fname, fext = os.path.splitext(path_leaf(filename))
    return fname
    
def GetSourceFile(object):
    """Extracts source file from an object. If it fails
    (e.g. built-in module) returns None
    
    :param object: A module or other live python object
    :returns: String or None
    """
    try:
        filename = inspect.getsourcefile( object )
    except:
        filename = None
        
    return filename
    
def GetParentModuleName(object):
    """Gets the name of the module this object belongs to,
    or None if no __module__ attribute is present.
    
    :param object: The object to inspect
    :returns: Module name as string or None
    """
    
    if (inspect.ismodule(object)):
        val = object.__name__
    else:
        # I really don't like "forgiveness is better than permission"
        # But it's shorter and simpler here
        try:
            val = object.__module__
        except:
            val = None

    return val

def ScanObject(object, depth = 2):
    """Scans an object for type, docstring and non-hidden members,
    recursively scanning members.

    Returns a dictionary containing 3 keys:

    :type: a string representing the type, as 'module', 'class', 
        'method', 'function' or 'other'
    :docstring: the docstring for the object, not for the members
    :members: a dictionary where the keys are the member names, and the 
        values are the results from recursive calls to ScanObject
        
    Default recursiveness depth is 2 (current object, children and grandchildren).
    This is enough for a module with classes and methods.
        
    :param object: A module, class, function or method.
    :param depth: Recursiveness depth 
        (0 means not recursive, this object level only)
    :returns: A dictionary"""
    
    this_file = GetSourceFile( object )
    this_module = GetParentModuleName( object )
    
    res = {}
    res['docstring'] = inspect.getdoc(object)
    res['name'] = object.__name__
    res['type'] = GetObjectType(object)
    res['object'] = object
    
    if res['type'] == 'other':
        return res
    

    # Be careful not do dive into functions, methods etc
    
    if ((res['type'] == 'module') or (res['type'] == 'class')) and (depth > 0):
        members = {}
        mlist = inspect.getmembers(object)
        for eitem in mlist:
            member_name = eitem[0]
            member_value = eitem[1]
            if member_name.startswith('_') is not True:
                member_type = GetObjectType(member_value)
                if (member_type != 'other'):
                    member_file = GetSourceFile( member_value )
                    member_module = GetParentModuleName( member_value )
                    if (member_file == this_file) or (member_module == this_module):
                        members[member_name] = ScanObject(member_value, depth-1)
                    else:
                        #print 'E: '+str(member_name)+" - MFile: "+str(member_file)+"["+str(member_type)+", "+str(member_module)+"]    TFile: "+str(this_file)+"["+str(res['type'])+", "+str(this_module)+"]"
                        pass
        res['members'] = members
    
    return res
    
       
    
def DokufyLevel(obj_info, level = 0, use_class=None, use_func=None):
    """Generates dokuwiki documentation based on an object info
    returned by ScanObject, optionally limited to a class, 
    function or method inside a class.
    
    Recursively traverses all levels of the object info, so depth
    should be limited in the ScanObject call.
    
    :param obj_info: The object info tree dictionary returned by ScanObject
    :param level: The starting level for the header. Will be incremented
        automatically in subsequent recursive calls
    :param use_class: (Optional) If not None, only considers this class
    :param use_func: (Optional) If not None, only considers this function
        If use_class is also provided, only considers this method from the class
    :returns: Documentation string in dokuwiki syntax
    """

    found_func = False
    found_class = False
    
    # Number of '=' chars in the header
    h_num = 6-level
    if h_num < 2:
        h_num = 0
    h_mark = "="*h_num
    
    body = doku.OBJECT_ENCLOSURE[0]
    
    body += h_mark+" "+obj_info['name']+" "+h_mark+"\n//**"+str(obj_info['type']).title()+"**//\n\n"
        
    if (use_class is None) and (use_func is None) and (obj_info['docstring'] is not None):
        body += doc2doku.to_doku(obj_info['docstring'])+"\n\n"
        
    if 'members' in obj_info:
        for emember in obj_info['members']:
            body += DokufyLevel(obj_info['members'][emember], level+1)

    body += doku.OBJECT_ENCLOSURE[1]
    
    return body

def Dokufy(object, use_class=None, use_func=None):
    """Internally calls ScanObject to scan a live object and then
    uses DokufyLevel to generate a dokuwiki documentation string.
    
    :param object: The live object to be scanned (usually a module)
    :param use_class: (Optional) If not None, only considers this class
    :param use_func: (Optional) If not None, only considers this function
        If use_class is also provided, only considers this method from the class
    :returns: Documentation string in dokuwiki syntax

    """
    
    obj_info = ScanObject(object)
    body = DokufyLevel(obj_info, 0, use_class, use_func)
    
    return body
    
    
    
def ImportSource(filename):
    """Imports a python script as a module.
    
    :param filename: The script file
    :returns: A module object, or None if file not found
    """
    
    if not os.path.isfile(filename):
        return None
        
    mname = ExtractFileCoreName(filename)

    code = compile(open(filename).read(), mname, "exec")

    module = imp.new_module(mname)
    
    #old_dir = os.getcwd()
    path = os.path.abspath( os.path.dirname(filename) )
    sys.path.append(path)
    #print os.getcwd()
    #os.chdir( path )
    
    #print os.getcwd()
    module.__file__ = filename

    exec(code, module.__dict__)

    #os.chdir(old_dir)
    #print os.getcwd()

    return module
    
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "\nUsage:\n"
        print "    python pydoku.py <python_script> [dokuwiki_output.txt]\n"
        print "pydoku will import the file as a python module and will try to scan it's"
        print "contents, generating dokuwiki documentation in the output file.\n"
        print "If no output file is specified, defaults to 'dokuwiki.txt'\n"
        quit()
    
    else:
        filename_py = sys.argv[1]
        if len(sys.argv) > 2:
            filename_dw = sys.argv[2]
        else:
            filename_dw = 'dokuwiki.txt'

    try:
        source_module = ImportSource(filename_py)
    except Exception as e:
        print "Error: could not load module from "+str(filename_py)
        print e
        source_module = None
       
    if source_module is not None:
        doc = Dokufy(source_module)
        
        with open(filename_dw, "w") as f: 
            f.write(doc) 
        print "Written to: "+filename_dw+"\n"
