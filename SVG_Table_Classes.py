from math import floor

class rectangle(object):
    """This object contains top_left, bottom_right, background, border_color, line_width"""
    def __init__(self):
        self.top_left = [0,0]
        self.bottom_right = [100, 30]
        self.background = (255,255,255)#white background
        self.border_color = (0,0,0)#border color
        self.line_width = 1 #line width


def draw_rec(rect_obj):
    BR = rect_obj.bottom_right
    TL = rect_obj.top_left
    back = rect_obj.background
    stroke_clr = rect_obj.border_color
    lin_width = rect_obj.line_width
    svc_rec_list = ['<rect ',
                    'height="{}"'.format(BR[1]),
                    'width="{}" '.format(BR[0]-TL[0]),
                    'style="',
                    'fill:rgb{};'.format(back),
                    'stroke:rgb{};'.format(stroke_clr),
                    'stroke-width:{}" '.format(lin_width), 
                    'x="{}" '.format(TL[0]+lin_width),
                    'y="{}" />\n'.format(TL[1]+lin_width)]
    return ' '.join(svc_rec_list)

def SVG_text(TL=(0,0), font_size=12, height=16, text='', font_color=(0,0,0), font_weight='normal', x_shift=0, font_family="Arial"):
    """This function generates the SVG text to display text.  It also supports multiple line text is \n is in the text"""
    x,y = TL
    if '\n' in text:
        y+=font_size+1
        #print(TL)
    else:
        y+=int(floor((height+font_size)/2))-1
    x += round(font_size/2) + x_shift
    list_of_text = text.split('\n')
    add_list=[]
    if len(list_of_text)>1:
        for index, text in enumerate(list_of_text[1:]):
            inst_y = y+(index+1)*(font_size+2)
            add_text = '<tspan x="{}" y="{}">'.format(x, inst_y)+text+'</tspan>'
            add_list.append(add_text)
    Text_list = ['<text x="{}" '.format(x),
                 'y="{}" '.format(y),
                 'font-size= "{}" '.format(font_size),
                 'font-weight = "{}" '.format(font_weight),
                 'style="fill:rgb{}" '.format(font_color),
                 'font-family="{}">'.format(font_family),
                 list_of_text[0]]
    Text_list+=add_list#+['\n']
    Text_list+=['</text>\n'] 
    return "".join(Text_list)

def Set_SVG_view(width, height, svg_display_text):
    """This function sets the viewbox and the height of an SVG object."""
    text = '<svg viewBox="0 0 {width} {height}" height="{height}" xmlns="http://www.w3.org/2000/svg" version="1.1">\n'.format(width=width, height=height)
    text+=svg_display_text+'</svg>'
    return(text)



class SVG_Text_obj(object):
    """This is a base class for handeling text objects"""
    def __init__(self, text="", font_size=12, font_color=(0,0,0), font_weight="normal", border_width=1, TL=(0,0), font_family="Arial"):
        """Initiailize"""
        self.line_width = self.check_line_width(border_width)
        self.font_weight = self.check_font_weight(font_weight)
        self.font_color = self.check_color(font_color)
        self.__font_size__ = self.check_font_size(font_size)
        self.__height__ = self.check_height(self.__font_size__, self.line_width)
        self.text = text
        self.Top_left = TL
        self.font_family=font_family


   
    def check_font_weight(self, font_weight):
        """This method validates the font_weight then returens it. Valid weights are
            normal | bold | bolder | lighter | 100 | 200 | 300| 400 | 500 | 600 | 700 | 800 | 900"""
        validweights = ["normal", "bold", "bolder", "lighter", 100, 200, 300, 400, 500,
                        600, 700, 800, 900, '100', '200', '300', '400', '500', '600', 
                        '700', '800', '900']
        try:
            assert(font_weight in validweights)
            return font_weight
        except:
            raise(RuntimeError("Font weight must be one of the following: {}".format(validweights)))
    
    def check_line_width(self, border_width):
        """This method validates the border_width then returns it."""
        try:
            assert(border_width>=0 and border_width == int(border_width))
            return border_width
        except:
            raise(RuntimeError("Line widths must be a positive integer.")) 
    
    def check_font_size(self, size):
        """This method validates size and returns it"""
        try:
            assert(size>=3 and size == int(size))
            return size
        except:
            raise(RuntimeError("Font size must be an integer 3 or greater.")) 
    
    def check_color(self, color):
        """This method is used to set the color of color_to_set or raise an error if
           the RGV values are invalid."""
        try:
            assert(min(color)>=0 and max(color)<256)
            return color
        except:
            raise(RuntimeError("RGB color values must be between 0 and 255 inclusive"))
    
    def check_height(self, font_size, border_width, height_to_check=0):
        """The method determines the minimum height based on the font_size 
           and the with of the lines on top and bottom.  Returns the greater 
           of set_height and the minimum height to set_height."""
        try:
            row_count=len(self.text.split('\n'))#+1
            #print("Here now and row_count is %d"% row_count)
            if row_count<1:
                row_count=1
        except:
            #print("An error occured")
            row_count=1
            pass
        min_height = row_count*(font_size+2*border_width)+2
        #print("min_height = %d"% min_height)
        #print("Height to check is %d" % height_to_check)
        
        return max(min_height, height_to_check)
        
        
    def set_font_size(self, font_size_to_set, size, height_to_set=0, border_width=0):
        """This method validates size then sets font_size_to_set.  If 
           border_width and height_to_set are provided then it will also update the 
           height_to_set."""
        self.__font_size__ = self.check_font_size(size)
        self.__height__ = self.check_height(self.__font_size__, border_width, self.__height__)
        
    def set_height(self, height):
        #print("here")
        self.__height__ = self.check_height(self.__font_size__, self.line_width, height)
        
    
    def get_SVG_text(self):
        return SVG_text(self.Top_left, self.__font_size__, self.__height__, self.text, self.font_color, self.font_weight, font_family=self.font_family)
        


