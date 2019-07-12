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
