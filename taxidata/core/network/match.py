import networkx as nx
import numpy as np
from ..object import taxiarray, trajectory, Dataset

def segment_length(G, segment):
    """return segment or edge iteration length

    Parameters
    ----------
    G : MultiDiGraph

    segment : list
        ex) [(1, 2, 0),(2, 6, 0), ...]
    Returns
    -------
    float
        segment length
    """
    segment_length = 0
    for i in range(len(segment)):
        segment_length += G.get_edge_data(segment[i][0],segment[i][1])[0]['length']
    return segment_length

def stitch_score(G, segment_start_edgelist, segment_next_edgelist):
    """return stitch score between two segments.

    Parameters
    ----------
    G : MultiDiGraph

    segment_start_edgelist : list
        ex) [(1, 2, 0),(2, 6, 0), ...]
    segment_next_edgelist : list
        ex) [(1, 2, 0),(2, 6, 0), ...]

    Returns
    -------
    float
        stitch score
    """

    if segment_next_edgelist[0] in segment_start_edgelist:
        start_overlap = segment_start_edgelist.index(segment_next_edgelist[0])   ## segment_2와 겹치는 segment_1의 시작부분
        end_overlap = segment_start_edgelist.index(segment_next_edgelist[-1])    ## segment_2와 겹치는 segment_1의 끝부분

        ## overlap length of segment
        overlap_length = 0
        for i in np.linspace(start_overlap, end_overlap, end_overlap-start_overlap+1):
            overlap_length += segment_length(G, [segment_start_edgelist[int(i)]])

        ## total length of segment
        total_length = segment_length(G, segment_start_edgelist) + segment_length(G, segment_next_edgelist) - overlap_length
        stitch_score = 1-overlap_length/total_length
    ## no overlap
    else: stitch_score = 1
    return stitch_score
