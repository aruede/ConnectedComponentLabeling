import numpy as np

class Lmanager:

  def __init__( self, data ):
    # Array with provisional labels
    # (Can be substitutet by dict to save space)
    self.labels_arr = np.zeros_like( data )
    # Equivalence list
    # Index is label, content is corrected label
    self.equi_l = [ 0 ]
    # Label variable
    self.label = 1
    # Object counter
    self.counter = 0
  
  def new_label( self ):
    l = self.label
    self.label += 1
    self.equi_l.append( l )
    self.counter += 1
    return l

  def merge( self, row, col, a, b=None  ):
    if b is None:
      self.labels_arr[row, col] = self.equi_l[ self.labels_arr[a] ]
      self.counter -= 1
    if a is not None and b is not None:
      self.labels_arr[row, col] = min( self.equi_l[ self.labels_arr[a] ], self.equi_l[ self.labels_arr[b] ] )
      self.equi_l[ self.labels_arr[a] ] = self.labels_arr[row, col]
      self.equi_l[ self.labels_arr[b] ] = self.labels_arr[row, col]

  def decision_tree( self, data, row, col ):
    """ 
    Decision Tree
    as presented in
    "Optimizing Connected Component labeling Algorithms"
    by K. Wu at el.
    """
    # If B is in picture and has a hit then assign B's label to E
    if row > 0 and data[row-1, col]:
      self.merge( row, col, (row-1, col) )
    else:
      # Check if C has a hit
      if row > 0 and col < data.shape[1]-1 and data[row-1, col+1]:
        # Check A
        if row > 0 and col > 0 and data[row-1, col-1]:
          self.merge( row, col, (row-1, col+1), (row-1, col-1) )
        else:
          # Check D
          if col > 0 and data[row, col-1]:
            self.merge( row, col, (row-1, col+1), (row, col-1) )
          else:
            self.merge( row, col, (row-1, col+1) )
      else:
        # Check A
        if row > 0 and col > 0 and data[row-1, col-1]:
          self.merge( row, col, (row-1, col-1) )
        else:
          # Check D
          if col > 0 and data[row, col-1]:
            self.merge( row, col, (row, col-1) )
          else:
            self.labels_arr[row, col] = self.new_label()

  def get_nb_clusters( self ):
    """ Returns the number of clusters (# different labels). """
    return len(set(self.equi_l))-1


def cluster_analyzer( equi_l, labels_arr ):
  # Set of labels for all clusters
  labels = set(equi_l)
  # Dictionary containing the the coordinates of all hits in each cluster
  clusters = dict( [(str(l), []) for l in labels] )
  hit_coords = np.transpose( np.nonzero( labels_arr ) )
  for hit in hit_coords:
      clusters[ str(labels_arr[hit[0], hit[1]]) ].append( (hit[0], hit[1]) )

  # Calculate position of each cluster
  for i, cl in enumerate( clusters ):
      cluster_size = len( clusters[cl] )
      if cluster_size == 0:
          continue
      col = np.zeros( cluster_size )
      row = np.zeros( cluster_size )
      for n, hit in enumerate( clusters[cl] ):
          row[n] = hit[0]
          col[n] = hit[1]
      print( "--- cluster " + str(i) + " ---" )
      print( "cluster size: " + str(cluster_size) )
      print( "Center: " + str(np.mean(col)) + ", " + str(np.mean(row)) )
