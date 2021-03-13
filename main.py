import json

#Stellt einen Quader dar
class Quader:
    #Construktor
    def __init__(self, x, y, z, w, h, d, index = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.h = h
        self.d = d
        self.index = index
    
    #Überlappt dieser Quader mit dem gegebenen Quader?
    def overlaps(self, other):
        if self.x >= other.x and self.x < other.x + other.w:
            if self.y >= other.y and self.y < other.y + other.h:
                if self.z >= other.z and self.z < other.z + other.d:
                    return True
        
        if other.x >= self.x and other.x < self.x + self.w:
            if other.y >= self.y and other.y < self.y + self.h:
                if other.z >= self.z and other.z < self.z + self.d:
                    return True
        
        return False
    
    #Passt dieser Quader in den übergebenen hinein?
    def fits_inside(self, other):
        return self.w <= other.w and self.h <= other.h and self.d <= other.d
    
    #Ist dieser Qader vollständig innerhalb des übergebenen Quaders?
    def is_inside(self, other):
        if self.x >= other.x and self.x + self.w <= other.x + other.w:
            if self.y >= other.y and self.y + self.h <= other.y + other.h:
                if self.z >= other.z and self.z + self.d <= other.z + other.d:
                    return True
        return False
    
    #Für schönere Ausgabe
    def print(self):
        print(f"Quader: pos: {self.x}, {self.y}, {self.z} dim: {self.w}, {self.h}, {self.d}")
    
    #Erzeugt einen neuen identischen Quader
    def clone(self):
        return Quader(self.x, self.y, self.z, self.w, self.h, self.d, self.index)

#Objekt um ein Paket dar zustellen
class Package:
    #Constructor
    def __init__(self, dimensions, cost = 0, type = 0):
        self.dimensions = dimensions
        self.articles = []
        self.cost = cost
        self.type = type
    
    #Leeres identisches Package erstellen
    def clone(self):
        return Package(Quader(self.dimensions.x, self.dimensions.y, self.dimensions.z, self.dimensions.w, self.dimensions.h, self.dimensions.d), self.cost, self.type)
    
    #Versucht einen Artikel im Package zu platzieren
    def put(self, new_article):
        article = new_article.clone()
        if not article.fits_inside(self.dimensions):
            return False
        for x in range(self.dimensions.w - article.w + 2):
            for y in range(self.dimensions.h - article.h + 2):
                for z in range(self.dimensions.d - article.d + 2):
                    article.x = x
                    article.y = y
                    article.z = z
                    if not self.collision(article):
                        self.articles.append(article)
                        return True
        return False
    
    #Überprüft auf Kollisionen des übergebenen Artickels mit bereits platzierten Artikeln
    def collision(self, article):
        if not article.is_inside(self.dimensions):
            return True
        for i in self.articles:
            if i.overlaps(article):
                return True
        return False
    
    #Für schönere Ausgabe
    def print(self):
        print(f"Package w: {self.dimensions.w}, h: {self.dimensions.h}, d: {self.dimensions.d}, cost: {self.cost}")
        
        for i in self.articles:
            print(f"Article: x: {i.x}, y: {i.y}, z: {i.z}, w: {i.w}, h: {i.h}, d: {i.d}")


solutions = []

#Probiert durch Rekursion verschiedene Packungsmöglichkeiten aus und legt sie in Solutions ab.

def pack(package_types, packages, articles):
    global solutions

    if len(articles) == 0:
        solutions.append(packages)
        return

    all_remains = []
    package_alternatives = []

    for t in package_types:
        p = t.clone()
        remaining = []

        for a in articles:
            if not p.put(a):
                remaining.append(a)

        #Übrige Artikel merken
        all_remains.append(remaining)
        #Packages mit platzierten Artikeln merken
        package_alternatives.append(p)
    
    for i in range(len(package_alternatives)):
        if len(package_alternatives[i].articles) != 0:
            #Rekursion für alle Paketarten weiterführen -> bereits gefüllte Pakete mitnehmen und nur übrige Artikel im nächsten Durchgang beachten.
            pack(package_types, packages + [package_alternatives[i]], all_remains[i])


def sum_package_costs(package_list):
    costs = 0
    for p in package_list:
        costs += p.cost
    return costs

def parse_from_json_input(json_input):
    jobj = json.loads(json_input)

    #Artikel parsen
    articles = []

    index = 0

    for i in jobj.get("articles"):
        articles.append(Quader(0, 0, 0, i[0], i[1], i[2], index))
        index += 1
    
    #Paketarten parsen
    package_types = []

    index = 0

    for e in jobj.get("package_types"):
        dims = e.get("dimensions")
        cost = e.get("cost")

        package_types.append(Package(Quader(0, 0, 0, dims[0], dims[1], dims[2]), cost, index))

        index += 1
    
    return articles, package_types


def get_json_response(package_list):
    response_dict = {}
    index_list = []
    articles_list = []

    pack_num = 0
    for p in package_list:
        index_list.append(p.type)

        for a in p.articles:
            #Paketnummer merken
            articles_list.append({"article":a, "package":pack_num})
        pack_num += 1
    
    #Artikel in die originale Reihenfolge bringen
    articles_list.sort(key = lambda e: e["article"].index)

    final_list = []

    for o in articles_list:
        x = o["article"].x
        y = o["article"].y
        z = o["article"].z
        final_list.append([o["package"], x, y, z])

    response_dict["used_packages"] = index_list
    response_dict["article_positions"] = final_list

    json_response = json.dumps(response_dict)

    return json_response




def handle_request(json_input):
    global solutions

    articles, package_types = parse_from_json_input(json_input)

    #Überprüfen ob die Pakete groß genug für alle Artikel sind
    for a in articles:
        fits = False
        for p in package_types:
            if a.fits_inside(p.dimensions):
                fits = True
        if not fits:
            #Es gibt Artikel die zu groß für jede Paketart sind
            return None

    #Alle Packmöglichkeiten notieren
    pack(package_types, [], articles)

    #Solutions nach Kosten sortieren
    solutions.sort(key = lambda e: sum_package_costs(e))

    #Das erste Element hat die geringsten Kosten
    best_solution = solutions[0]

    response = get_json_response(best_solution)

    return response


from http.server import BaseHTTPRequestHandler, HTTPServer

class PackageRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        content_length = int(self.headers["Content-Length"])

        json_query = self.rfile.read(content_length).decode()

        try:
            response = handle_request(json_query)
        except:
            info_text = "400: malformed request -> bad json object"

            self.send_response(400)
            self.wfile.write(info_text.encode())

            print(info_text)
        else:
            print("handling request")

            if response == None:
                info_text = "405: invalid input -> articles too big for packages"
                
                self.send_response(405)
                self.wfile.write(info_text.encode())

                print(info_text)
            else:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                self.wfile.write(response.encode())

                print("200 Ok")

            print("response sent")

if __name__ == "__main__":
    import sys

    port = 80

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except:
            print("Port has to be an Integer. Using default port (80).")
    
    myServer = HTTPServer(("", port), PackageRequestHandler)
    print(f"Server started on port {port}.")

    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass

    myServer.server_close()
    print("Server closed.")