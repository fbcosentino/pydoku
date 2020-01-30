"""
docutils Translator for dokuwiki

:Author:
    Fernando Cosentino
    https://github.com/fbcosentino/
    
"""

import doku_template as doku
from docutils import core, nodes
from docutils.writers.html4css1 import Writer,HTMLTranslator
class HTMLFragmentTranslator( HTMLTranslator ):
    def __init__( self, document ):
        HTMLTranslator.__init__( self, document )
        self.head_prefix = ['','','','','']
        self.doctype = ''
        self.html_head = []
        self.stylesheet = []
        
        self.inside_list = 0 # 0=no list, 1=ul, 2=ol
        self.indent_level = 0
        self.is_field_name = False
        self.is_field_body = False
        self.is_python_code = False

        
        
        self.header_from_level = {
            'h2': '=====',
            'h3': '====',
            'h4': '===',
            'h5': '==',
            'h6': '=='
        }
        
    def astext(self):
        return ''.join(self.body)
        
    def visit_Text(self, node):
        text = node.astext()
        #if self.is_python_code is not True:
        #    encoded = self.encode(text)
        #else:
        #    encoded = text
        encoded = text
        
        if self.is_field_name:
            if encoded in doku.FIELD_TRANSLATE:
                encoded = doku.FIELD_TRANSLATE[encoded]
                
            elif encoded.startswith('param '):
                encoded = encoded[6:]
                
            encoded = encoded.title()
        
        elif self.is_field_body:
            encoded = encoded.replace("\n","\\\\ ")
            
        
        indent_prefix = "    "*self.indent_level
        begin_prefix = ""+indent_prefix
        inter_prefix = "\n"+indent_prefix
        
        if   self.inside_list == 1:
            begin_prefix += "  * "
            inter_prefix += "    "
        elif self.inside_list == 2:
            begin_prefix += "  - "
            inter_prefix += "    "
            
        encoded = encoded.replace("\n",inter_prefix)
        
        self.body.append(begin_prefix+encoded)
    
    def visit_emphasis(self, node):
        self.body.append('//')
    
    def depart_emphasis(self, node):
        self.body.append('//')        
    
    def visit_strong(self, node):
        self.body.append('**')
    
    def depart_strong(self, node):
        self.body.append('**')
    
    def visit_literal(self, node):
        # this is inline
        self.body.append("''%%")
    
    def depart_literal(self, node):
        # this is inline
        self.body.append("%%''")
    
    def visit_literal_block(self, node):
        self.body.append('<code>')
    
    def depart_literal_block(self, node):
        self.body.append("</code>\n\n")
    
    def visit_paragraph(self, node):
        pass
    
    def depart_paragraph(self, node):
        if (not (isinstance(node.parent, (nodes.list_item, nodes.entry)) and
                (len(node.parent) == 1))) and (self.is_field_body is False):
            self.body.append("\n\n")
    
    def visit_bullet_list(self, node):
        self.context.append(self.inside_list)
        self.inside_list = 1
    
    def depart_bullet_list(self, node):
        self.inside_list = self.context.pop()
        self.body.append("\n")
        
    def visit_enumerated_list(self, node):
        self.context.append(self.inside_list)
        self.inside_list = 2

    def depart_enumerated_list(self, node):
        self.inside_list = self.context.pop()
        self.body.append("\n")
        
    def visit_list_item(self, node):
        pass

    def depart_list_item(self, node):
        self.body.append("\n")
        
    def visit_subscript(self, node):
        self.body.append('<sub>')

    def depart_subscript(self, node):
        self.body.append('</sub>')   

    def visit_block_quote(self, node):
        self.indent_level += 1

    def depart_block_quote(self, node):
        self.indent_level -= 1     

    def visit_reference(self, node):
        if 'refuri' in node:
            if self.is_field_body is not True:
                self.body.append("[["+node['refuri']+"|")
            else:
                self.body.append("[[")

    def depart_reference(self, node):
        self.body.append(']]')
        if not isinstance(node.parent, nodes.TextElement):
            self.body.append('\n')
            
    def visit_title(self, node):
        """Only 6 section levels are supported by HTML."""
        if isinstance(node.parent, nodes.document):
            self.body.append('===== ')
            close_tag = " =====\n\n"
        else:
            h_level = self.section_level + self.initial_header_level - 1
            h_len = 5-h_level 
            if h_len < 2:
                h_len = 2
            if h_len > 4:
                h_len = 4
            self.body.append("="*h_len+' ')
            close_tag = ' '+"="*h_len+"\n\n"
        self.context.append(close_tag)

    def depart_title(self, node):
        self.body.append(self.context.pop())
        
    # If sections are not used and only one H2 is present,
    # it is subtitle
    def visit_subtitle(self, node):
        self.body.append('== ')

    def depart_subtitle(self, node):
        self.body.append(' ==\n\n')
    
    # If several H2 or several H levels are present, they are sections
    def visit_section(self, node):
        self.section_level += 1
        #self.body.append('section '+str(self.section_level))

    def depart_section(self, node):
        self.section_level -= 1
        #self.body.append('</>\n')
        pass
        
    def visit_transition(self, node):
        self.body.append('--------\n\n')

    def depart_transition(self, node):
        pass
        
    def visit_image(self, node):
        uri = node['uri']
        # image size
        size=''
        if 'width' in node:
            size = '?'+str(node['width'])
            # dokuwiki does not allow height without width
            if 'height' in node:
                size += 'x'+str(node['height'])
                
        img_link = uri+size
        
        if 'align' in node:
            if (node['align'] == 'left') or (node['align'] == 'center'):
                img_link = img_link+' '
            if (node['align'] == 'right') or (node['align'] == 'center'):
                img_link = ' '+img_link
                
        self.body.append('{{'+img_link+'}}')

    def depart_image(self, node):
        pass
        
    def visit_field_list(self, node):
        self.body.append(doku.FIELD_TABLE[0])

    def depart_field_list(self, node):
        self.body.append(doku.FIELD_TABLE[1]+"\n\n")

    def visit_field(self, node):
        self.body.append(doku.FIELD_ROW[0])

    def depart_field(self, node):
        self.body.append(doku.FIELD_ROW[1])
        
    def visit_field_name(self, node):
        self.is_field_name = True
        self.body.append(doku.FIELD_NAME[0])

    def depart_field_name(self, node):
        self.is_field_name = False
        self.body.append(doku.FIELD_NAME[1])

    def visit_field_body(self, node):
        self.is_field_body = True
        self.body.append(doku.FIELD_BODY[0])

    def depart_field_body(self, node):
        self.is_field_body = False
        self.body.append(doku.FIELD_BODY[1])
    
    def visit_doctest_block(self, node):
        self.is_python_code = True
        self.body.append('<code python>\n')

    def depart_doctest_block(self, node):
        self.is_python_code = False
        self.body.append('\n</code>\n\n')
        
    ########## TODO
    
    def visit_definition(self, node):
        self.visit_literal_block(node)

    def depart_definition(self, node):
        self.depart_literal_block(node)

    def visit_definition_list(self, node):
        pass

    def depart_definition_list(self, node):
        pass

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass
        
    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass

