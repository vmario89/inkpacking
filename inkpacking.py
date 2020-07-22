#! /usr/bin/env python
'''
Copyleft ( ) 2009 Celso Junior celsojr2008 at gmail dot com>, 
             2015 Maren Hachmann <marenhachmann@yahoo.com> (updated for Inkscape 0.91)
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

__version__ = "0.11"

import inkex, simplestyle
from math import *
from lxml import etree
from inkex.paths import Path

class inkpacking(inkex.Effect):

    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--width",
                        action="store", type=float,
                        dest="width", default=10.0,
                        help="")
        self.arg_parser.add_argument("--height",
                        action="store", type=float,
                        dest="height", default=15.0,
                        help="")
        self.arg_parser.add_argument("--depth",
                        action="store", type=float,
                        dest="depth", default=3.0,
                        help="")
        self.arg_parser.add_argument("--unit",
                        action="store", type=str,
                        dest="unit", default="mm",
                        help="")
        self.arg_parser.add_argument("--topscheme",
                        action="store", type=str,
                        dest="topscheme", default="rwlf",
                        help="")
        self.arg_parser.add_argument("--botscheme",
                        action="store", type=str,
                        dest="botscheme", default="rwlf",
                        help="")
        self.arg_parser.add_argument("--paper-thickness",
                        action="store", type=float,
                        dest="thickness", default=0.5,
                        help="")
        self.arg_parser.add_argument("-t", "--tab-proportion",
                        action="store", type=float,
                        dest="tabProportion", default=14,
                        help="Inner tab propotion for upper tab")
        self.arg_parser.add_argument("-r", "--lockroundradius",
                        action="store", type=float,
                        dest="lockroundradius", default=18,
                        help="Lock Radius")
        self.arg_parser.add_argument("-c", "--clueflapsize",
                        action="store", type=float,
                        dest="clueflapsize", default=13,
                        help="Clue Flap Size")
        self.arg_parser.add_argument("-a", "--clueflapangle",
                        action="store", type=float,
                        dest="clueflapangle", default=12,
                        help="Clue Flap Angle")
        self.arg_parser.add_argument("--clueflapside",
                        action="store", type=inkex.Boolean, 
                        dest="clueflapside", default=False,
                        help="")    
        self.arg_parser.add_argument("--pages",
                        action="store", type=str, 
                        dest="page", default="page1",
                        help="") 
        self.arg_parser.add_argument("--dustpages",
                        action="store", type=str, 
                        dest="dustpage", default="page1",
                        help="") 
        self.arg_parser.add_argument("--about",
                        action="store", type=str, 
                        dest="about", default="",
                        help="") 
        self.arg_parser.add_argument("--tfal",
                        action="store", type=inkex.Boolean, 
                        dest="tfal", default=False,
                        help="")    
        self.arg_parser.add_argument("--bfal",
                        action="store", type=inkex.Boolean, 
                        dest="bfal", default=False,
                        help="")    
        self.arg_parser.add_argument("--hotmeltprop",
                        action="store", type=float, 
                        dest="hotmeltprop", default=0.6,
                        help="")    
        self.arg_parser.add_argument("--createshapes",
                        action="store", type=inkex.Boolean, 
                        dest="createshapes", default=False,
                        help="")    
        self.arg_parser.add_argument("--createglueshapes",
                        action="store", type=inkex.Boolean, 
                        dest="createglueshapes", default=False,
                        help="")    
        self.arg_parser.add_argument("--fingergrepa",
                        action="store", type=inkex.Boolean, 
                        dest="fingergrepa", default=False,
                        help="")    
        self.arg_parser.add_argument("--fingergrepb",
                        action="store", type=inkex.Boolean, 
                        dest="fingergrepb", default=False,
                        help="")    
        self.arg_parser.add_argument("--fingergrepr",
                        action="store", type=float, 
                        dest="fingergrepr", default=5,
                        help="")    

        self.arg_parser.add_argument("--usetop",
                        action="store", type=inkex.Boolean, 
                        dest="usetop", default=False,
                        help="")    

        self.arg_parser.add_argument("--glueflapinoff",
                        action="store", type=float, 
                        dest="glueflapinoff", default=0,
                        help="")    
        self.arg_parser.add_argument("--glueflapin45",
                        action="store", type=float, 
                        dest="glueflapin45", default=2,
                        help="")    
        self.arg_parser.add_argument("--glueflapinang",
                        action="store", type=float, 
                        dest="glueflapinang", default=7,
                        help="")    
        self.arg_parser.add_argument("--glueflapouoff",
                        action="store", type=float, 
                        dest="glueflapouoff", default=0,
                        help="")    
        self.arg_parser.add_argument("--glueflapou45",
                        action="store", type=float, 
                        dest="glueflapou45", default=3,
                        help="")    
        self.arg_parser.add_argument("--glueflapouang",
                        action="store", type=float, 
                        dest="glueflapouang", default=12,
                        help="")    

        self.arg_parser.add_argument("--bglueflapinoff",
                        action="store", type=float, 
                        dest="bglueflapinoff", default=0,
                        help="")    
        self.arg_parser.add_argument("--bglueflapin45",
                        action="store", type=float, 
                        dest="bglueflapin45", default=2,
                        help="")    
        self.arg_parser.add_argument("--bglueflapinang",
                        action="store", type=float, 
                        dest="bglueflapinang", default=7,
                        help="")    
        self.arg_parser.add_argument("--bglueflapouoff",
                        action="store", type=float, 
                        dest="bglueflapouoff", default=0,
                        help="")    
        self.arg_parser.add_argument("--bglueflapou45",
                        action="store", type=float, 
                        dest="bglueflapou45", default=3,
                        help="")    
        self.arg_parser.add_argument("--bglueflapouang",
                        action="store", type=float, 
                        dest="bglueflapouang", default=12,
                        help="")    


        self.arg_parser.add_argument("--roto",
                        action="store", type=float, 
                        dest="roto", default=0,
                        help="")    

    def effect(self):

        docW = self.getUnittouu(self.document.getroot().get('width'))
        docH = self.getUnittouu(self.document.getroot().get('height'))

        roto = self.getUnittouu( str(self.options.roto)  + self.options.unit )

        boxW = self.getUnittouu( str(self.options.width)  + self.options.unit )
        boxH = self.getUnittouu( str(self.options.height) + self.options.unit )
        boxD = self.getUnittouu( str(self.options.depth)  + self.options.unit )
        boxL = self.getUnittouu( str(self.options.tabProportion)  + self.options.unit )
        thck = self.getUnittouu( str(self.options.thickness)  + self.options.unit )
        fingergrepr = self.getUnittouu( str(self.options.fingergrepr)  + self.options.unit ) 



        gflapsize = self.getUnittouu( str(self.options.clueflapsize)  + self.options.unit )
        gflapangle = self.options.clueflapangle

        gfmirror = self.options.clueflapside
        fingergrepa = self.options.fingergrepa
        fingergrepb = self.options.fingergrepb
        gflapangle = 90 - gflapangle
        usetop = self.options.usetop


        glueflapinoff = self.getUnittouu( str(self.options.glueflapinoff)  + self.options.unit )
        glueflapin45 = self.getUnittouu( str(self.options.glueflapin45)  + self.options.unit )

        lockrr = self.getUnittouu( str(self.options.lockroundradius)  + self.options.unit )

        glueflapinang = self.options.glueflapinang

        glueflapindesl = (( (boxD + boxL) / 2  - glueflapinoff - glueflapin45) /  sin(radians(90 - glueflapinang)) * sin(radians(glueflapinang)))

        glueflapouoff = self.getUnittouu( str(self.options.glueflapouoff)  + self.options.unit )
        glueflapou45 = self.getUnittouu( str(self.options.glueflapou45)  + self.options.unit )
        glueflapouang = self.options.glueflapouang

        glueflapoudesl = (( (boxD + boxL) / 2 - glueflapouoff - glueflapou45) /  sin(radians(90 - glueflapouang)) * sin(radians(glueflapouang)))



        bglueflapinoff = self.getUnittouu( str(self.options.bglueflapinoff)  + self.options.unit )
        bglueflapin45 = self.getUnittouu( str(self.options.bglueflapin45)  + self.options.unit )

        bglueflapinang = self.options.bglueflapinang

        bglueflapindesl = (( (boxD + boxL) / 2  - bglueflapinoff - bglueflapin45) /  sin(radians(90 - bglueflapinang)) * sin(radians(bglueflapinang)))

        bglueflapouoff = self.getUnittouu( str(self.options.bglueflapouoff)  + self.options.unit )
        bglueflapou45 = self.getUnittouu( str(self.options.bglueflapou45)  + self.options.unit )
        bglueflapouang = self.options.bglueflapouang

        bglueflapoudesl = (( (boxD + boxL) / 2 - bglueflapouoff - bglueflapou45) /  sin(radians(90 - bglueflapouang)) * sin(radians(bglueflapouang)))


        tpsc = self.options.topscheme
        btsc = self.options.botscheme
        tfal = self.options.tfal
        bfal = self.options.bfal

        hotmeltp = self.options.hotmeltprop

        angx = asin( (boxL - thck) / lockrr )
        angy = (3.141615 / 2) - angx 
        lockroff = lockrr - (lockrr * sin(angy))

        box_id = self.svg.get_unique_id('box')

        self.box = g = etree.SubElement(self.svg.get_current_layer(), 'g', {'id':box_id})

        line_style = str(inkex.Style(({ 'stroke': '#000000', 'fill': 'none' })))

        gflapoffy = (gflapsize / sin( (gflapangle /  360) * 6.28  )) * sin( ((90 - gflapangle) / 360 ) * 6.28)

        # Side Glueflap
        if not gfmirror:
            line_path = [
                          [ 'M', [ 0 ,  0 ] ],
                          [ 'L', [ gflapsize * -1, gflapoffy ] ],
                          [ 'L', [ gflapsize * -1,  boxH - gflapoffy ] ],
                          [ 'L', [ 0,  boxH ] ],
                          [ 'M', [ 0 ,  0 ] ],
                          [ 'Z', [] ]
                        ]
        
        if gfmirror:
            line_path = [
                          [ 'M', [ boxW+boxD+boxW+boxD - thck,  0 ] ],
                          [ 'L', [ boxW+boxD+boxW+boxD - thck + gflapsize , gflapoffy ] ],
                          [ 'L', [ boxW+boxD+boxW+boxD - thck + gflapsize ,  boxH - gflapoffy ] ],
                          [ 'L', [ boxW+boxD+boxW+boxD - thck,  boxH ] ],
                          [ 'M', [ boxW+boxD+boxW+boxD - thck,  0 ] ],
                          [ 'Z', [] ]
                        ]
        


        line_atts = { 'style':line_style, 'id':box_id+'-sideglueflap', 'd':str(Path(line_path)) }
        etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
   
        

        # MainBody
        line_path = [
                      [ 'M', [ 0 , 0 ] ],
                      [ 'L', [ 0 ,  boxH ] ],
                      [ 'M', [ boxW ,  0 ] ],
                      [ 'L', [ boxW ,  boxH ] ],
                      [ 'M', [ boxW + boxD ,  0 ] ],
                      [ 'L', [ boxW + boxD,  boxH ] ],
                      [ 'M', [ boxW + boxD + boxW ,  0 ] ],
                      [ 'L', [ boxW + boxD + boxW,  boxH ] ],
                      [ 'M', [ boxW + boxD + boxW + boxD - thck ,  0 ] ],
                      [ 'L', [ boxW + boxD + boxW + boxD - thck,  boxH ] ],
                      [ 'M', [ 0, 0 ] ],
                      [ 'Z', [] ]
                    ]
        line_atts = { 'style':line_style, 'id':box_id+'-body', 'd':str(Path(line_path)) }
        etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # No Top Option
        if tpsc == "notp":
            if not fingergrepa and not fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ boxW, 0 ] ],
                              [ 'L', [ boxW + boxD ,  0 ] ],
                              [ 'L', [ boxW + boxD + boxW, 0 ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck, 0 ] ],
                              [ 'Z', [] ]
                            ]
            if fingergrepa and not fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ boxW / 2 - fingergrepr , 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW - boxW / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW , 0 ] ],
                              [ 'L', [ boxW + boxD, 0 ] ],
                              [ 'L', [ boxW + boxD + boxW / 2 - fingergrepr , 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD + boxW - boxW / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW + boxD + boxW , 0 ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , 0 ] ],
                              [ 'M', [ 0 , 0] ],
                              [ 'Z', [] ]
                            ]
            if fingergrepa and fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ boxW / 2 - fingergrepr , 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW - boxW / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW , 0 ] ],
                              [ 'L', [ boxW + boxD / 2 - fingergrepr, 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD - boxD / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW + boxD , 0 ] ],
                              [ 'L', [ boxW + boxD + boxW / 2 - fingergrepr , 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD + boxW - boxW / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW + boxD + boxW , 0 ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck - ( (boxD - thck) / 2 ) - fingergrepr, 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD + boxW - thck + boxD - ( ( boxD - thck ) / 2 ) + fingergrepr  , 0] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , 0 ] ],
                              [ 'M', [ 0 , 0] ],
                              [ 'Z', [] ]
                            ]

            if not fingergrepa and fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ boxW , 0 ] ],
                              [ 'L', [ boxW + boxD / 2 - fingergrepr, 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD - boxD / 2 + fingergrepr, 0] ],
                              [ 'L', [ boxW + boxD , 0 ] ],
                              [ 'L', [ boxW + boxD + boxW , 0 ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck - ( (boxD - thck) / 2 ) - fingergrepr, 0 ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 0, boxW + boxD + boxW - thck + boxD - ( ( boxD - thck ) / 2 ) + fingergrepr  , 0] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , 0 ] ],
                              [ 'M', [ 0 , 0] ],
                              [ 'Z', [] ]
                            ]
            

            line_atts = { 'style':line_style, 'id':box_id+'-topdraw', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # No Bottom Option
        if btsc == "nobt":
            if not fingergrepa and not fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  boxH ] ],
                              [ 'L', [ boxW, boxH ] ],
                              [ 'L', [ boxW + boxD , boxH ] ],
                              [ 'L', [ boxW + boxD + boxW, boxH ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck, boxH ] ],
                              [ 'Z', [] ]
                            ]
            if fingergrepa and not fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  boxH ] ],
                              [ 'L', [ boxW / 2 - fingergrepr , boxH ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW - boxW / 2 + fingergrepr, boxH] ],
                              [ 'L', [ boxW , boxH ] ],
                              [ 'L', [ boxW + boxD, boxH ] ],
                              [ 'L', [ boxW + boxD + boxW / 2 - fingergrepr , boxH ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD + boxW - boxW / 2 + fingergrepr, boxH] ],
                              [ 'L', [ boxW + boxD + boxW , boxH ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , boxH ] ],
                              [ 'M', [ 0 , boxH ] ],
                              [ 'Z', [] ]
                            ]
            if fingergrepa and fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  boxH ] ],
                              [ 'L', [ boxW / 2 - fingergrepr , boxH ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW - boxW / 2 + fingergrepr, boxH] ],
                              [ 'L', [ boxW , boxH ] ],
                              [ 'L', [ boxW + boxD / 2 - fingergrepr, boxH ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD - boxD / 2 + fingergrepr, boxH] ],
                              [ 'L', [ boxW + boxD , boxH  ] ],
                              [ 'L', [ boxW + boxD + boxW / 2 - fingergrepr , boxH  ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD + boxW - boxW / 2 + fingergrepr, boxH ] ],
                              [ 'L', [ boxW + boxD + boxW , boxH ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck - ( (boxD - thck) / 2 ) - fingergrepr, boxH ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD + boxW - thck + boxD - ( ( boxD - thck ) / 2 ) + fingergrepr  , boxH ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , boxH  ] ],
                              [ 'M', [ 0 , boxH ] ],
                              [ 'Z', [] ]
                            ]

            if not fingergrepa and fingergrepb:
                line_path = [
                              [ 'M', [ 0 ,  boxH  ] ],
                              [ 'L', [ boxW , boxH  ] ],
                              [ 'L', [ boxW + boxD / 2 - fingergrepr, boxH  ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD - boxD / 2 + fingergrepr, boxH ] ],
                              [ 'L', [ boxW + boxD , boxH  ] ],
                              [ 'L', [ boxW + boxD + boxW , boxH  ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck - ( (boxD - thck) / 2 ) - fingergrepr, boxH  ] ],
                              [ 'A', [ fingergrepr,  fingergrepr , 0 , 1, 1, boxW + boxD + boxW - thck + boxD - ( ( boxD - thck ) / 2 ) + fingergrepr  , boxH ] ],
                              [ 'L', [ boxW + boxD + boxW + boxD - thck , boxH  ] ],
                              [ 'M', [ 0 , boxH ] ],
                              [ 'Z', [] ]
                            ]
            

            line_atts = { 'style':line_style, 'id':box_id+'-botdraw', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # Flat Bottom with Lock Flaps
        if btsc == "fwlf":
            desloc = 0
            inicut = boxW + boxD
            if not bfal:
                desloc = boxW + boxD
                inicut = 0
            line_path = [
                        [ 'M', [ desloc,boxH ] ],
                        [ 'l', [ 0, boxD * 1] ],
                        [ 'l', [ 6, 0 ] ],
                        [ 'l', [ 0, thck * -2] ],
                        [ 'm', [ 0, thck * 1] ],
                        [ 'l', [ boxW - 12, 0] ],
                        [ 'm', [ 0, thck * -1] ],
                        [ 'l', [ 0, thck * 2] ],
                        [ 'l', [6, 0 ] ],
                        [ 'l', [0, boxD * -1] ],
                        [ 'M', [desloc, boxH ] ],
                        [ 'm', [0, boxD *1] ],
                        [ 'm', [thck, 0] ],
                        [ 'l', [ lockroff , (boxL - thck) * 1 ] ],
                        [ 'l', [boxW - lockroff - lockroff - thck - thck, 0] ],
                        [ 'l', [lockroff , (boxL - thck) * -1 ] ],
                        [ 'M', [desloc,boxH + thck * 1] ],
                        [ 'l', [boxW,0] ],
                        [ 'Z', [] ]
                       ]
            line_atts = { 'style':line_style, 'id':box_id+'-bothead', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if fingergrepa:
                line_path = [
                    ["M", [inicut, boxH]],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["a", [fingergrepr, fingergrepr, 0, 0, 1, fingergrepr * 2,0] ],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-botcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            if not fingergrepa:
                line_path = [
                    ["M", [inicut, boxH]],
                    ["l", [boxW , 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-botcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            
        
        # Flat Top with Lock Flaps
        if tpsc == "fwlf":
            desloc = 0
            inicut = boxW + boxD
            if not tfal:
                desloc = boxW + boxD
                inicut = 0
            line_path = [
                        [ 'M', [ desloc,0 ] ],
                        [ 'l', [ 0, boxD * -1] ],
                        [ 'l', [ 6, 0 ] ],
                        [ 'l', [ 0, thck * 2] ],
                        [ 'm', [ 0, thck * -1] ],
                        [ 'l', [ boxW - 12, 0] ],
                        [ 'm', [ 0, thck] ],
                        [ 'l', [ 0, thck * -2] ],
                        [ 'l', [6, 0 ] ],
                        [ 'l', [0, boxD] ],
                        [ 'M', [desloc, 0 ] ],
                        [ 'm', [0, boxD *-1] ],
                        [ 'm', [thck, 0] ],
                        [ 'l', [ lockroff , (boxL - thck) * -1 ] ],
                        [ 'l', [boxW - lockroff - lockroff - thck - thck, 0] ],
                        [ 'l', [lockroff , (boxL - thck) ] ],
                        [ 'M', [desloc,thck * -1] ],
                        [ 'l', [boxW,0] ],
                        [ 'Z', [] ]
                       ]
            line_atts = { 'style':line_style, 'id':box_id+'-tophead', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if fingergrepa:
                line_path = [
                    ["M", [inicut,0]],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["a", [fingergrepr, fingergrepr, 0, 0, 0, fingergrepr * 2,0] ],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-topcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            if not fingergrepa:
                line_path = [
                    ["M", [inicut,0]],
                    ["l", [boxW , 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-topcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # Rounded Bottom with Lock Flaps
        if btsc == "rwlf":
            desloc = 0
            inicut = boxW + boxD
            if not bfal:
                desloc = boxW + boxD
                inicut = 0
            line_path = [
                        [ 'M', [ desloc,boxH ] ],
                        [ 'l', [ 0, boxD * 1] ],
                        [ 'l', [ 6, 0 ] ],
                        [ 'l', [ 0, thck * -2] ],
                        [ 'm', [ 0, thck * 1] ],
                        [ 'l', [ boxW - 12, 0] ],
                        [ 'm', [ 0, thck * -1] ],
                        [ 'l', [ 0, thck * 2] ],
                        [ 'l', [6, 0 ] ],
                        [ 'l', [0, boxD * -1] ],
                        [ 'M', [desloc, boxH ] ],
                        [ 'm', [0, boxD * 1] ],
                        [ 'm', [thck, 0] ],
                        [ 'a', [lockrr  , lockrr , 0 , 0 , 0, lockroff , (boxL - thck) * 1 ] ],
                        [ 'l', [boxW - lockroff - lockroff - thck - thck, 0] ],
                        [ 'a', [lockrr , lockrr , roto , 0 , 0, lockroff , (boxL - thck) * - 1 ] ],
                        [ 'M', [desloc,boxH + thck * 1] ],
                        [ 'l', [boxW,0] ],
                        [ 'Z', [] ]
                       ]
            line_atts = { 'style':line_style, 'id':box_id+'-bothead', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if fingergrepa:
                line_path = [
                    ["M", [inicut,boxH]],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["a", [fingergrepr, fingergrepr, 0, 0, 1, fingergrepr * 2,0] ],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-botcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            if not fingergrepa:
                line_path = [
                    ["M", [inicut,boxH]],
                    ["l", [boxW , 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-botcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # Rounded Top with Lock Flaps
        if tpsc == "rwlf":
            desloc = 0
            inicut = boxW + boxD
            if not tfal:
                desloc = boxW + boxD
                inicut = 0
            line_path = [
                        [ 'M', [ desloc,0 ] ],
                        [ 'l', [ 0, boxD * -1] ],
                        [ 'l', [ 6, 0 ] ],
                        [ 'l', [ 0, thck * 2] ],
                        [ 'm', [ 0, thck * -1] ],
                        [ 'l', [ boxW - 12, 0] ],
                        [ 'm', [ 0, thck] ],
                        [ 'l', [ 0, thck * -2] ],
                        [ 'l', [6, 0 ] ],
                        [ 'l', [0, boxD] ],
                        [ 'M', [desloc, 0 ] ],
                        [ 'm', [0, boxD *-1] ],
                        [ 'm', [thck, 0] ],
                        [ 'a', [lockrr  , lockrr , 0 , 0 , 1, lockroff , (boxL - thck) * -1 ] ],
                        [ 'l', [boxW - lockroff - lockroff - thck - thck, 0] ],
                        [ 'a', [lockrr , lockrr , roto , 0 , 1, lockroff , (boxL - thck) ] ],
                        [ 'M', [desloc,thck * -1] ],
                        [ 'l', [boxW,0] ],
                        [ 'Z', [] ]
                       ]
            line_atts = { 'style':line_style, 'id':box_id+'-tophead', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if fingergrepa:
                line_path = [
                    ["M", [inicut,0]],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["a", [fingergrepr, fingergrepr, 0, 0, 0, fingergrepr * 2,0] ],
                    ["l", [boxW / 2 - fingergrepr, 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-topcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            if not fingergrepa:
                line_path = [
                    ["M", [inicut,0]],
                    ["l", [boxW , 0] ],
                    ["M", [0,0] ],
                    ["Z", [] ]
                ]
                line_atts = { 'style':line_style, 'id':box_id+'-topcut', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            
        # HotMelt Top
        if tpsc == "fwnf":
            if tfal:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ 0, boxD * -1 ] ],
                              [ 'L', [ boxW, boxD * -1 ] ],
                              [ 'L', [ boxW, 0 ] ],
                              [ 'M', [ boxW, boxD * -1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxD * -1 / 2 ] ],
                              [ 'M', [ boxW + boxD, 0 ] ],
                              [ 'L', [ boxW + boxD, boxD * -1 * hotmeltp ] ],
                              [ 'L', [ boxW + boxD + boxW, boxD * -1 * hotmeltp ] ],
                              [ 'L', [ boxW + boxD + boxW, 0 ] ],
                              [ 'M', [ boxW + boxD + boxW, boxD * -1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxD * -1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, 0 ] ],
                              [ 'M', [ 0 ,  0 - thck ] ],
                              [ 'L', [ boxW ,  0 - thck ] ],
                              [ 'M', [ boxW + boxD ,  0 - thck ] ],
                              [ 'L', [ boxW + boxD + boxW ,  0 - thck ] ],
                              [ 'Z', [] ]
                            ]
                line_atts = { 'style':line_style, 'id':box_id+'-topdraw', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if not tfal:
                line_path = [
                              [ 'M', [ 0 ,  0 ] ],
                              [ 'L', [ 0, boxD * -1 * hotmeltp ] ],
                              [ 'L', [ boxW, boxD * -1 * hotmeltp ] ],
                              [ 'L', [ boxW, 0 ] ],
                              [ 'M', [ boxW, boxD * -1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxD * -1 / 2 ] ],
                              [ 'M', [ boxW + boxD, 0 ] ],
                              [ 'L', [ boxW + boxD, boxD * -1 ] ],
                              [ 'L', [ boxW + boxD + boxW, boxD * -1 ] ],
                              [ 'L', [ boxW + boxD + boxW, 0 ] ],
                              [ 'M', [ boxW + boxD + boxW, boxD * -1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxD * -1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, 0 ] ],
                              [ 'M', [ 0 ,  0 - thck ] ],
                              [ 'L', [ boxW ,  0 - thck ] ],
                              [ 'M', [ boxW + boxD ,  0 - thck ] ],
                              [ 'L', [ boxW + boxD + boxW ,  0 - thck ] ],
                              [ 'Z', [] ]
                            ]
                line_atts = { 'style':line_style, 'id':box_id+'-topdraw', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        # HotMelt Bottom
        if btsc == "fwnf":
            if bfal:
                line_path = [
                              [ 'M', [ 0 ,  boxH ] ],
                              [ 'L', [ 0, boxH + boxD * 1 ] ],
                              [ 'L', [ boxW, boxH + boxD * 1 ] ],
                              [ 'L', [ boxW, boxH ] ],
                              [ 'M', [ boxW, boxH + boxD * 1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxH + boxD * 1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxH ] ],
                              [ 'L', [ boxW + boxD, boxH + boxD * 1 * hotmeltp ] ],
                              [ 'L', [ boxW + boxD + boxW, boxH + boxD * 1 * hotmeltp ] ],
                              [ 'L', [ boxW + boxD + boxW, boxH ] ],
                              [ 'M', [ boxW + boxD + boxW, boxH + boxD * 1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxH + boxD * 1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxH ] ],
                              [ 'M', [ 0 ,  boxH + thck ] ],
                              [ 'L', [ boxW ,  boxH + thck ] ],
                              [ 'M', [ boxW + boxD ,  boxH + thck ] ],
                              [ 'L', [ boxW + boxD + boxW ,  boxH + thck ] ],
                              [ 'Z', [] ]
                            ]
                line_atts = { 'style':line_style, 'id':box_id+'-botdraw', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

            if not bfal:
                line_path = [
                              [ 'M', [ 0 ,  boxH ] ],
                              [ 'L', [ 0, boxH + boxD * 1 * hotmeltp ] ],
                              [ 'L', [ boxW, boxH + boxD * 1 * hotmeltp ] ],
                              [ 'L', [ boxW, boxH ] ],
                              [ 'M', [ boxW, boxH + boxD * 1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxH + boxD * 1 / 2 ] ],
                              [ 'M', [ boxW + boxD, boxH ] ],
                              [ 'L', [ boxW + boxD, boxH + boxD * 1 ] ],
                              [ 'L', [ boxW + boxD + boxW, boxH + boxD * 1 ] ],
                              [ 'L', [ boxW + boxD + boxW, boxH ] ],
                              [ 'M', [ boxW + boxD + boxW, boxH + boxD * 1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxH + boxD * 1 /2 ] ],
                              [ 'M', [ boxW + boxD + boxW + boxD - thck, boxH ] ],
                              [ 'M', [ 0 ,  boxH + thck ] ],
                              [ 'L', [ boxW ,  boxH + thck ] ],
                              [ 'M', [ boxW + boxD ,  boxH + thck ] ],
                              [ 'L', [ boxW + boxD + boxW ,  boxH + thck ] ],
                              [ 'Z', [] ]
                            ]
                line_atts = { 'style':line_style, 'id':box_id+'-botdraw', 'd':str(Path(line_path)) }
                etree.SubElement(g, inkex.addNS('path','svg'), line_atts )

        thck2 = thck / 2

        # Top Glue Flaps
        if tpsc <> "notp":
            desclock = thck
            if tpsc == "fwnf":
                desclock = 0
            if tfal:
                line_path = [
                              [ 'M', [ boxW ,  0 ] ],
                              [ 'l', [ 0, glueflapinoff * -1] ],  
                              [ 'l', [ glueflapin45, glueflapin45 * -1] ],  
                              [ 'l', [ glueflapindesl, ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * -1 + thck2] ],  
                              [ 'M', [ boxW + boxD ,  0 ] ],
                              [ 'l', [ desclock * -1,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * -1] ],  
                              [ 'l', [ glueflapou45 * -1, glueflapou45 * -1] ],  
                              [ 'l', [ glueflapoudesl * -1, ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * -1 + thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock) * -1, 0 ] ],
                              [ 'M', [ boxW ,  0 ] ],
                              [ 'l', [ boxD - desclock ,  0 ] ],
                              [ 'M', [ boxW + boxW + boxD + boxD - thck ,  0 ] ],
                              [ 'l', [ 0, glueflapinoff * -1] ],  
                              [ 'l', [ glueflapin45 * -1, glueflapin45 * -1] ],  
                              [ 'l', [ glueflapindesl * -1 , ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * -1 + thck2] ],  
                              [ 'M', [ boxW + boxD + boxW ,  0 ] ],
                              [ 'l', [ desclock ,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * -1] ],  
                              [ 'l', [ glueflapou45 , glueflapou45 * -1] ],  
                              [ 'l', [ glueflapoudesl , ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * -1 + thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock -thck ) , 0 ] ],
                              [ 'M', [ boxW + boxD + boxW + desclock ,  0 ] ],
                              [ 'l', [ boxD - thck - desclock ,  0 ] ],
                              [ 'Z', [] ]
                             ]

            if not tfal:
                line_path = [
                              [ 'M', [ boxW + boxD,  0 ] ],

                              [ 'l', [ 0, glueflapinoff * -1] ],  
                              [ 'l', [ glueflapin45 * -1, glueflapin45 * -1] ],  
                              [ 'l', [ glueflapindesl * -1 , ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * -1 + thck2] ],  
                              [ 'M', [ boxW ,  0 ] ],
                              [ 'l', [ desclock ,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * -1] ],  
                              [ 'l', [ glueflapou45 , glueflapou45 * -1] ],  
                              [ 'l', [ glueflapoudesl , ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * -1 + thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock) , 0 ] ],
                              [ 'M', [ boxW + desclock ,  0 ] ],
                              [ 'l', [ boxD - desclock ,  0 ] ],
                
                              [ 'M', [ boxW + boxD + boxW ,  0 ] ],
                              [ 'l', [ 0, glueflapinoff * -1] ],  
                              [ 'l', [ glueflapin45, glueflapin45 * -1] ],  
                              [ 'l', [ glueflapindesl, ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * -1 + thck2] ],  
                              [ 'M', [ boxW + boxD + boxW + boxD - thck ,  0 ] ],
                              [ 'l', [ desclock * -1,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * -1] ],  
                              [ 'l', [ glueflapou45 * -1, glueflapou45 * -1] ],  
                              [ 'l', [ glueflapoudesl * -1, ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * -1 + thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock -thck) * -1, 0 ] ],
                              [ 'M', [ boxW + boxD + boxW ,  0 ] ],
                              [ 'l', [ boxD -thck - desclock ,  0 ] ],
                              [ 'Z', [] ]
                             ]


            line_atts = { 'style':line_style, 'id':box_id+'-topglueflap', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
                
        # Bottom Glue Flaps
	if not usetop:
		glueflapinoff = bglueflapinoff
		glueflapin45 = bglueflapin45
		glueflapindesl = bglueflapindesl
		glueflapouoff = bglueflapouoff
		glueflapou45 = bglueflapou45
		glueflapoudesl = bglueflapoudesl

        if btsc <> "nobt":
            desclock = thck
            if btsc == "fwnf":
                desclock = 0
            if bfal:
                line_path = [
                              [ 'M', [ boxW ,  boxH ] ],
                              [ 'l', [ 0, glueflapinoff * 1] ],  
                              [ 'l', [ glueflapin45, glueflapin45 * 1] ],  
                              [ 'l', [ glueflapindesl, ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * 1 -thck2] ],  
                              [ 'M', [ boxW + boxD ,  boxH ] ],
                              [ 'l', [ desclock * -1,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * 1] ],  
                              [ 'l', [ glueflapou45 * -1, glueflapou45 * 1] ],  
                              [ 'l', [ glueflapoudesl * -1, ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * 1 -thck2 ] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock) * -1, 0 ] ],
                              [ 'M', [ boxW ,  boxH ] ],
                              [ 'l', [ boxD - desclock ,  0 ] ],
                              [ 'M', [ boxW + boxW + boxD + boxD - thck ,  boxH ] ],
                              [ 'l', [ 0, glueflapinoff * 1] ],  
                              [ 'l', [ glueflapin45 * -1, glueflapin45 * 1] ],  
                              [ 'l', [ glueflapindesl * -1 , ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * 1 - thck2] ],  
                              [ 'M', [ boxW + boxD + boxW ,  boxH ] ],
                              [ 'l', [ desclock ,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * 1] ],  
                              [ 'l', [ glueflapou45 , glueflapou45 * 1] ],  
                              [ 'l', [ glueflapoudesl , ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * 1 -thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock -thck ) , 0 ] ],
                              [ 'M', [ boxW + boxD + boxW + desclock ,  boxH ] ],
                              [ 'l', [ boxD - thck - desclock ,  0 ] ],
                              [ 'Z', [] ]
                             ]

            if not bfal:
                line_path = [
                              [ 'M', [ boxW + boxD,  boxH ] ],

                              [ 'l', [ 0, glueflapinoff * 1] ],  
                              [ 'l', [ glueflapin45 * -1, glueflapin45 * 1] ],  
                              [ 'l', [ glueflapindesl * -1 , ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * 1 - thck2] ],  
                              [ 'M', [ boxW ,  boxH ] ],
                              [ 'l', [ desclock ,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * 1] ],  
                              [ 'l', [ glueflapou45 , glueflapou45 * 1] ],  
                              [ 'l', [ glueflapoudesl , ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * 1 - thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock) , 0 ] ],
                              [ 'M', [ boxW + desclock ,  boxH ] ],
                              [ 'l', [ boxD - desclock ,  0 ] ],
                
                              [ 'M', [ boxW + boxD + boxW ,  boxH ] ],
                              [ 'l', [ 0, glueflapinoff * 1] ],  
                              [ 'l', [ glueflapin45, glueflapin45 * 1] ],  
                              [ 'l', [ glueflapindesl, ((boxD + boxL) / 2 - glueflapinoff - glueflapin45) * 1 - thck2] ],  
                              [ 'M', [ boxW + boxD + boxW + boxD - thck ,  boxH ] ],
                              [ 'l', [ desclock * -1,  0 ] ],
                              [ 'l', [ 0, glueflapouoff * 1] ],  
                              [ 'l', [ glueflapou45 * -1, glueflapou45 * 1] ],  
                              [ 'l', [ glueflapoudesl * -1, ((boxD + boxL) / 2 - glueflapouoff - glueflapou45) * 1 - thck2] ],
                              [ 'l', [ (boxD - glueflapindesl - glueflapoudesl - glueflapin45 - glueflapou45 - desclock -thck) * -1, 0 ] ],
                              [ 'M', [ boxW + boxD + boxW ,  boxH ] ],
                              [ 'l', [ boxD -thck - desclock ,  0 ] ],
                              [ 'Z', [] ]
                             ]


            line_atts = { 'style':line_style, 'id':box_id+'-botglueflap', 'd':str(Path(line_path)) }
            etree.SubElement(g, inkex.addNS('path','svg'), line_atts )
            
    def getUnittouu(self, param):
        try:
            return self.svg.unittouu(param)
        except AttributeError:
            return self.unittouu(param)

      
if __name__ == '__main__':
    e = inkpacking()
    e.run()
