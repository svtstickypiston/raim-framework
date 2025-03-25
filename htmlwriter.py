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
    f = open("./index.txt")

    body = f.read()

    target.write(body)
    f.close()

    for entry in os.scandir("./pillars"):  
        if entry.is_dir():  # check if it's a folder
            path = entry.path + "/description.json"
            jf = open(path)

            data = json.load(jf)
            id = data['pillar_id']
            name = data['name']
            brief = data['brief']
            imgpath = data['imagepath']

            html = '\
            <section id="features-1" class="container my-4">\
                <h3>Pillar '+str(id)+': '+name+'</h3>\
                <p>'+brief+'</p>\
                <div id="'+str(id)+'" class="card-deck">\
            '

            for entry in os.scandir(entry.path):  
                if entry.is_file() and entry.path.endswith('description.json')==False:  # check if it's a file, and that it isn't the pillar description
                    card_file = open(entry.path)

                    card_data = json.load(card_file)
                    name = card_data['feature_name']
                    brief = card_data['feature_brief']
                    pillarid = str(card_data['pillar_id'])
                    number = str(card_data['feature_num'])
                    facet = card_data['facet']
                    body = card_data['feature_long']

                    html += '\
                    <div class="card">\
                        <img class="card-img-top" src="assets'+imgpath+'">\
                        <div class="card-body">\
                            <h5 class="card-title">'+name+'</h5>\
                            <p class="card-text">'+brief+'</p>\
                        </div>\
                        <div class="card-footer d-flex w-100 justify-content-between">\
                            <small class="text-muted">Feature '+pillarid+'-'+number+'</small>\
                            <small class="text-muted">'+facet+'</small>\
                        </div>\
                    </div>\
                    <div class="popup">\
                        <div class="popup-content">\
                            <span class="close-button">&times;</span>\
                            <h2>'+name+'</h2>\
                            <p>'+body+'</p>\
                        </div>\
                    </div>\
                    '

            html += '\
                </div>\
            <!-- End Card Group -->\
            </section>\
            <div class="section-divider"></div>\
            '

            target.write(html+"\n")
            jf.close()

# creates the features for the pillar pages
def createFeatures (pillar, target):
    directory = "./pillars/"+pillar
    
    descriptions = open(directory+'/description.json')

    pillardata = json.load(descriptions)
    id = pillardata['pillar_id']
    name = pillardata['name']
    brief = pillardata['brief']
    tagline = pillardata['tagline']
    body = pillardata['description']
    # imgpath = pillardata['imagepath']

    html_1 = '\n\
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

    for entry in os.scandir(directory):  
        if entry.is_file()  and entry.path.endswith('description.json')==False:  # check if it's a file
            f = open(entry.path)
            print(entry.path)

            data = json.load(f)

            name = data['feature_name']
            brief = data['feature_brief']
            pillarid = str(data['pillar_id'])
            number = str(data['feature_num'])
            facet = data['facet']
            usecase = data['feature_use_case']
            summary = data['feature_summary']

            html_2 = '\
                <div class="expandable_card_wrapper">\
                <div class="expandable_card">\
                    <div class = "expandable_icon">\
                        <ion-icon name="chevron-down-outline"></ion-icon>\
                    </div>\
                    <h5 class="expandable_title">'+name+'</h5>\
                    <p class="expandable_body">'+brief+'</p>\
                    <div class="expandable_footer">\
                        <small class="text-muted">Feature '+pillarid+'-'+number+'</small>\
                        <small class="text-muted">'+facet+'</small>\
                    </div>\
                </div>\
                <div class="expandable_content_wrapper">\
                    <div class="expandable_content">\
                        <p>'+summary+'</p>\
                        <p>'+usecase+'</p>\
                    </div>\
                </div>\
                </div>\
            '

            target.write(html_2+"\n")

    target.write('</section><div class="section-divider mb-0"></div>\n')
    f.close()

def createWebsite():
    dir = './root'

    index = open(dir+'/index.html', 'a')
    index.truncate(0)

    createHeader(index)
    createIndex(index)
    createFooter(index)

    index.close()
    
    for entry in os.scandir(dir):  
        if entry.is_file() and re.search('pillars-[0-9].html', entry.path)!=None:  # look for pillar files
            f = open(entry.path, 'a')
            f.truncate(0)

            templist = re.findall('[0-9]', entry.path)
            pillarnum = templist[len(templist)-1]
            pillar = 'pillar_'+pillarnum
    
            createHeader(f)
            createFeatures(pillar, f)
            createFooter(f)

            f.close()

createWebsite()