html_fragment_writer = Writer()
html_fragment_writer.translator_class = HTMLFragmentTranslator

def to_doku( s ):
    return core.publish_parts( s, writer = html_fragment_writer )['body']

if __name__ == '__main__':
    test = """

H1 text
=======

Subtitle (if used only once after title)
++++++++++++++++++++++++++++++++++++++++

H2 text
~~~~~~~

H3 Text
-------

H4 text
.......

H5 Text
,,,,,,,


*Italic* and **Bold. >>**

::

    Code with no formatting
    all contents are preserved
        indentation of first line is reference

This is a `link to external page
<http://www.external.page>`_.

This is a `link to internal dokuwiki page
<namespace:page>`_.

-----

List items:

- item 1
  item 1 continuing


    1. I1
    2. I2
    3. I3
    
- item 2
- item 3

    - item 3.1 (make sure to add blank line between level changes)
    - item 3.2 (you may remove them after conversion)
    
        - item 3.2.1

This |img_name| is an image.

.. |img_name| image:: ball1.gif


Here is an ``Inline Literal`` element.

::
  
  This code will
  
  be preserved as is

No indentation

    Indented
    Same indented
    
        Nested
        same indentation as nested
        
    :param arg1: description
    :param arg2: description 2
    :returns: value

    >>> Test
    a
    >>> le
    False
        
End of docstring
"""
    res = reST_to_doku(test)
    
    
    print res