class Table_Header(SVG_Text_obj):
    """This is a header object for the top row of a table.  If the header text using 
       the set_header_text (or this is created with the header text) the header will
       be set to show (self.Show_header = True)."""
    def __init__(self, text="", bordercolor=(0,0,0), height=25, size=14, font_color=(0,0,0), background=(255,255,255), line_width=1, TL=(0,0), width=100, font_family="Arial"):
        """Initiailize"""
        super().__init__(text, size, font_color, "bold", line_width, TL, font_family)
        self.Show_header = False
        self.Header_width = width
        self.set_header_text(text)
        self.__height__ = self.check_height(self.__font_size__, self.line_width, height)
        self.Header_border_color = self.check_color(bordercolor)
        self.Header_background = self.check_color(background)

    
    def set_header_text(self, text=""):
        """This method let the user set the text of the header of the table.  By default if the text is set then the
           header is set to show but it can be turned off by setting self.Show_header=False."""
        if len(text)>0:
            self.text = text
            self.Show_header = True
        else:
            print("No header was added")
            
    @property
    def bottom(self):
        return self.__height__+self.line_width+self.Top_left[1]-1
    
    def get_SVG_header(self):
        if self.Show_header:
            rect_obj = rectangle()
            rect_obj.top_left = self.Top_left
            BR=[self.Header_width+self.Top_left[0],self.__height__]
            rect_obj.bottom_right = BR
            rect_obj.background = self.Header_background
            rect_obj.border_color = self.Header_border_color
            rect_obj.line_width = self.line_width
            Text = draw_rec(rect_obj)
            Text += SVG_text(self.Top_left, self.__font_size__, self.__height__, self.text, 
                             self.font_color, self.font_weight, font_family=self.font_family)
            return Text 
        else:
            return ""

