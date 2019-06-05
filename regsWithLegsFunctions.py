def proc_heading(tag, level):
    """Processes headings and returns an array that contains
    the heading level, heading type, heading name, heading text"""

    headinglevel = level # Retrieves heading level IE: 1 = part
    headingtype = list(tag.get('class'))[0]  # Defines the type of variable by the HTML class
    headingtext = list(tag)[0].get_text()  # Contains the part number etc

    if len(list(tag)) > 1:
        headingdescription = list(tag)[1].get_text()  # Contains the description, if any
    else:
        headingdescription = ''

    headingid = tag.get('id')

    return [[headinglevel, headingtype, headingtext, headingdescription, headingid]]


def proc_marginalnote(tag, level):
    """Processes marginal notes and returns an array that contains
        the heading level, heading type, heading name, heading text"""

    headinglevel = level  # Retrieves heading level IE: 1 = part
    headingtype = tag.get('class')[0]
    headingtext = tag.find(text=True, recursive=False)  # Contains the part number etc
    headingdescription = ''  # Marginal notes do not have associated descriptions
    headingid = tag.get('id')

    return [[headinglevel, headingtype, headingtext, headingdescription, headingid]]

def proc_section(tag, level):
    """Processes section and returns an array that contains
    the heading level, heading type, heading name, heading text"""
    subcode = tag.find(class_="sectionLabel")
    tempitem = tag
    tempitem.strong.extract()

    headinglevel = level  # Retrieves heading level IE: 1 = part
    headingtype = tag.get('class')[0]
    headingtext = subcode.get_text() # Contains the part number etc
    headingdescription = tempitem.get_text()  # Marginal notes do not have associated descriptions
    headingid = subcode.get('id')

    return [[headinglevel, headingtype, headingtext, headingdescription, headingid]]

def proc_subsection(tag, subLevel):
    """<p class='subSection'> have one of the following structures:
    1. SECTION(SUB SECTION) or
    2. (SUB SECTION)
    The differentiation is important as type 1 needs to have the section split out of it in
    the case of a section, the class type will be sectionLabel, subsections will have class lawlabel"""
    outputlist = ['start of list']
    # Check for presence of section label, which is always wrapped in <strong>
    # The definition itself will be tied to the subsection, not the section in this case
    if len(tag.find_all('strong')) == 1:
        sectiontag = tag.find(class_='sectionLabel')

        headinglevel = 6 # subSection
        headingtype = 'sectionLabel'
        headingtext = sectiontag.get_text()
        headingdescription = ""
        headingid = sectiontag.get('id')

        # Generates entry to add too list
        outputlist.append([[headinglevel, headingtype, headingtext, headingdescription, headingid]])

    if len(tag.find_all(class_='lawLabel')) > 0:
        #subTag = tag.find(class_="lawLabel")
        headinglevel = subLevel  # Subsection, this may need to change
        headingtype = 'lawLabel'
        headingtext = tag.get_text()
        headingid = tag.get('id')
        tag.parent # Step up to parent
        headingdescription = tag.find(text=True, recursive=False)


        # Generates entry to add too list
        outputlist.append([[headinglevel, headingtype, headingtext, headingdescription, headingid]])

    del outputlist[0]  # Removes first faux entry

    return outputlist
def proc_provisions(tag):
    """Processes provisions, this is a recursive function as the depth of these
    lists are otherwise unknown"""

    # S1: Check for <li> tag, if present retrieve children
    if tag.name == 'li':
        tag = tag.find_all(recursive=False)

    #Simplification step: skip multi-class tags, this will be refined after testing
    if len(tag.get('class')) == 1:
        # S2: There should only be <p> and <ul> at this point, in the case of <p> scrape contents based on class
        if tag.name == 'p':
            #Subsection processing
            if tag.get('class')[0] == 'Subsection':
                print()

