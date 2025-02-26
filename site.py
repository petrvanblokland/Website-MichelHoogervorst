#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Buro Petr van Blokland + Claudia Mens
#     www.pagebot.io
#     Licensed under MIT conditions
#
#     Supporting DrawBot, www.drawbot.com
#     Supporting Flat, xxyxyz.org/flat
# -----------------------------------------------------------------------------
#
#     siteAutoStyle.py
#
from __future__ import division # Make integer division result in float.

import os
from pagebot.publications.publication import Publication
from pagebot.constants import URL_JQUERY, URL_MEDIA
from pagebot.typesetter import Typesetter
from pagebot.elements import *
from pagebot.toolbox.color import color, whiteColor
from pagebot.toolbox.units import em
from pagebot.toolbox.dating import now

MD_PATH = 'content.md'
EXPORT_PATH = 'docs'

DO_FILE = 'File' # Generate website output in _export/SimpleSite and open browser on file index.html
DO_MAMP = 'Mamp' # Generate website in /Applications/Mamp/htdocs/SimpleSite and open a localhost
#DO_GIT = 'Git' # Generate website and commit to git (so site is published in git docs folder.
EXPORT_TYPE = DO_FILE

class Header(Element):
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.header(cssClass='wrapper clearfix')
        for e in self.elements:
            e.build_html(view, path)
        b._header()
        b.comment('End '+self.__class__.__name__)

class Banner(Element):
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId='banner')
        for e in self.elements:
            e.build_html(view, path)
        b._div()
        b.comment('End #banner')
        b.comment('End '+self.__class__.__name__)

