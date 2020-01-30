"""
Template for dokuwiki

:Author:
    Fernando Cosentino
    https://github.com/fbcosentino/
    
"""

FIELD_TABLE = ['',''] # enclosures for the outter table (like ['<table>','</table>'] )
FIELD_ROW = ['','|\n'] # enclosures for each field container/row (field + value) (like ['<tr>','</tr>'] )
FIELD_NAME = ['^ ','  '] # enclosure for the field name (like ['<th>','</th>'] )
FIELD_BODY = ['| ','  '] # enclosure for the field body (the contents) (like ['<td>','</td>'] )

FIELD_TRANSLATE = {
    'returns': 'Returns'
}

OBJECT_ENCLOSURE = ['\n-----\n\n','']