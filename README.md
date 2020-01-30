# pydoku

_pydoku_ is a Python documentation generator to dokuwiki format. 

As source, currently supports a subset of _reStructuredText_ syntax in docstrings.

The output is the syntax format used by [dokuwiki](https://www.dokuwiki.org/dokuwiki), a very simple to use and open source wiki plaftorm that _does not require a database_ (as all data is stored in plain text files). Dokuwiki is my system of choice for all documentation and knowledge bases, hence this script.

Usage:

```
python pydoku.py <source_python_file> [destination_text_file]
```

The `destination_text_file` will be created and the dokuwiki content will be written. If not specified, defaults to `dokuwiki.txt`.

Ideally you can have pydoku as a subfolder in your script folder, and call it from there:

```
python pydoku/pydoku.py <your_script>
```

And get the results from `dokuwiki.txt` in your script folder.

**_Warning_**: _the user script will be imported as module. If it has code that runs immediately, that code **will run**!_


## Example:

The example below was created by running the script to read itself (`python pydoku.py pydoku.py`). Notice it starts with a horizontal rule. You can write your custom introduction text above this line, and have the first line separating your description from the API.

```
	
	----
	
	====== pydoku ======
	//**Module**//
	
	pydoku is a Python documentation generator to dokuwiki format. As source
	currently supports a subset of reStructuredText syntax in docstrings.
	
	^ Author  | Fernando Cosentino\\ [[https://github.com/fbcosentino/]]  |
	
	
	
	
	
	-----
	
	===== Dokufy =====
	//**Function**//
	
	Internally calls ScanObject to scan a live object and then
	uses DokufyLevel to generate a dokuwiki documentation string.
	
	^ Object  | The live object to be scanned (usually a module)  |
	^ Use_Class  | (Optional) If not None, only considers this class  |
	^ Use_Func  | (Optional) If not None, only considers this function\\ If use_class is also provided, only considers this method from the class  |
	^ Returns  | Documentation string in dokuwiki syntax  |
	
	
	
	
	
	-----
	
	===== path_leaf =====
	//**Function**//
	
	Function by [[https://stackoverflow.com/users/566644/lauritz-v-thaulow|Lauritz V. Thaulow]]
	
	
	
	
	-----
	
	===== ImportSource =====
	//**Function**//
	
	Imports a python script as a module.
	
	^ Filename  | The script file  |
	^ Returns  | A module object, or None if file not found  |
	
	
	
	
	
	-----
	
	===== DokufyLevel =====
	//**Function**//
	
	Generates dokuwiki documentation based on an object info
	returned by ScanObject, optionally limited to a class,
	function or method inside a class.
	
	Recursively traverses all levels of the object info, so depth
	should be limited in the ScanObject call.
	
	^ Obj_Info  | The object info tree dictionary returned by ScanObject  |
	^ Level  | The starting level for the header. Will be incremented\\ automatically in subsequent recursive calls  |
	^ Use_Class  | (Optional) If not None, only considers this class  |
	^ Use_Func  | (Optional) If not None, only considers this function\\ If use_class is also provided, only considers this method from the class  |
	^ Returns  | Documentation string in dokuwiki syntax  |
	
	
	
	
	
	-----
	
	===== GetParentModuleName =====
	//**Function**//
	
	Gets the name of the module this object belongs to,
	or None if no __module__ attribute is present.
	
	^ Object  | The object to inspect  |
	^ Returns  | Module name as string or None  |
	
	
	
	
	
	-----
	
	===== ScanObject =====
	//**Function**//
	
	Scans an object for type, docstring and non-hidden members,
	recursively scanning members.
	
	Returns a dictionary containing 3 keys:
	
	^ Type  | a string representing the type, as 'module', 'class',\\ 'method', 'function' or 'other'  |
	^ Docstring  | the docstring for the object, not for the members  |
	^ Members  | a dictionary where the keys are the member names, and the\\ values are the results from recursive calls to ScanObject  |
	
	
	Default recursiveness depth is 2 (current object, children and grandchildren).
	This is enough for a module with classes and methods.
	
	^ Object  | A module, class, function or method.  |
	^ Depth  | Recursiveness depth\\ (0 means not recursive, this object level only)  |
	^ Returns  | A dictionary  |
	
	
	
	
	
	-----
	
	===== GetSourceFile =====
	//**Function**//
	
	Extracts source file from an object. If it fails
	(e.g. built-in module) returns None
	
	^ Object  | A module or other live python object  |
	^ Returns  | String or None  |
	
	
	
	
	
	-----
	
	===== GetObjectType =====
	//**Function**//
	
	Inspects an object to find if it is a module, class, method, function or other.
	
	^ Object  | A python live object  |
	^ Returns  | A string containing 'module', 'class', 'method', 'function' or 'other'  |
	
	
	
	
	
	-----
	
	===== ExtractFileCoreName =====
	//**Function**//
	
	Extracts the file name no including directories or extensions
```

## License

This script is provided under MIT license, described in file LICENSE.txt.