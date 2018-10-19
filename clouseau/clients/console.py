from __future__ import absolute_import
from .abstract import AbstractClient
from jinja2 import Template, Environment, PackageLoader
from .colors import *
import codecs
import re
import subprocess
import sys
import os
import tempfile

class ConsoleClient(AbstractClient):
    """
    Command-line client for Clouseau
    """

    def __init__(self):
        pass

    def render(self, terms, data):
        """
        Much refactoring to do!
            - setup Jinja and template
            - fetch data (parse)
            - highlight search terms
            - render template
            - fix/improve paging
         
        """
        env = Environment(loader=PackageLoader('clouseau', 'templates'))
        env.filters['purple'] = purple
        env.filters['cyan'] = cyan
        env.filters['darkcyan'] = darkcyan
        env.filters['blue'] = blue
        env.filters['darkblue'] = darkblue
        env.filters['red'] = red
        env.filters['darkred'] = darkred
        env.filters['green'] = green
        env.filters['darkgreen'] = darkgreen
        env.filters['yellow'] = yellow
        env.filters['smoke'] = smoke
        env.filters['bold'] = bold
        env.filters['ok'] = ok
        env.filters['fail'] = fail
        env.filters['gray'] = gray
        env.filters['orange_bg'] = orange_bg
          
        template = env.get_template('console.html')
        
        
       # Highlight (Ack! This feels like the worst code I've written) 
        for item in data:
            for x in data[item]:
                for y in data[item][x]:
                    if y == 'matched_lines':
                        match = data[item][x][y]
                        for m in match:
                            for term in terms:
                                if term == item:
                                    regx = re.compile(term, flags=re.I)
                                    match = regx.search( m[1] )
                                    if match:
                                        m[1] = m[1].replace( match.group(0) , orange_bg( match.group(0)  ) )
                                    # This matches only the term, not the matched expression
                                    #m[1] = m[1].replace(term, orange_bg(term) )


        scratchfile_handle, scratchfile_path = tempfile.mkstemp()
        rendered = template.render(data=data)

        with codecs.open(scratchfile_path, 'w', 'utf-8') as scratchfile:
            scratchfile.write(rendered)
        
        try:
            subprocess.call(['less', '-F', '-R', '-S', '-X', '-K'], stdin=scratchfile_handle)
        except KeyboardInterrupt:
            pass
        finally:
            os.remove(scratchfile_path)






