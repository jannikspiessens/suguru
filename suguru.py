import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

def PDFparsermed(volume, book):

  NUM_PAGES = 4
  SIZE = 8
  CORNERS = (((25, 463), (277, 715)),
              ((313, 463), (565, 715)),
              ((25, 130), (277, 382)),
              ((312, 130), (565, 382)))
  CELLWIDTH = (CORNERS[0][1][0] - CORNERS[0][0][0]) / SIZE
  try:
    fd = open("krazydad/medium/{}/{}.pdf".format(volume, book), "rb")
  except:
    return None
  viewer = SimplePDFViewer(fd)

  for i in range(1, NUM_PAGES+1):
    viewer.navigate(i)
    viewer.render()
    text = viewer.canvas.text_content
    #open('{}.txt'.format(book), 'a+').write(text)
    puzzles = viewer.canvas.text_content.split('Suguru #')[1:]

    for k in range(len(puzzles)):
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
      groupsflat = set()
      i = 0
      for y in range(SIZE):
        for x in range(SIZE):
          new = set()
          rightupper = [CORNERS[k][0][0] + (x+1)*CELLWIDTH, CORNERS[k][1][1] - y*CELLWIDTH]
          leftlower = [CORNERS[k][0][0] + x*CELLWIDTH, CORNERS[k][1][1] - (y+1)*CELLWIDTH]

          # if next edge is right edge of this coord
          if i < len(edges) and edges[i][0] == rightupper:
            i += 1
          elif (x+1, y) in groups:
            new = set(groups[(x+1, y)])
          elif x+1 < SIZE:
            new.add((x+1, y))

          # if next edge is lower edge of this coord
          if i < len(edges) and edges[i][0] == leftlower:
            i += 1
          elif (x, y+1) in groups:
            new.update(groups[(x, y+1)])
          elif y+1 < SIZE:
            new.add((x, y+1))
          
          if (x, y) in groups:
            groups[(x, y)] |= frozenset(new)
            group = groups[(x, y)]
            for coord in new:
              groups[coord] = group
          else:
            group = frozenset(new) | frozenset([(x, y)])
            for coord in group:
              groups[coord] = group
          
          newgroup = True
          for groupflat in groupsflat:
            if len(groupflat & group) != 0:
              groupsflat.remove(groupflat)
              groupsflat.add(group)
              newgroup = False
              break
          if newgroup: groupsflat.add(group)
      
      f = open('readable_data/medium/{}-{}.txt'.format(volume, book), 'w')
      f.write(str(given))
      f.write('\n')
      f.write(str(groupsflat).replace('), f', ', f').replace('frozenset(', ''))
      f.write('\n')
      f.close()
      break

    fd.close()
    break

if __name__ == "__main__":
  PDFparsermed(1, 1)
