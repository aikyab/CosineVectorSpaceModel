
import math
class Node:
    def __init__(self,val):
        self.val = val
        self.left = None
        self.right = None

node1 = Node(5)
node1.left = Node(4)
node1.right = Node(10)
nodeleft = node1.left
nodeleft.left = Node(8)
nodeleft.right = Node(3)

noderight = node1.right
noderight.left = Node(16)
noderight.right = Node(9)

nodeleft.right.right = Node(1)

def recursive(node,sumx,list1):
    if not node:
        return
    if not node.left and not node.right:
        sumx+=node.val
        list1.append(sumx)
        return
    else:
        recursive(node.left,sumx+node.val,list1)
        recursive(node.right,sumx+node.val,list1)


mini = []
recursive(node1,0,mini)

print(min(mini))

print(math.log(1/3,2))
print(math.sqrt(2.344))