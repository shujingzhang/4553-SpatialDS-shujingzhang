import sys
#sys.path.append('/usr/local/lib/python3.4/site-packages/')
import math
import graphviz as gv
import functools
import time

"""
@author - shujing zhang	
@date -  September 27 2015
@description - This program does visualize our tree.
"""



"""
@class node - simple kdtree node
@method - __init__: Sets value,children,discriminator
@method - getVals: Return list of items in the node
@method - printNode: Prints items in node for debugging purposes
"""
class node:
    def __init__(self,dim_items=None,disc=None):

        if not dim_items:
            self.dim = 0
            self.dimList = []
        else:
            self.dimList = dim_items
            self.dim = len(self.dimList)

        self.leftChild = None
        self.rightChild = None
        self.disc = disc

    """
    @public
    @method - getVals: Return list of items in the node
    @param void
    @returns list[]: list of items in node
    """
    def getVals(self):
        return self.dimList

    """
    @public
    @method - getDiscValue: Return value based on discriminator
    @param void
    @returns mixed: Item in list
    """
    def getDiscValue(self,val=None):
        if not val == None:
            return self.dimList[val]

        return self.dimList[self.disc]

    """
    @public
    @method - setVals: Set values held in node
    @param vals[]: List of items
    @returns bool: True if successful
    """
    def setVals(self,vals):
        if not len(vals) == self.dim:
            return False
        for i in range(len(vals)):
            self.dimList[i] = vals[i]

        return True


    """
    @public
    @method - printNode: Prints items in node for debugging purposes
    @param void
    @returns void
    """
    def printNode(self):
        if not self.leftChild == None:
            leftVals = ', '.join(map(str, self.leftChild.dimList))
        else:
            leftVals = 'Null'
        if not self.rightChild == None:
            rightVals = ', '.join(map(str, self.rightChild.dimList))
        else:
            rightVals = 'Null'
        pString = ', '.join(map(str, self.dimList))
        pString += "\n"
        pString += "leftChild: " + leftVals+ "\n"
        pString += "rightChild: "  + rightVals + "\n"
        pString += "disc: "  + str(self.disc)
        print(pString)



class kdtree:
    def __init__(self,dim):

        self.root = None
        self.dim = dim

    """
    @public
    @method - insert: Insert value into kdtree
    @param val: item of length dim (where dim = dimension) to place into a node
    @returns {None}:
    """
    def insert(self,val):
        if self._is_iterable(val):
            if self.root == None:
                self.root = node(val,0)
            else:
                newNode = node(val,0)
                currRoot = self.root

                self._recInsert(currRoot,newNode)
                print("===============")
        else:
            print(val)
            print("Whoops: Item must be iterable.")

    """
    @private
    @method - _recInsert: Insert value into kdtree
    @param root: a copy of the root of the tree
    @param node: the new node to be inserted
    @returns bool: true if successful
    """
    def _recInsert(self,root,newNode):
        print(','.join(map(str, newNode.dimList)),' : ',','.join(map(str, root.dimList)))
        print(newNode.getDiscValue(root.disc),' > ',root.getDiscValue(),'?')
        if newNode.getDiscValue(root.disc) > root.getDiscValue():
            print("going right")
            if root.rightChild == None:
                print("inserting right")
                root.rightChild = newNode
                newNode.disc = (root.disc + 1) % self.dim
            else:
                print("rec call right")
                self._recInsert(root.rightChild,newNode)
        else:
            print("going left")
            if root.leftChild == None:
                print("inserting left")
                root.leftChild = newNode
                newNode.disc = (root.disc + 1) % self.dim
            else:
                print("rec call left")
                self._recInsert(root.leftChild,newNode)
                
    """ Return all nodes of the tree in order of layer by layer.
    """
    def GetAllNodes(self):
        nodes = []
        
        q = [self.root]
        while len(q) > 0:
            node = q.pop(0)
            if node:
                nodes.append(node)
                q.append(node.leftChild)
                q.append(node.rightChild)
        return nodes

    """ Return all edges of the tree in order of layer by layer.
    """
    def GetAllEdges(self):
        edges = []

        q = [self.root]
        while len(q) > 0:
            node = q.pop(0)
            if node:
                if node.leftChild:
                    q.append(node.leftChild)
                    edges.append((node, node.leftChild))
                if node.rightChild:
                    q.append(node.rightChild)
                    edges.append((node, node.rightChild))
        return edges
                              
    
    def Traversal(self,traversal_type="in"):
        self._Traversal(self.root,traversal_type)

    def _Traversal(self,root,traversal_type):
        if root == None:
            return
        else:
            if traversal_type == "pre":
                root.printNode()
                print("=========")
            self._Traversal(root.leftChild,traversal_type)
            if traversal_type == "in":
                root.printNode()
                print("=========")
            self._Traversal(root.rightChild,traversal_type)
            if traversal_type == "post":
                root.printNode()
                print("=========")

    def breadthFirst(self):
        self._breadthFirst(self.root,[])

    def _breadthFirst(self,root,queue):
        if root == None:
            return
        else:
            line = '[' + ','.join(map(str, root.dimList)) + ']'
            print (line)
            if not root.leftChild == None:
                queue.append(root.leftChild)
            if not root.rightChild == None:
                queue.append(root.rightChild)

            if len(queue) > 0:
                root = queue.pop(0)
                self._breadthFirst(root,queue)




    """
    @private
    @method - is_iterable: determines whether the var is iterable (list,etc)
    @param var: variable to be tested
    @returns bool: true if iterable
    """
    def _is_iterable(self,var):

        return isinstance(var, (list, tuple))

class draw_kdtree:
    def __init__(self, tree):
        self.tree = tree
        self.g = gv.Digraph(format='svg')

    """
    @public
    @method - AddNodes: add nodes to the graph
    @param nodes: list of nodes to be added to the graph
    """
    def AddNodes(self, nodes):
        for n in nodes:
            self.g.node('-'.join([str(e) for e in n.dimList]))

    """
    @public
    @method - AddEdges: add edges to the graph
    @param edges: list of edges to be added
    """
    def AddEdges(self, edges):
        for e in edges:
            self.g.edge('-'.join([str(e) for e in e[0].dimList]), \
                        '-'.join([str(e) for e in e[1].dimList]))
            

    """
    @public
    @method - Draw: draw the kd-tree as a graph and save the svg file
    """
    def Draw(self):
        self.g.render('kdtree-out.svg')

    """
    @public
    @method - Prepare2Draw: add nodes and edges to graph
    """
    def Prepare2Draw(self):
        self.AddNodes(self.tree.GetAllNodes())
        self.AddEdges(self.tree.GetAllEdges())
    

if __name__ == '__main__':
    time1 = time.time()
    
    tree = kdtree(3)
    tree.insert([3,1,4])
    tree.insert([2,3,7])
    tree.insert([4,3,4])
    tree.insert([2,1,3])
    tree.insert([2,4,5])
    tree.insert([6,1,4])
    tree.insert([1,4,4])
    tree.insert([0,5,7])
    tree.insert([5,2,5])
    tree.insert([4,0,6])
    tree.insert([7,1,6])
    tree.Traversal("pre")
    tree.breadthFirst()

    d = draw_kdtree(tree)
    d.Prepare2Draw()
    d.Draw()
    
    print("Program ran in %.2f seconds."%(time.time()-time1))

