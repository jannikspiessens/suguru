import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

def PDFparsermed(volume, book):

    NUM_PAGES = 4
    SIZE = 8
    CORNERS = (((25, 463), (277, 715)),     # ((xmin, ymin), (xmax, ymax)) for every puzzle
                ((313, 463), (565, 715)),
                ((25, 130), (277, 382)),
                ((313, 130), (565, 382)))
    CELLWIDTH = (CORNERS[0][1][0] - CORNERS[0][0][0]) / SIZE

    fd = open("../data/pdf/medium_{}_{}.pdf".format(volume, book), "rb")
    viewer = SimplePDFViewer(fd)

    for p in range(1, NUM_PAGES+1):
        viewer.navigate(p)
        viewer.render()
        text = viewer.canvas.text_content
        open('{}.txt'.format(book), 'a+').write(text)
        puzzles = viewer.canvas.text_content.split('Suguru #')[1:]

        for k in range(len(puzzles)):
            puzzle = (p-1)*4+k+1
            f = open('../data/sugurus/medium_{}_{}_{}.sug'.format(volume, book, puzzle), 'w')

            given = dict()

            for x in puzzles[k].split('/Ft1 23 Tf')[1:]:
                #format of x: '\n223.356 691.375 Td\n(4) Tj\n ET\n BT\n'
                temp = x.split(' ')
                given[(int((float(temp[0][1:])-CORNERS[k][0][0]) / CELLWIDTH), 7 -
                       int((float(temp[1])-CORNERS[k][0][1]) / CELLWIDTH))] = temp[2][-2]

            edges = puzzles[k].split('2.5 w\n1 J\n')[-1].split('{} {} m'.format(CORNERS[k][0][0], CORNERS[k][1][1]))[0]
            #format of edges: 119.500 715 m
            #                 119.500 683.500 l
            #                 88 683.500 m
            #                 119.500 683.500 l
            # made by taking string between '2.5 w\n1 J\n' and '\topleft_coord m'

            edges = [[[float(z) for z in y.split()] for y in x.split(' m\n')] for x in edges.split(' l\n')[:-1]]
            #format of edges: [[[119.5, 715.0], [119.5, 683.5]], ... ]

            groups = dict()
            i = 0
            # uses the fact that edges are ordered top to bottom, left to right, first bottom edge then right edge
            for y in range(SIZE):
                for x in range(SIZE):
                    new = set()
                    leftlower = [CORNERS[k][0][0] + x*CELLWIDTH, CORNERS[k][1][1] - (y+1)*CELLWIDTH]
                    rightupper = [CORNERS[k][0][0] + (x+1)*CELLWIDTH, CORNERS[k][1][1] - y*CELLWIDTH]

                    # if next edge is right edge of this coord
                    if i < len(edges) and edges[i][0] == rightupper:
                        i += 1
                    elif (x+1, y) in groups:
                        new = set(groups[(x+1, y)])
                    elif x+1 < SIZE:
                        new.add((x+1, y))

                    # if next edge is lower edge of this coord
                    if i < len(edges) and edges[i][0] == leftlower and edges[i][1][0] == rightupper[0]:
                        i += 1
                    elif (x, y+1) in groups:
                        new.update(groups[(x, y+1)])
                    elif y+1 < SIZE:
                        new.add((x, y+1))

                    group = frozenset(new) | groups.get((x,y), frozenset([(x,y)]))
                    for coord in group:
                        groups[coord] = group

            #TODO: make groupsflat in previous x-y loop
            groupsflat = set()
            for y in range(SIZE):
                for x in range(SIZE):
                    groupsflat.add(groups[(x,y)])

            f.write(str(given))
            f.write('\n')
            f.write(str(groupsflat).replace('), f', ', f').replace('frozenset(', '')[:-2]+'}')
            f.close()
            print('saved file for volume {}, book {}, puzzle {}'.format(volume, book, puzzle))

if __name__ == "__main__":
    for b in range(3, 4):
        PDFparsermed(1, b)