class Navigation(Element):            
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.nav(cssId='topnav', role='navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._nav()
        b.comment('End '+self.__class__.__name__)
        
class TopMenu(Element):        
    def build_html(self, view, path):
        b = self.context.b        
        b.comment('Start '+self.__class__.__name__)
        b.div(cssClass='menu-toggle')
        b.addHtml('Menu')
        b._div()
        b.comment('.menu-toggle')
        b.ul(cssClass='srt-menu', cssId='menu-main-navigation')
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        b.comment('End '+self.__class__.__name__)
        
class Menu(Element):        
    def build_html(self, view, path):
        b = self.context.b        
        b.ul()
        for e in self.elements:
            e.build_html(view, path)
        b._ul()
        
class MenuItem(Element):
    def __init__(self, href=None, label=None, current=False, **kwargs):
        Element.__init__(self, **kwargs)
        self.current = current
        self.href = href
        self.label = label
        
    def build_html(self, view, path):
        u"""
        <li>
            <a href="index.html">Home</a>
        </li>
        """
        b = self.context.b
        if self.current:
            isCurrent = 'current'
        else:
            isCurrent = None
        b.li(cssClass=isCurrent)
        if self.href and self.label:
            b.a(href=self.href)
            b.addHtml(self.label)
            b._a()
        for e in self.elements:
            e.build_html(view, path)
        b._li()
        
class Logo(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Logo')
    
    def build(self, view, path):
        pass
        
    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId="logo")
        b.a(href="index.html")
        for e in self.elements:
            e.build_html(view, path)
        b._a()
        b._div() 
        b.comment('End #logo')
        b.comment('End '+self.__class__.__name__)

class SlideShow(Element):
    def newSlide(self):
        return newTextBox('', parent=self)

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        for i, e in enumerate(self.elements):
            cssClass = 'slide fade'
            if i == 0:
                cssClass += ' firstSlide'
            b.div(cssClass=cssClass)
            e.build_html(view, path)
            b._div()
            b.comment('End .slides .fade')
        b.comment('End '+self.__class__.__name__)
            
class Hero(Element):
    def __init__(self, introId=None, slidesId=None, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId=introId or 'Introduction')
        print('fdfds', slidesId)
        SlideShow(parent=self, cssId=slidesId or 'HeroSlides')

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.section(cssId='hero', cssClass='clearFix')
        b.div(cssClass='wrapper')
        b.div(cssClass='row')
        
        b.div(cssClass='grid_4')
        self.deepFind('Introduction').build_html(view, path)
        b._div()
        b.comment('End .grid_4')
        
        b.div(cssClass="grid_8")
        self.deepFind('HeroSlides').build_html(view, path)        
        b._div()
        b.comment('End .grid_8')

        b._div() # end .row 
        b.comment('End .row')
        b._div() # end .wrapper 
        b._section()
        b.comment('End .wrapper')
        b.comment('End '+self.__class__.__name__)
                               
class Content(Element):
    def __init__(self, contentId=None, **kwargs):
        Element.__init__(self, **kwargs)
        #newTextBox('', parent=self, cssId=contentId or 'Content')
        newTextBox('', parent=self, cssId='Content')

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.div(cssId='main', cssClass='wrapper clearfix')
        b.section(cssId='content', cssClass='wide-content' )
        # Content here, should come from markdown file.
        for e in self.elements:
            e.build_html(view, path)
        #b.p()
        #b.a(href='index.html', cssClass='buttonlink')
        #b.addHtml('Use Pagebot')
        #b._a()
        #b._p()
        b._section() # end content area -->
        b._div() # end div #main .wrapper 
        b.comment('End #main .wrapper .clearfix')
        b.comment('End '+self.__class__.__name__)
        
class ColoredSection(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='ColoredSectionHeader')
        newTextBox('', parent=self, cssId='ColoredSection0')
        newTextBox('', parent=self, cssId='ColoredSection1')
        newTextBox('', parent=self, cssId='ColoredSection2')

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.section(cssId='features', cssClass='blueelement vertical-padding')
        b.div(cssClass='wrapper clearfix')
        self.deepFind('ColoredSectionHeader').build_html(view, path) 
        b.div(cssClass='row vertical-padding')
        
        for n in range(0, 3):
            b.div(cssClass='grid_4')
            self.deepFind('ColoredSection%d' % n).build_html(view, path) 
            b._div() # grid_4
        
        b._div() # row vertical padding
        b.comment('End .row .vertical-padding')
        b._div() # .wrapper
        b.comment('End .wrapper')
        b._section()
        b.comment('End '+self.__class__.__name__)
  
class Footer(Element):
    def __init__(self, **kwargs):
        Element.__init__(self, **kwargs)
        newTextBox('', parent=self, cssId='Footer')

    def build_html(self, view, path):
        b = self.context.b
        b.comment('Start '+self.__class__.__name__)
        b.footer()
        b.div(cssId='colophon', cssClass='wrapper clearfix')
        self.deepFind('Footer').build_html(view, path) 
        b._div()
        b.comment('End #colophon .wrapper .clearfix')
        b._footer()
        b.comment('End '+self.__class__.__name__)
        

class Site(Publication):
    u"""Build a website, similar to the original template by Kirsten Langmuur.

    """

SITE = [
    ('index', 'Home'),
    ('projects', 'Projects'),
    ('works', 'Works'),
    ('exhibitions', 'Exhibitions'),
    ('contact', 'Contact'),
]
style = dict(
    fill=whiteColor,
    margin=em(0),
    padding=em(3),
    fontSize=em(1.1),
    leading=em(1.32),
)
doc = Site(viewId='Site', autoPages=len(SITE), style=style)
view = doc.view
view.resourcePaths = ('css','fonts','images','js')
view.jsUrls = (URL_JQUERY, URL_MEDIA, 'js/main.js')
#view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style.sass.css')
view.cssUrls = ('fonts/webfonts.css', 'css/normalize.css', 'css/style-org.css')

for pn, (name, title) in enumerate(SITE):
    page = doc[pn+1]
    page.name, page.title = name, title
    page.description = 'PageBot SimpleSite is a basic generated template for responsive web design'
    page.keyWords = 'PageBot Python Scripting Simple Demo Site Design Design Space'
    page.viewPort = 'width=device-width, initial-scale=1.0, user-scalable=yes'
    page.style = style
        
    currentPage = name + '.html'
    # Add neste content elements for this page.
    header = Header(parent=page)
    banner = Banner(parent=header, fill=color(0, 0.5, 1))
    logo = Logo(parent=banner, name=name)
    navigation = Navigation(parent=header)
    # TODO: Build this automatic from the content of the pages table.
    menu = TopMenu(parent=navigation)
    menuItem1 = MenuItem(parent=menu, href='index.html', label='Home', current=currentPage=='index.html')
    menuItem2 = MenuItem(parent=menu, href='projects.html', label='Projects', current=currentPage=='projects.html')
    menuItem3 = MenuItem(parent=menu, href='works.html', label='Works', current=currentPage=='works.html')
    menuItem4 = MenuItem(parent=menu, href='exhibitions.html', label='Exhibitions', current=currentPage=='exhibitions.html')
    menuItem5 = MenuItem(parent=menu, href='contact.html', label='Contact', current=currentPage=='contact.html')
    
    menu2 = Menu(parent=menuItem2)
    menuItem21 = MenuItem(parent=menu2, href='projects.html', label='Guess things happen that way', current=False)
    menuItem22 = MenuItem(parent=menu2, href='projects.html', label='OTTHON Leszek', current=False)
    menuItem23 = MenuItem(parent=menu2, href='projects.html', label='Cash in studio', current=False)
    
    menu3 = Menu(parent=menuItem3)
    menuItem31 = MenuItem(parent=menu3, href='works.html', label='Paintings', current=False)
    menuItem32 = MenuItem(parent=menu3, href='works.html', label='Drawings', current=False)

    # WORKS info uit ander bestand halen: archive.md
    menu31 = Menu(parent=menuItem31)
    for n in range(1994, now().year+1):
        MenuItem(parent=menu31, href='works.html', label='%d' % n, current=False)
    menu32 = Menu(parent=menuItem32)
    for n in range(1994, now().year+1):
        MenuItem(parent=menu32, href='works.html', label='%d' % n, current=False)
   
    # Vullen met content van: exhibitions.md
    menu41 = Menu(parent=menuItem4)
    for n in (1996, 1998, 2003, 2004, 2005, 2015, 2016, 2017, 2018):
        MenuItem(parent=menu41, href='works.html', label='%d' % n, current=False)
    
    menu5 = Menu(parent=menuItem5)
    menuItem51 = MenuItem(parent=menu5, href='contact.html', label='Contact', current=False)
    menuItem52 = MenuItem(parent=menu5, href='contact.html', label='CV', current=False)
    menuItem53 = MenuItem(parent=menu5, href='contact.html', label='Links', current=False)
    
    if pn+1 == 1: # Home
        hero = Hero(parent=page, fontSize=em(1.1), fill=0.95)
        content = Content(parent=page, fill=whiteColor)
        section = ColoredSection(parent=page)
    elif pn+1 == 2: # Projects
        hero = Hero(parent=page, fontSize=em(1.1), fill=0.95)
        content = Content(parent=page, fill=whiteColor)
        #hero2 = Hero(parent=page, fontSize=em(1.1), fill=0.95, cssId='Hero2', introId='Introduction2', slidesId='HeroSlides2')
        #content2 = Content(parent=page, fill=whiteColor, contentId='Content2')
        #content3 = Content(parent=page, fill=whiteColor, contentId='Content3')

    elif pn+1 == 3: # Works
        hero = Hero(parent=page, fontSize=em(1.1), fill=0.95)
        content = Content(parent=page, fill=whiteColor)
        #hero2 = Hero(parent=page, fontSize=em(1.1), fill=0.95, cssId='Hero2', introId='Introduction2', slidesId='HeroSlides2')
    elif pn+1 == 4: # Exhibitions
        hero = Hero(parent=page, fontSize=em(1.1), fill=0.95)
        content = Content(parent=page, fill=whiteColor)
        #hero2 = Hero(parent=page, fontSize=em(1.1), fill=0.95, cssId='Hero2', introId='Introduction2', slidesId='HeroSlides2')
    elif pn+1 == 5: # Contact
        content = Content(parent=page, fill=whiteColor)
        #hero2 = Hero(parent=page, fontSize=em(1.1), fill=0.95, cssId='Hero2', introId='Introduction2', slidesId='HeroSlides2')

    section = ColoredSection(parent=page)
    footer = Footer(parent=page)
    
# Create a Typesetter for this document, then create pages and fill content. 
# As no Galley instance is supplied to the Typesetter, it will create one,
# or put the current page/box variables to where the MarkDown file indicates.
t = Typesetter(doc, tryExcept=False, verbose=False)
# Parse the markdown content and execute the embedded Python code blocks.
# The blocks, global defined feedback variables and text content are in the 
# typesetter t.galley.
# By default, the typesetter produces a single Galley with content and code blocks.
# In this case it directly writes into the boxes on the Website template pages.
t.typesetFile(MD_PATH)

if EXPORT_TYPE == DO_FILE:
    doc.export(EXPORT_PATH)
    os.system('open "%s/index.html"' % EXPORT_PATH)
    
elif EXPORT_TYPE == DO_MAMP:
    # Internal CSS file may be switched off for development.
    mampView = doc.newView('Mamp')
    mampView.resourcePaths = view.resourcePaths
    mampView.jsUrls = view.jsUrls
    mampView.cssUrls = view.cssUrls

    MAMP_PATH = '/Applications/MAMP/htdocs/MichelHoogervorstSite' 
    doc.export(path=MAMP_PATH)

    if not os.path.exists(MAMP_PATH):
        print('The local MAMP server application does not exist. Download and in stall from %s.' % view.MAMP_SHOP_URL)
        os.system(u'open %s' % view.MAMP_SHOP_URL)
    else:
        #t.doc.export('_export/%s.pdf' % NAME, multiPages=True)
        os.system(u'open "%s"' % mampView.getUrl('MichelHoogervorstSite'))

elif EXPORTTYPE == DO_GIT and False: # Not supported for SimpleSite, only one per repository?
    # Make sure outside always has the right generated CSS
    view = doc.newView('Git')
    doc.build(path=EXPORT_PATH)
    # Open the css file in the default editor of your local system.
    os.system('git pull; git add *;git commit -m "Updating website changes.";git pull; git push')
    os.system(u'open "%s"' % view.getUrl(DOMAIN))

else: # No output view defined
    print('Set EXPORTTYPE to DO_FILE or DO_MAMP or DO_GIT')

print('Done') 
