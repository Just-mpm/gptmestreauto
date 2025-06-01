"""
Fallback implementation for networkx when not available
Provides basic graph functionality
"""
from typing import Dict, List, Set, Any, Optional, Tuple
import random

class FallbackGraph:
    """Simple graph implementation as fallback for networkx.Graph"""
    
    def __init__(self):
        self.nodes_dict: Dict[Any, Dict] = {}
        self.edges_dict: Dict[Tuple, Dict] = {}
        self.adjacency_dict: Dict[Any, Set] = {}
    
    def add_node(self, node: Any, **attr):
        """Add a node with optional attributes"""
        if node not in self.nodes_dict:
            self.nodes_dict[node] = {}
            self.adjacency_dict[node] = set()
        self.nodes_dict[node].update(attr)
    
    def add_edge(self, u: Any, v: Any, **attr):
        """Add an edge between two nodes"""
        # Ensure nodes exist
        self.add_node(u)
        self.add_node(v)
        
        # Add edge
        edge_key = (u, v) if u <= v else (v, u)
        self.edges_dict[edge_key] = attr
        
        # Update adjacency
        self.adjacency_dict[u].add(v)
        self.adjacency_dict[v].add(u)
    
    def remove_node(self, node: Any):
        """Remove a node and all its edges"""
        if node in self.nodes_dict:
            # Remove all edges connected to this node
            for neighbor in list(self.adjacency_dict[node]):
                self.remove_edge(node, neighbor)
            
            # Remove node
            del self.nodes_dict[node]
            del self.adjacency_dict[node]
    
    def remove_edge(self, u: Any, v: Any):
        """Remove an edge between two nodes"""
        edge_key = (u, v) if u <= v else (v, u)
        if edge_key in self.edges_dict:
            del self.edges_dict[edge_key]
            self.adjacency_dict[u].discard(v)
            self.adjacency_dict[v].discard(u)
    
    def nodes(self, data: bool = False):
        """Return nodes, optionally with data"""
        if data:
            return list(self.nodes_dict.items())
        return list(self.nodes_dict.keys())
    
    def edges(self, data: bool = False):
        """Return edges, optionally with data"""
        if data:
            return [(u, v, attr) for (u, v), attr in self.edges_dict.items()]
        return [edge for edge in self.edges_dict.keys()]
    
    def neighbors(self, node: Any):
        """Return neighbors of a node"""
        return list(self.adjacency_dict.get(node, set()))
    
    def number_of_nodes(self) -> int:
        """Return number of nodes"""
        return len(self.nodes_dict)
    
    def number_of_edges(self) -> int:
        """Return number of edges"""
        return len(self.edges_dict)
    
    def has_node(self, node: Any) -> bool:
        """Check if node exists"""
        return node in self.nodes_dict
    
    def has_edge(self, u: Any, v: Any) -> bool:
        """Check if edge exists"""
        edge_key = (u, v) if u <= v else (v, u)
        return edge_key in self.edges_dict
    
    def degree(self, node: Any = None):
        """Return degree of node(s)"""
        if node is not None:
            return len(self.adjacency_dict.get(node, set()))
        return {n: len(adj) for n, adj in self.adjacency_dict.items()}

class FallbackDiGraph(FallbackGraph):
    """Simple directed graph implementation"""
    
    def __init__(self):
        super().__init__()
        self.in_adjacency_dict: Dict[Any, Set] = {}
        self.out_adjacency_dict: Dict[Any, Set] = {}
    
    def add_node(self, node: Any, **attr):
        """Add a node with optional attributes"""
        super().add_node(node, **attr)
        if node not in self.in_adjacency_dict:
            self.in_adjacency_dict[node] = set()
            self.out_adjacency_dict[node] = set()
    
    def add_edge(self, u: Any, v: Any, **attr):
        """Add a directed edge from u to v"""
        # Ensure nodes exist
        self.add_node(u)
        self.add_node(v)
        
        # Add edge (directed)
        edge_key = (u, v)
        self.edges_dict[edge_key] = attr
        
        # Update adjacency (directed)
        self.out_adjacency_dict[u].add(v)
        self.in_adjacency_dict[v].add(u)
    
    def predecessors(self, node: Any):
        """Return predecessors of a node"""
        return list(self.in_adjacency_dict.get(node, set()))
    
    def successors(self, node: Any):
        """Return successors of a node"""
        return list(self.out_adjacency_dict.get(node, set()))