class Table_rows(SVG_Text_obj):
    #__Count__=0
    def __init__(self, font_size=12, line_width=1, top_left=(0,0), text_list=[], width=100, font_color=(0,0,0), background=(255,255,255), border_color=(0,0,0),font_family="Arial"):
        """Initiailize"""
        super().__init__("", font_size, font_color, "normal", line_width, top_left, font_family)
        self.row_width = width
        self.__column_locations__ = [0]

        self.__text_list__ = self.check_text_list(text_list)
        self.Show_rows = len(self.__text_list__)>0
        self.__count__ = 0
        self.set_count(self.__count__)
        self.row_border_color = self.check_color(border_color)
        self.row_background = self.check_color(background)
        self.x_shift=0
        
 
    def check_text_list(self, text_list=[]):
        """This method validates that every element in the text_list is a list of equal lenght"""
        try:
            if len(text_list)>0:
                check_len = len(text_list[0])
                same_size = not(sum([len(x)!=check_len for x in text_list]))
                assert(same_size==True)
        except:
            raise(RuntimeError("Every row must be a list containing the same number of elements"))
        return text_list
    
    @property
    def column_locations(self):
        return [location-self.Top_left[0] for location in self.__column_locations__]
    
    @column_locations.setter
    def column_locations(self, locations):
        locations = [local+self.Top_left[0] for local in locations]
        self.__set_column_locations__(locations)
    
    @property
    def bottom(self):
        return (self.line_width+self.__height__)*self.__count__+self.Top_left[1]
    
    def set_text_list(self, text_list):
        """This method first validates the text_list then sets the internal text_list and updates 
           the row count."""
        self.__text_list__ = self.check_text_list(text_list)
        self.set_count(self.__count__)
        try:
            if self.column_locations[0]<0:
                self.column_locations=[0]
        except:
            self.column_locations=[0]
        self.Show_rows = True
    
    def set_count(self, count):
        """This method lets you add rows beyond the lenght of the text_list."""
        try:
            assert(count>=0 and int(count)==count)
        except:
            raise(RuntimeError("The row count must be a postive integer"))
        self.__count__ = max(count,len(self.__text_list__))
        self.Show_rows = True
    
    def __set_column_locations__(self, locations=[0]):
        """This method sets the vertical dividers and text placement of the columns in the table."""
        try:
            assert(max(locations)<=self.row_width+self.Top_left[0])
            assert(min(locations)>=0)#+self.Top_left[0]>=0)
            if len(locations)<len(self.__text_list__[0]):
                more = len(self.__text_list__[0])-len(locations)
                step = 10
                start = locations[-1]+step
                stop = more*step+locations[-1]
                locations+=list(range(start, stop, step))
            self.__column_locations__=locations
        except:
            print(locations)
            raise(RuntimeError("Column locations must all be greater than or equal to zero and be less than or equal to the row width."))
        
    def get_SVG_rows(self):
        if self.Show_rows:
            try:
                columns = len(self.__text_list__[0])
            except:
                columns = 1
            TL = list(self.Top_left)
            #self.check_height(self.__font_size__, self.line_width)            
            row_height=self.__height__+self.__count__*self.line_width

            BR = [self.row_width+TL[0],row_height]
            rect_obj = rectangle()
            rect_obj.top_left = TL
            rect_obj.bottom_right = BR
            rect_obj.background = self.row_background
            rect_obj.border_color = self.row_border_color
            rect_obj.line_width = self.line_width
            Text = ""
            
            for row in range(self.__count__):
                #Text += draw_rec(rect_obj)
                try:
                    row_text = self.__text_list__[row]
                    #this is to check for a minimum number of column locations
                    if len(self.column_locations)<len(row_text):
                        print("column_locations are not set, using defaults")
                        self.column_locations = list(range(0,(len(row_text))*20,20))
                        #print(self.column_locations)
                    #print(column_count)
                    for self.text in row_text: #Set row height to the height of the tallest entry in that row
                        self.__height__=self.check_height(self.__font_size__, self.line_width, self.__height__)     
                    row_height=self.__height__+self.__count__*self.line_width
                    BR[1]=row_height
                    rect_obj.bottom_right = BR
                    Text += draw_rec(rect_obj)
                    Top_left = list(TL)
                    for self.text, x_local in zip(row_text, self.__column_locations__):
                        if x_local<TL[0]:
                            print(x_local)
                        Top_left[0]=x_local
                        Text += SVG_text(Top_left, self.__font_size__, row_height, self.text, 
                                         self.font_color, self.font_weight, self.x_shift, self.font_family)
                except: #there was no row text so draw an empty rectangle
                    Text += draw_rec(rect_obj)
                TL[1]+=row_height
            bottom = TL[1]+self.line_width
            top = self.Top_left[1]+self.line_width
            
            for hor_local in self.__column_locations__:
                if hor_local<=TL[0]:
                    continue
                line = '<line x1="{0}" y1="{1}" x2="{0}" y2="{2}" '.format(hor_local, top, bottom)
                line +='style="stroke:rgb{0}; stroke-width:{1}"/>\n'.format(self.row_border_color, self.line_width)
                Text+=line
            return Text 
        else:
            return ""


def clean_text(text):
    """This function replaces problem characters with HTML friendly characters """
    if '<' in text or '>' in text: #allow for the display of <n> and <tab>
        text = text.replace('<','&lt;')#'&#60')
        text = text.replace('>','&gt;')#'&#62')
    if '$' in text: #ensure that $ renders as a $
        #$ will render correctly when viewed in a browser but not
        #using IPython.display.HTML
        pass
    #text=text.replace(" ",'&nbsp')
    text= text.strip('\b')
    return text
