import json
import os
import re

# creates the html head, as well as the navigation ribbon at the top of each page
def createHeader (target):
    f = open("./header.txt")
    header = f.read()

    target.write(header)
    f.close()

# creates all common content at the bottom of the page
def createFooter (target):
    f = open("./footer.txt")
    footer = f.read()

    target.write(footer)
    f.close()

# creates the body for the index file
def createIndex (target):

    # write the initial part for the index page
    f = open("./index.txt")
    body = f.read()
    target.write(body)
    f.close()

    # load the feature cards from JSON files
    for entry in os.scandir("./pillars"):  
        if entry.is_dir():  # check for folders
            # navigate to the JSON folder for the pillar descriptions
            path = entry.path + "/description.json"
            pillar_description = open(path)

            # load data from JSON file
            data = json.load(pillar_description)
            id = data['pillar_id']
            name = data['name']
            brief = data['brief']
            imgpath = data['imagepath']

            # begin the card deck for each pillar
            html = '\n\
            <!-- Card Deck -->\n\
            <section id="features-1" class="container my-4">\n\
                <h3>Pillar '+str(id)+': '+name+'</h3>\n\
                <p>'+brief+'</p>\n\
                <div id="'+str(id)+'" class="card-deck">\n\
            '

            # load JSON data for individual features from the relevant pillar
            for entry in os.scandir(entry.path):  
                if entry.is_file() and entry.path.endswith('description.json')==False:  # check if it's a file, and that it isn't the pillar description
                    card_file = open(entry.path)

                    # load data from JSON file
                    card_data = json.load(card_file)
                    name = card_data['feature_name']
                    brief = card_data['feature_brief']
                    pillarid = str(card_data['pillar_id'])
                    number = str(card_data['feature_num'])
                    facet = card_data['facet']
                    body = card_data['feature_long']

                    # add each individual card based on JSON data
                    html += '\n\
                    <!-- Feature Card -->\n\
                    <div class="card">\n\
                        <img class="card-img-top" src="assets'+imgpath+'">\n\
                        <div class="card-body">\n\
                            <h5 class="card-title">'+name+'</h5>\n\
                            <p class="card-text">'+brief+'</p>\n\
                        </div>\n\
                        <div class="card-footer d-flex w-100 justify-content-between">\n\
                            <small class="text-muted">Feature '+pillarid+'-'+number+'</small>\n\
                            <small class="text-muted">'+facet+'</small>\n\
                        </div>\n\
                    </div>\n\
                    <div class="popup">\n\
                        <div class="popup-content">\n\
                            <span class="close-button">&times;</span>\n\
                            <h2>'+name+'</h2>\n\
                            <p>'+body+'</p>\n\
                        </div>\n\
                    </div>\n\
                    '

            # end each card deck
            html += '\n\
                </div>\n\
            <!-- End Card Deck -->\n\
            </section>\n\
            <div class="section-divider"></div>\n\
            '

            target.write(html+"\n")
            pillar_description.close()

# creates the features for the pillar pages
def createFeatures (pillar, target):
    # navigate to the JSON folder for the pillar descriptions
    dir = "./pillars/"+pillar
    descriptions = open(dir+'/description.json')

    # load data from JSON file
    pillardata = json.load(descriptions)
    id = pillardata['pillar_id']
    name = pillardata['name']
    brief = pillardata['brief']
    tagline = pillardata['tagline']
    body = pillardata['description']
    # imgpath = pillardata['imagepath']

    # writes the introduction to each pillar
    html_1 = '\n\
        <!-- Pillar introduction -->\n\
        <main role="main">\n\
        <!-- Hero Section -->\n\
        <section id="hero" class="jumbotron">\n\
            <div id="title-wrapper" class="container">\n\
            <div id="title">\n\
                <h1 class="display-4 text-body-emphasis">'+name+'</h1>\n\
                <p class="lead">'+tagline+'</p>\n\
            </div>\n\
            </div>\n\
        </section>\n\
        <!-- Features Section -->\n\
        <section id="features" class="container my-4">\n\
          <h2>Background Information</h2>\n\
          <!-- Write about background information -->\n\
            <p>'+brief+'</p>\n\
            <p>'+body+'</p>\n\
        </section>\n\
        <div class="section-divider"></div>\n\
        <pre id="output"></pre>\n\
        <!-- Start Card Group -->\n\
        <section class="container my-4">\n\
          <h3>Features for Pillar '+str(id)+': '+name+'</h3>\n\
        <div class="expandable_section">\n\
    '

    target.write(html_1+"\n")

    # gets data from the features for that pillar
    for entry in os.scandir(dir):  
        if entry.is_file()  and entry.path.endswith('description.json')==False:  # check if it's a file
            f = open(entry.path)
            print(entry.path)

            # load data from JSON file
            data = json.load(f)
            name = data['feature_name']
            brief = data['feature_brief']
            pillarid = str(data['pillar_id'])
            number = str(data['feature_num'])
            facet = data['facet']
            usecase = data['feature_use_case']
            summary = data['feature_summary']

            # creates an expandable section for each feature
            html_2 = '\n\
                <!-- Expandable section -->\n\
                <div class="expandable_card_wrapper">\n\
                <div class="expandable_card">\n\
                    <div class = "expandable_icon">\n\
                        <ion-icon name="chevron-down-outline"></ion-icon>\n\
                    </div>\n\
                    <h5 class="expandable_title">'+name+'</h5>\n\
                    <p class="expandable_body">'+brief+'</p>\n\
                    <div class="expandable_footer">\n\
                        <small class="text-muted">Feature '+pillarid+'-'+number+'</small>\n\
                        <small class="text-muted">'+facet+'</small>\n\
                    </div>\n\
                </div>\n\
                <div class="expandable_content_wrapper">\n\
                    <div class="expandable_content">\n\
                        <p>'+summary+'</p>\n\
                        <p>'+usecase+'</p>\n\
                    </div>\n\
                </div>\n\
                </div>\n\
            '

            target.write(html_2+"\n")

    # finish the section
    target.write('</section><div class="section-divider mb-0"></div>\n')
    f.close()

# main function that runs everything else
def createWebsite():
    dir = '.'

    # open and clear the index.html file
    index = open(dir+'/index.html', 'a')
    index.truncate(0)

    # create a new index.html file
    createHeader(index)
    createIndex(index)
    createFooter(index)

    index.close()
    
    # for every pillars-x.html file, it opens and clears it, before creating a new one from the JSON data in the relevant file directory
    for entry in os.scandir(dir):  
        if entry.is_file() and re.search('pillars-[0-9].html', entry.path)!=None:  # look for pillar files
            # open and clear the pillars-x.html file
            f = open(entry.path, 'a')
            f.truncate(0)

            # get the correct folder for each pillars-x.html file
            templist = re.findall('[0-9]', entry.path)
            pillarnum = templist[len(templist)-1]
            pillar = 'pillar_'+pillarnum
    
            # create a new pillars-x.html file
            createHeader(f)
            createFeatures(pillar, f)
            createFooter(f)

            f.close()

createWebsite()