class FallbackNetworkX:
    """Fallback networkx-like interface"""
    
    def __init__(self):
        self.Graph = FallbackGraph
        self.DiGraph = FallbackDiGraph
    
    def shortest_path(self, G, source: Any, target: Any = None):
        """Simple shortest path using BFS"""
        if target is None:
            # Return paths to all nodes
            return self._all_shortest_paths(G, source)
        
        # BFS for single target
        if not G.has_node(source) or not G.has_node(target):
            return []
        
        if source == target:
            return [source]
        
        queue = [(source, [source])]
        visited = {source}
        
        while queue:
            node, path = queue.pop(0)
            
            for neighbor in G.neighbors(node):
                if neighbor == target:
                    return path + [neighbor]
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return []  # No path found
    
    def _all_shortest_paths(self, G, source: Any):
        """BFS to find shortest paths to all reachable nodes"""
        if not G.has_node(source):
            return {}
        
        paths = {source: [source]}
        queue = [(source, [source])]
        visited = {source}
        
        while queue:
            node, path = queue.pop(0)
            
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    paths[neighbor] = new_path
                    queue.append((neighbor, new_path))
        
        return paths
    
    def connected_components(self, G):
        """Find connected components using DFS"""
        visited = set()
        components = []
        
        for node in G.nodes():
            if node not in visited:
                component = set()
                stack = [node]
                
                while stack:
                    current = stack.pop()
                    if current not in visited:
                        visited.add(current)
                        component.add(current)
                        stack.extend(n for n in G.neighbors(current) if n not in visited)
                
                components.append(component)
        
        return components
    
    def pagerank(self, G, alpha: float = 0.85, max_iter: int = 100):
        """Simple PageRank implementation"""
        nodes = list(G.nodes())
        if not nodes:
            return {}
        
        # Initialize PageRank values
        pagerank = {node: 1.0 / len(nodes) for node in nodes}
        
        for _ in range(max_iter):
            new_pagerank = {}
            
            for node in nodes:
                rank = (1.0 - alpha) / len(nodes)
                
                for neighbor in G.neighbors(node):
                    out_degree = len(G.neighbors(neighbor))
                    if out_degree > 0:
                        rank += alpha * pagerank[neighbor] / out_degree
                
                new_pagerank[node] = rank
            
            pagerank = new_pagerank
        
        return pagerank
    
    def betweenness_centrality(self, G):
        """Simple betweenness centrality calculation"""
        nodes = list(G.nodes())
        centrality = {node: 0.0 for node in nodes}
        
        for source in nodes:
            paths = self._all_shortest_paths(G, source)
            
            for target, path in paths.items():
                if len(path) > 2:  # Only consider paths with intermediate nodes
                    for intermediate in path[1:-1]:
                        centrality[intermediate] += 1.0
        
        # Normalize
        n = len(nodes)
        if n <= 2:
            return centrality
        
        norm = 2.0 / ((n - 1) * (n - 2))
        for node in centrality:
            centrality[node] *= norm
        
        return centrality

def get_fallback_networkx() -> FallbackNetworkX:
    """Get fallback networkx instance"""
    return FallbackNetworkX()

# Create global instances for compatibility
fallback_nx = get_fallback_networkx()
Graph = fallback_nx.Graph
DiGraph = fallback_nx.DiGraph
shortest_path = fallback_nx.shortest_path
connected_components = fallback_nx.connected_components
pagerank = fallback_nx.pagerank
betweenness_centrality = fallback_nx.betweenness_centrality